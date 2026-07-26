import logging

import httpx

from config import settings
from services.knowledge_base import find_answer
from services.online_knowledge import format_knowledge_context, search_online_knowledge

logger = logging.getLogger(__name__)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
POLLINATIONS_URL = "https://text.pollinations.ai/openai/chat/completions"

SYSTEM_PROMPT = settings.CHAT_SYSTEM_PROMPT


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
        "model": data.get("model", "openai"),
        "usage": data.get("usage", {}),
    }


async def chat_completion(
    user_message: str,
    conversation_history: list[dict] | None = None,
    subject: str = "General",
    db=None,
) -> dict:
    """Generate a chat response with free online + offline knowledge support.

    Order:
      1) Offline curriculum knowledge base (instant, no network)
      2) Free online KB = search Document Library (SQLite) + ground LLM
      3) Pollinations (free API)
      4) Gemini (free tier when key set)
      5) Clear offline fallback message
    """
    # 1) Offline curriculum KB (keyword curriculum entries)
    offline_answer = find_answer(user_message, subject)
    if offline_answer:
        return {
            "text": offline_answer,
            "provider": "offline_knowledge_base",
            "model": "none",
            "usage": {},
            "knowledge_sources": [],
            "knowledge_mode": "offline_curriculum",
        }

    # 2) Free online KB: retrieve from uploaded library documents
    knowledge_sources: list[dict] = []
    online_context = ""
    if db is not None:
        try:
            snippets = await search_online_knowledge(db, user_message, subject)
            if snippets:
                online_context = format_knowledge_context(snippets)
                knowledge_sources = [
                    {
                        "document_id": s.get("document_id"),
                        "title": s.get("title"),
                        "subject": s.get("subject"),
                        "score": round(float(s.get("score", 0)), 2),
                    }
                    for s in snippets
                ]
        except Exception as e:
            logger.warning("Online knowledge retrieval failed: %s", e)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if subject != "General":
        messages.append({
            "role": "system",
            "content": f"The student is asking about {subject}. Focus your response on this subject.",
        })

    if online_context:
        messages.append({
            "role": "system",
            "content": online_context,
        })

    if conversation_history:
        messages.extend(conversation_history[-10:])

    messages.append({"role": "user", "content": user_message})

    errors: list[str] = []

    # Prefer Gemini when key is set (better grounding quality), else free Pollinations first
    provider_order = []
    if settings.GEMINI_API_KEY:
        provider_order.append(("gemini", _call_gemini))
        provider_order.append(("pollinations", _call_pollinations))
    else:
        provider_order.append(("pollinations", _call_pollinations))
        provider_order.append(("gemini", _call_gemini))

    for name, fn in provider_order:
        try:
            result = await fn(messages)
            if "error" not in result:
                result["knowledge_sources"] = knowledge_sources
                result["knowledge_mode"] = (
                    "online_library_rag" if knowledge_sources else "general_ai"
                )
                return result
            errors.append(f"{name}: {result['error']}")
        except httpx.HTTPStatusError as e:
            errors.append(f"{name}: HTTP {e.response.status_code}")
        except Exception as e:
            errors.append(f"{name}: {e}")

    if errors:
        logger.warning("AI providers failed: %s", "; ".join(errors))

    # If we have library material but APIs failed, return a plain extractive answer
    if knowledge_sources and online_context:
        plain = (
            "I found this in your school learning materials. "
            "The online tutor service is temporarily unavailable, so here is the relevant text. "
        )
        # Reuse first passages without system instructions
        extract_bits = []
        for line in online_context.split("\n\n"):
            if line.startswith("[Source"):
                extract_bits.append(line)
        if extract_bits:
            text = plain + " ".join(
                re_sub_source_header(bit) for bit in extract_bits[:2]
            )
            return {
                "text": text[:1500],
                "provider": "online_knowledge_base",
                "model": "none",
                "usage": {},
                "knowledge_sources": knowledge_sources,
                "knowledge_mode": "online_library_extractive",
            }

    return {
        "text": (
            "I am not sure how to answer that right now. "
            "Please ask your teacher for help, or try asking a different question. "
            "You can also upload a lesson document to the Library so I can use it as a knowledge base. "
            "You can ask me about subjects like Mathematics, Science, English, Social Studies, and Vocational Studies."
        ),
        "provider": "offline_fallback",
        "model": "none",
        "usage": {},
        "knowledge_sources": knowledge_sources,
        "knowledge_mode": "fallback",
    }


def re_sub_source_header(block: str) -> str:
    """Strip [Source N: ...] header for extractive fallback speech."""
    lines = block.split("\n", 1)
    if len(lines) == 2 and lines[0].startswith("[Source"):
        return lines[1].strip()
    return block.strip()
