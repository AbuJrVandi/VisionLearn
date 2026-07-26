"""
Free online knowledge base for the VisionLearn AI tutor.

Uses school materials already stored in the documents table (Document Library)
as a curriculum knowledge base. No paid vector database is required:
keyword scoring + passage extraction runs entirely on the free backend/SQLite.
"""

from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

# Stop words kept small so maths/science terms are not dropped.
_STOP = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should", "may",
    "might", "must", "shall", "can", "need", "dare", "ought", "used",
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us",
    "them", "my", "your", "his", "its", "our", "their", "this", "that",
    "these", "those", "what", "which", "who", "whom", "whose", "where",
    "when", "why", "how", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own",
    "same", "so", "than", "too", "very", "just", "about", "into", "from",
    "with", "as", "by", "please", "tell", "explain", "help", "know",
    "want", "like", "something", "anything", "question", "answer",
}


def _tokenize(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if len(w) > 2 and w not in _STOP]


def _split_passages(text: str, max_chars: int = 450) -> list[str]:
    """Split document text into roughly paragraph/sentence-sized passages."""
    if not text or not text.strip():
        return []
    # Prefer paragraphs, then sentences
    chunks = re.split(r"\n\s*\n+", text.strip())
    passages: list[str] = []
    for chunk in chunks:
        chunk = re.sub(r"\s+", " ", chunk).strip()
        if not chunk:
            continue
        if len(chunk) <= max_chars:
            passages.append(chunk)
            continue
        sentences = re.split(r"(?<=[.!?])\s+", chunk)
        buf = ""
        for sent in sentences:
            if not sent:
                continue
            if len(buf) + len(sent) + 1 <= max_chars:
                buf = f"{buf} {sent}".strip()
            else:
                if buf:
                    passages.append(buf)
                buf = sent[:max_chars]
        if buf:
            passages.append(buf)
    return passages


def _score_passage(tokens: list[str], passage: str) -> float:
    if not tokens or not passage:
        return 0.0
    lower = passage.lower()
    score = 0.0
    for t in tokens:
        # whole-word preference
        count = len(re.findall(rf"\b{re.escape(t)}\b", lower))
        if count:
            score += count * (1.0 + 0.15 * min(len(t), 12))
    # slight boost for denser matches
    if score > 0:
        unique_hits = sum(1 for t in set(tokens) if re.search(rf"\b{re.escape(t)}\b", lower))
        score += unique_hits * 0.5
    return score


async def search_online_knowledge(
    db,
    query: str,
    subject: str = "General",
    *,
    top_k: int = 4,
    max_total_chars: int = 2200,
) -> list[dict[str, Any]]:
    """
    Search uploaded library documents for passages relevant to the query.

    Returns a list of {title, subject, passage, score, document_id}.
    Free: uses only SQLite + Python (no embeddings / paid vector DB).
    """
    tokens = _tokenize(query)
    if not tokens:
        return []

    try:
        if subject and subject != "General":
            rows = await db.execute_fetchall(
                "SELECT id, original_name, subject, extracted_text, summary "
                "FROM documents "
                "WHERE (extracted_text IS NOT NULL AND LENGTH(TRIM(extracted_text)) > 40) "
                "AND (subject = ? OR subject = 'General' OR subject IS NULL OR subject = '') "
                "ORDER BY created_at DESC LIMIT 80",
                (subject,),
            )
        else:
            rows = await db.execute_fetchall(
                "SELECT id, original_name, subject, extracted_text, summary "
                "FROM documents "
                "WHERE extracted_text IS NOT NULL AND LENGTH(TRIM(extracted_text)) > 40 "
                "ORDER BY created_at DESC LIMIT 80"
            )
    except Exception as e:
        logger.warning("Online KB query failed: %s", e)
        return []

    candidates: list[dict[str, Any]] = []
    for row in rows:
        doc = dict(row)
        text = (doc.get("extracted_text") or "").strip()
        summary = (doc.get("summary") or "").strip()
        if summary:
            text = f"{summary}\n\n{text}"
        title = doc.get("original_name") or doc.get("filename") or "Document"
        doc_subject = doc.get("subject") or "General"
        doc_id = doc.get("id")

        for passage in _split_passages(text):
            score = _score_passage(tokens, passage)
            if score <= 0:
                continue
            candidates.append(
                {
                    "document_id": doc_id,
                    "title": title,
                    "subject": doc_subject,
                    "passage": passage,
                    "score": score,
                }
            )

    if not candidates:
        return []

    candidates.sort(key=lambda c: c["score"], reverse=True)

    selected: list[dict[str, Any]] = []
    used_chars = 0
    seen_passages: set[str] = set()
    for item in candidates:
        key = item["passage"][:120]
        if key in seen_passages:
            continue
        seen_passages.add(key)
        length = len(item["passage"])
        if selected and used_chars + length > max_total_chars:
            continue
        selected.append(item)
        used_chars += length
        if len(selected) >= top_k:
            break

    return selected


def format_knowledge_context(snippets: list[dict[str, Any]]) -> str:
    """Format retrieved passages for injection into the tutor system prompt."""
    if not snippets:
        return ""
    parts = [
        "Use the following school learning materials from the VisionLearn document library "
        "to answer the student. Prefer these materials when they are relevant. "
        "Explain in plain language suitable for text-to-speech. "
        "If the materials do not contain the answer, say so honestly and give a careful general explanation."
    ]
    for i, snip in enumerate(snippets, 1):
        title = snip.get("title", "Document")
        subj = snip.get("subject", "General")
        passage = snip.get("passage", "")
        parts.append(f"[Source {i}: {title} | Subject: {subj}]\n{passage}")
    return "\n\n".join(parts)
