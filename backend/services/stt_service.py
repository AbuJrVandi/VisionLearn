import logging

import httpx

from config import settings

logger = logging.getLogger(__name__)

HF_WHISPER_URL = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"


async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav") -> dict:
    """Transcribe audio to text using Hugging Face Whisper.

    The frontend also supports browser-based speech recognition via the Web
    Speech API — this backend endpoint is a fallback for browsers that lack
    that support.
    """
    if not settings.HF_API_KEY:
        return {
            "text": "",
            "success": False,
            "error": "Speech-to-text not configured. Please type your message or use the browser microphone.",
        }

    try:
        headers = {"Authorization": f"Bearer {settings.HF_API_KEY}"}
        files = {"file": (filename, audio_bytes, "audio/wav")}
        payload = {
            "parameters": {
                "language": "en",
                "task": "transcribe",
            }
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(HF_WHISPER_URL, headers=headers, files=files, json=payload)

            if response.status_code == 503:
                data = response.json()
                if data.get("error") and "loading" in data["error"].lower():
                    return {
                        "text": "",
                        "success": False,
                        "error": "STT model is loading, please try again in 30 seconds.",
                    }

            response.raise_for_status()
            result = response.json()

        text = result.get("text", "")
        return {
            "text": text,
            "success": True,
            "language": result.get("language", "en"),
        }

    except httpx.HTTPStatusError as e:
        logger.error("Whisper API error %s: %s", e.response.status_code, e.response.text)
        return {
            "text": "",
            "success": False,
            "error": "Could not process audio. Please try again or type your message.",
        }
    except Exception as e:
        logger.error("Transcription failed: %s", e)
        return {
            "text": "",
            "success": False,
            "error": "Audio processing failed. Please type your message instead.",
        }
