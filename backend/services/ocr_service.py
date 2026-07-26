import io
import logging
import re
from pathlib import Path

import numpy as np
import pytesseract
from PIL import Image, ImageFilter, ImageOps

logger = logging.getLogger(__name__)

TESSERACT_BASE = "--oem 3"
LANG = "eng"
PSM_MODES = [3, 6, 4, 11, 12]
CONFIDENCE_THRESHOLD = 55


def _otsu_threshold(arr: np.ndarray) -> int:
    hist, _ = np.histogram(arr, bins=256, range=(0, 256))
    total = arr.size
    if total == 0:
        return 128
    sum_total = float(np.dot(hist, np.arange(256)))
    sum_b, w_b = 0.0, 0
    best_thresh, best_var = 0, 0.0
    for t in range(256):
        w_b += hist[t]
        if w_b == 0:
            continue
        w_f = total - w_b
        if w_f == 0:
            break
        sum_b += t * hist[t]
        mean_b = sum_b / w_b
        mean_f = (sum_total - sum_b) / w_f
        var = w_b * w_f * (mean_b - mean_f) ** 2
        if var > best_var:
            best_var = var
            best_thresh = t
    return best_thresh


def _preprocess_variants(image: Image.Image) -> list[tuple[str, Image.Image]]:
    if image.mode != "L":
        gray = image.convert("L")
    else:
        gray = image.copy()

    variants = []

    variants.append(("original_gray", gray))

    denoised = gray.filter(ImageFilter.MedianFilter(size=3))
    eq = ImageOps.equalize(denoised)
    variants.append(("equalized", eq))

    sharp = gray.filter(ImageFilter.UnsharpMask(radius=1, percent=100, threshold=2))
    variants.append(("sharpened", sharp))

    arr = np.array(denoised, dtype=np.uint8)
    thresh = _otsu_threshold(arr)
    otsu = Image.fromarray((arr > thresh).astype(np.uint8) * 255, mode="L")
    variants.append(("otsu", otsu))

    remapped = Image.fromarray(arr, mode="L")
    inv = ImageOps.invert(remapped)
    inv_thresh = _otsu_threshold(np.array(inv, dtype=np.uint8))
    inv_bin = Image.fromarray((np.array(inv, dtype=np.uint8) > inv_thresh).astype(np.uint8) * 255, mode="L")
    variants.append(("inverted_otsu", inv_bin))

    return variants


def _is_junk_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped or len(stripped) < 3:
        return True
    alpha_count = sum(1 for c in stripped if c.isalpha())
    if alpha_count == 0:
        return True
    alpha_ratio = alpha_count / len(stripped)
    if alpha_ratio < 0.4 and len(stripped) > 5:
        return True
    words = stripped.split()
    single_letter_words = sum(1 for w in words if len(w) == 1 and w.isalpha())
    if len(words) > 2 and single_letter_words / len(words) > 0.5:
        return True
    return False


def _postprocess_text(text: str) -> str:
    lines = text.split("\n")
    clean_lines = []
    for line in lines:
        if not _is_junk_line(line):
            clean_lines.append(line)
    text = "\n".join(clean_lines)

    text = re.sub(r"[|¦I]", "I", text)
    text = re.sub(r"\[\s*\]", "", text)
    text = re.sub(r"\(\s*\)", "", text)

    text = re.sub(r"(?<![A-Za-z])[0O]{2,}(?![A-Za-z])", lambda m: "0" if all(c == "0" for c in m.group(0)) else "O", text)

    text = re.sub(r"[^\S\n]+", " ", text)
    text = re.sub(r" (?=\n)", "", text)
    text = re.sub(r"(?<=\n) ", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"^[^A-Za-z0-9]+", "", text)

    return text.strip()


def _run_tesseract(image: Image.Image, psm: int) -> dict | None:
    config = f"{TESSERACT_BASE} --psm {psm} -l {LANG}"
    try:
        data = pytesseract.image_to_data(image, config=config, output_type=pytesseract.Output.DICT)
        words_with_conf = []
        for word, conf in zip(data["text"], data["conf"]):
            w = word.strip()
            if w and int(conf) > 0:
                words_with_conf.append({"word": w, "confidence": int(conf)})
        if not words_with_conf:
            return None
        avg_conf = sum(w["confidence"] for w in words_with_conf) / len(words_with_conf)
        full_text = pytesseract.image_to_string(image, config=config).strip()
        if not full_text:
            return None
        return {
            "text": full_text,
            "confidence": avg_conf,
            "word_count": len(full_text.split()),
            "character_count": len(full_text),
        }
    except Exception as e:
        logger.debug("Tesseract failed psm=%d: %s", psm, e)
        return None


def extract_text_from_image(image_bytes: bytes, filename: str = "") -> dict:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        variants = _preprocess_variants(image)

        best = {"text": "", "confidence": 0.0, "word_count": 0, "character_count": 0}

        for variant_name, processed in variants:
            result = _run_tesseract(processed, psm=3)
            if result and result["confidence"] > best["confidence"]:
                best["text"] = result["text"]
                best["confidence"] = result["confidence"]
                best["word_count"] = result["word_count"]
                best["character_count"] = result["character_count"]
                best["variant"] = variant_name

        if best["confidence"] < CONFIDENCE_THRESHOLD and best["text"]:
            best_img = None
            best_variant_conf = 0
            for vname, vimg in variants:
                result = _run_tesseract(vimg, psm=6)
                if result and result["confidence"] > best_variant_conf:
                    best_variant_conf = result["confidence"]
                    best_img = vimg

            if best_img:
                for psm in PSM_MODES:
                    if psm in (3, 6):
                        continue
                    result = _run_tesseract(best_img, psm=psm)
                    if result and result["confidence"] > best["confidence"]:
                        best["text"] = result["text"]
                        best["confidence"] = result["confidence"]
                        best["word_count"] = result["word_count"]
                        best["character_count"] = result["character_count"]

        if best["text"]:
            best["text"] = _postprocess_text(best["text"])
            best["word_count"] = len(best["text"].split())
            best["character_count"] = len(best["text"])

        return {
            "text": best["text"],
            "confidence": round(best["confidence"], 1),
            "word_count": best["word_count"],
            "character_count": best["character_count"],
            "filename": filename,
            "success": bool(best["text"]),
        }

    except Exception as e:
        logger.error("OCR failed for %s: %s", filename, e)
        return {
            "text": "", "confidence": 0, "word_count": 0,
            "character_count": 0, "filename": filename,
            "success": False, "error": str(e),
        }


def extract_text_from_file(file_path: Path) -> dict:
    image_bytes = file_path.read_bytes()
    return extract_text_from_image(image_bytes, file_path.name)
