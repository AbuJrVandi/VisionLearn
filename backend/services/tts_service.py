import logging

import edge_tts

logger = logging.getLogger(__name__)

VOICES = [
    "en-US-AriaNeural",
    "en-US-JennyNeural",
    "en-US-EmmaNeural",
    "en-US-GuyNeural",
    "en-GB-LibbyNeural",
    "en-GB-RyanNeural",
]


async def generate_speech(text: str, lang: str = "en", slow: bool = False) -> bytes | None:
    if not text or not text.strip():
        return None

    rate = "-15%" if slow else "+0%"

    for voice in VOICES:
        try:
            communicate = edge_tts.Communicate(text.strip(), voice, rate=rate)
            audio_buffer = bytearray()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_buffer.extend(chunk["data"])
            if audio_buffer:
                return bytes(audio_buffer)
        except Exception as e:
            logger.warning("edge-tts voice '%s' failed: %s", voice, e)
            continue

    logger.error("All edge-tts voices failed")
    return None
