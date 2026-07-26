import io
import logging

import fitz
import docx
from PIL import Image

from services.ocr_service import extract_text_from_image

logger = logging.getLogger(__name__)


def _render_page_to_image(page) -> bytes:
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def extract_text_from_pdf(file_bytes: bytes) -> dict:
    """Extract text from a PDF using PyMuPDF."""
    try:
        pdf = fitz.open(stream=file_bytes, filetype="pdf")
        pages_text = []
        ocr_pages = []

        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text = page.get_text()
            if text.strip():
                pages_text.append(text.strip())

        full_text = "\n\n".join(pages_text)

        if full_text.strip():
            pdf.close()
            return {
                "text": full_text,
                "success": True,
                "page_count": len(pdf),
                "word_count": len(full_text.split()),
            }

        logger.info("No text layer found in PDF, falling back to OCR on rendered pages")
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            img_bytes = _render_page_to_image(page)
            ocr_result = extract_text_from_image(img_bytes, f"pdf_page_{page_num}")
            if ocr_result.get("success") and ocr_result.get("text", "").strip():
                ocr_pages.append(ocr_result["text"].strip())

        pdf.close()

        if ocr_pages:
            full_ocr_text = "\n\n".join(ocr_pages)
            return {
                "text": full_ocr_text,
                "success": True,
                "page_count": len(ocr_pages),
                "word_count": len(full_ocr_text.split()),
                "ocr_fallback": True,
            }

        return {
            "text": "",
            "success": False,
            "page_count": len(pdf),
            "error": "Could not extract text from this PDF. The document may be empty or unreadable.",
        }

    except Exception as e:
        logger.error("PDF extraction failed: %s", e)
        return {
            "text": "",
            "success": False,
            "error": f"Could not read this PDF: {e}",
        }


def extract_text_from_docx(file_bytes: bytes) -> dict:
    """Extract text from a Word document using python-docx."""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)

        full_text = "\n\n".join(paragraphs)

        if not full_text.strip():
            return {
                "text": "",
                "success": False,
                "paragraph_count": len(paragraphs),
                "error": "No readable text found in this document.",
            }

        return {
            "text": full_text,
            "success": True,
            "paragraph_count": len(paragraphs),
            "word_count": len(full_text.split()),
        }

    except Exception as e:
        logger.error("DOCX extraction failed: %s", e)
        return {
            "text": "",
            "success": False,
            "error": f"Could not read this Word document: {e}",
        }
