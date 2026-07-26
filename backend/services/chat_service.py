import logging

import httpx

from config import settings
from services.knowledge_base import find_answer

logger = logging.getLogger(__name__)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
POLLINATIONS_URL = "https://text.pollinations.ai/openai/chat/completions"

SYSTEM_PROMPT = settings.CHAT_SYSTEM_PROMPT

PROVIDER_ERRORS = []


async def _call_gemini(messages: list[dict]) -> dict:
    """Call Google Gemini via OpenAI-compatible endpoint."""
    if not settings.GEMINI_API_KEY:
        return {"error": "no key", "provider": "gemini"}

    headers = {
        "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.GEMINI_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 0.9,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(GEMINI_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    text = data["choices"][0]["message"]["content"]
    return {
        "text": text.strip(),
        "provider": "gemini",
        "model": settings.GEMINI_MODEL,
        "usage": data.get("usage", {}),
    }


async def _call_pollinations(messages: list[dict]) -> dict:
    """Call Pollinations.ai — free, no API key required."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "openai",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 0.9,
    }

    async with httpx.AsyncClient(timeout=45.0) as client:
        response = await client.post(POLLINATIONS_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    text = data["choices"][0]["message"]["content"]
    return {
        "text": text.strip(),
        "provider": "pollinations",
        "model": data.get("model", "openai-fast"),
        "usage": data.get("usage", {}),
    }


async def chat_completion(
    user_message: str,
    conversation_history: list[dict] | None = None,
    subject: str = "General",
) -> dict:
    """Generate a chat response using real AI providers.

    Tries: offline knowledge base → Pollinations → Gemini.
    Returns the fallback message if all fail.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if subject != "General":
        messages.append({
            "role": "system",
            "content": f"The student is asking about {subject}. Focus your response on this subject.",
        })

    if conversation_history:
        messages.extend(conversation_history[-10:])

    messages.append({"role": "user", "content": user_message})

    offline_answer = find_answer(user_message, subject)
    if offline_answer:
        return {
            "text": offline_answer,
            "provider": "offline_knowledge_base",
            "model": "none",
            "usage": {},
        }

    errors = []
    try:
        result = await _call_pollinations(messages)
        if "error" not in result:
            return result
        errors.append(f"Pollinations: {result['error']}")
    except httpx.HTTPStatusError as e:
        errors.append(f"Pollinations: HTTP {e.response.status_code}")
    except Exception as e:
        errors.append(f"Pollinations: {e}")

    try:
        result = await _call_gemini(messages)
        if "error" not in result:
            return result
        errors.append(f"Gemini: {result['error']}")
    except httpx.HTTPStatusError as e:
        errors.append(f"Gemini: HTTP {e.response.status_code}")
    except Exception as e:
        errors.append(f"Gemini: {e}")

    if errors:
        logger.warning("AI providers failed: %s", "; ".join(errors))

    return {
        "text": (
            "I am not sure how to answer that right now. "
            "Please ask your teacher for help, or try asking a different question. "
            "You can ask me about subjects like Mathematics, Science, English, Social Studies, and Vocational Studies."
        ),
        "provider": "offline_fallback",
        "model": "none",
        "usage": {},
    }
