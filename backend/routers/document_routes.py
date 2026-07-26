import hashlib
import logging
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from config import settings
from models.database import get_database
from services.ocr_service import extract_text_from_image
from services.document_extraction import extract_text_from_pdf, extract_text_from_docx
from services.chat_service import chat_completion

logger = logging.getLogger(__name__)
router = APIRouter()


def _generate_summary_prompt(text: str) -> str:
    """Build a summarisation prompt from document text."""
    truncated = text[:6000]
    return (
        f"Summarise the following document in 3 to 5 clear, simple sentences "
        f"suitable for a visually impaired student. Focus on the main topic and "
        f"key points. Use plain language.\n\nDocument text:\n{truncated}"
    )


async def _generate_summary(text: str) -> str:
    """Generate an AI summary of extracted document text."""
    if not text or len(text.strip()) < 50:
        return ""
    try:
        result = await chat_completion(_generate_summary_prompt(text))
        return result.get("text", "")
    except Exception as e:
        logger.warning("Summary generation failed: %s", e)
        return ""


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    subject: str = Form(default="General"),
):
    """Upload a document or image, extract text, generate AI summary, and store."""
    if not file.content_type:
        raise HTTPException(status_code=400, detail="File type could not be determined.")

    allowed = settings.ALLOWED_IMAGE_TYPES + settings.ALLOWED_DOC_TYPES
    if file.content_type not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file.content_type}' is not supported.",
        )

    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File exceeds the 10 MB size limit.")

    ext = Path(file.filename or "upload").suffix or ".bin"
    content_hash = hashlib.sha256(contents).hexdigest()[:12]
    safe_name = f"{Path(file.filename or 'upload').stem}_{content_hash}{ext}"
    file_path = settings.UPLOAD_DIR / safe_name

    file_path.write_bytes(contents)

    extracted_text = ""
    summary = ""

    if file.content_type in settings.ALLOWED_IMAGE_TYPES:
        result = extract_text_from_image(contents, safe_name)
        if result["success"]:
            extracted_text = result["text"]

    elif file.content_type == "application/pdf":
        result = extract_text_from_pdf(contents)
        if result["success"]:
            extracted_text = result["text"]

    elif file.content_type in (
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ):
        result = extract_text_from_docx(contents)
        if result["success"]:
            extracted_text = result["text"]

    elif file.content_type == "text/plain":
        try:
            extracted_text = contents.decode("utf-8")
        except UnicodeDecodeError:
            try:
                extracted_text = contents.decode("latin-1")
            except Exception:
                extracted_text = ""

    if extracted_text:
        summary = await _generate_summary(extracted_text)

    db = await get_database()
    try:
        cursor = await db.execute(
            "INSERT INTO documents (filename, original_name, file_type, file_size, extracted_text, subject, summary) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (safe_name, file.filename, file.content_type, len(contents), extracted_text, subject, summary),
        )
        await db.commit()
        doc_id = cursor.lastrowid

        await db.execute("INSERT INTO usage_logs (action, detail) VALUES (?, ?)", ("upload", safe_name))
        await db.commit()
    finally:
        await db.close()

    return {
        "id": doc_id,
        "filename": safe_name,
        "original_name": file.filename,
        "file_type": file.content_type,
        "file_size": len(contents),
        "extracted_text": extracted_text,
        "summary": summary,
        "subject": subject,
    }


@router.get("/list")
async def list_documents(subject: str | None = None):
    """List all uploaded documents, optionally filtered by subject."""
    db = await get_database()
    try:
        if subject:
            rows = await db.execute_fetchall(
                "SELECT * FROM documents WHERE subject = ? ORDER BY created_at DESC",
                (subject,),
            )
        else:
            rows = await db.execute_fetchall("SELECT * FROM documents ORDER BY created_at DESC")

        return {"documents": [dict(row) for row in rows]}
    finally:
        await db.close()


@router.get("/{doc_id}")
async def get_document(doc_id: int):
    """Get a single document by ID."""
    db = await get_database()
    try:
        row = await db.execute_fetchall("SELECT * FROM documents WHERE id = ?", (doc_id,))
        if not row:
            raise HTTPException(status_code=404, detail="Document not found.")
        return dict(row[0])
    finally:
        await db.close()


@router.delete("/{doc_id}")
async def delete_document(doc_id: int):
    """Delete a document by ID."""
    db = await get_database()
    try:
        row = await db.execute_fetchall("SELECT filename FROM documents WHERE id = ?", (doc_id,))
        if not row:
            raise HTTPException(status_code=404, detail="Document not found.")

        file_path = settings.UPLOAD_DIR / row[0]["filename"]
        if file_path.exists():
            file_path.unlink()

        await db.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        await db.commit()

        return {"message": "Document deleted successfully."}
    finally:
        await db.close()


@router.post("/ocr")
async def process_ocr(file: UploadFile = File(...)):
    """Run OCR on an uploaded image and return extracted text."""
    if not file.content_type or file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Please upload a PNG, JPEG, or WebP image.")

    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="Image exceeds the 10 MB size limit.")

    result = extract_text_from_image(contents, file.filename or "camera_capture")

    db = await get_database()
    try:
        await db.execute("INSERT INTO usage_logs (action, detail) VALUES (?, ?)", ("ocr", file.filename))
        await db.commit()
    finally:
        await db.close()

    return result
