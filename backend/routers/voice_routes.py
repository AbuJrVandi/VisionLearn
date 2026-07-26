import io

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from models.database import get_database
from services.stt_service import transcribe_audio
from services.tts_service import generate_speech

MAX_TTS_LENGTH = 5000
router = APIRouter()


@router.post("/tts")
async def text_to_speech(
    text: str = Form(...),
    lang: str = Form(default="en"),
    slow: bool = Form(default=False),
):
    """Convert text to speech and return an MP3 audio stream."""
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    if len(text) > MAX_TTS_LENGTH:
        raise HTTPException(status_code=400, detail=f"Text exceeds {MAX_TTS_LENGTH} character limit.")

    audio_bytes = await generate_speech(text, lang=lang, slow=slow)
    if not audio_bytes:
        raise HTTPException(status_code=500, detail="Failed to generate speech audio.")

    db = await get_database()
    try:
        await db.execute("INSERT INTO usage_logs (action, detail) VALUES (?, ?)", ("tts", text[:100]))
        await db.commit()
    finally:
        await db.close()

    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=speech.mp3"},
    )


@router.post("/stt")
async def speech_to_text(
    file: UploadFile = File(...),
):
    """Transcribe an audio file to text using Whisper."""
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Please upload an audio file.")

    audio_bytes = await file.read()
    if len(audio_bytes) > 25 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Audio file exceeds 25 MB limit.")

    result = await transcribe_audio(audio_bytes, filename=file.filename or "recording.wav")

    db = await get_database()
    try:
        await db.execute("INSERT INTO usage_logs (action, detail) VALUES (?, ?)", ("stt", result.get("text", "")[:100]))
        await db.commit()
    finally:
        await db.close()

    return result
