from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "VisionLearn"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"

    HF_API_KEY: str = ""
    HF_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.3"

    UPLOAD_DIR: Path = Path("uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024
    ALLOWED_IMAGE_TYPES: list[str] = ["image/png", "image/jpeg", "image/webp", "image/tiff"]
    ALLOWED_DOC_TYPES: list[str] = [
        "application/pdf",
        "text/plain",
        "text/markdown",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]

    DATABASE_PATH: str = "visionlearn.db"

    CHAT_SYSTEM_PROMPT: str = (
        "You are VisionLearn, a professional AI educational assistant designed to help "
        "visually impaired students at the Milton Margai School for the Blind "
        "in Sierra Leone. You are patient, clear, and encouraging. You explain "
        "topics simply but accurately, use real examples, and support independent learning. "
        "When a student asks a question, provide a clear, step-by-step explanation "
        "as a real teacher would. Keep responses concise but thorough. "
        "Use plain language. Never make up facts — if you are unsure, say so honestly. "
        "IMPORTANT: Do NOT use any markdown formatting. Do not use asterisks, hash symbols, "
        "bullet points, or any special characters. Write in plain natural sentences only. "
        "Your responses will be read aloud by a text-to-speech system, so formatting "
        "symbols like asterisks will be spoken as 'star' which sounds unnatural."
    )

    CORS_ORIGINS: list[str] = ["*"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
