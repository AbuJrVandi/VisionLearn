from fastapi import APIRouter
from pydantic import BaseModel, Field

from models.database import get_database
from services.chat_service import chat_completion

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    session_id: int | None = Field(default=None, description="Existing session ID")
    subject: str = Field(default="General", description="Academic subject")


class ChatMessage(BaseModel):
    role: str
    content: str


@router.post("/send")
async def send_message(request: ChatRequest):
    """Send a message to the AI tutor and receive a response."""
    db = await get_database()
    try:
        if request.session_id:
            rows = await db.execute_fetchall(
                "SELECT role, content FROM chat_messages WHERE session_id = ? ORDER BY id",
                (request.session_id,),
            )
            history = [ChatMessage(role=row["role"], content=row["content"]).model_dump() for row in rows]
            session_id = request.session_id
        else:
            cursor = await db.execute(
                "INSERT INTO chat_sessions (session_type) VALUES (?)",
                ("chat",),
            )
            await db.commit()
            session_id = cursor.lastrowid
            history = []

        await db.execute(
            "INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, "user", request.message),
        )
        await db.commit()

        # Free online knowledge base: search Document Library (SQLite) then tutor
        ai_result = await chat_completion(
            user_message=request.message,
            conversation_history=history,
            subject=request.subject,
            db=db,
        )

        await db.execute(
            "INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, "assistant", ai_result["text"]),
        )
        await db.commit()

        mode = ai_result.get("knowledge_mode", "")
        await db.execute(
            "INSERT INTO usage_logs (action, detail) VALUES (?, ?)",
            ("chat", f"{request.subject}|{mode}"),
        )
        await db.commit()

        return {
            "session_id": session_id,
            "response": ai_result["text"],
            "provider": ai_result.get("provider", "unknown"),
            "model": ai_result.get("model", "unknown"),
            "knowledge_mode": ai_result.get("knowledge_mode", "unknown"),
            "knowledge_sources": ai_result.get("knowledge_sources", []),
        }

    finally:
        await db.close()


@router.get("/sessions")
async def list_sessions():
    """List all chat sessions."""
    db = await get_database()
    try:
        rows = await db.execute_fetchall(
            "SELECT id, session_type, created_at FROM chat_sessions ORDER BY created_at DESC"
        )
        return {"sessions": [dict(row) for row in rows]}
    finally:
        await db.close()


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: int):
    """Get all messages for a chat session."""
    db = await get_database()
    try:
        rows = await db.execute_fetchall(
            "SELECT role, content, created_at FROM chat_messages WHERE session_id = ? ORDER BY id",
            (session_id,),
        )
        return {"messages": [dict(row) for row in rows]}
    finally:
        await db.close()


@router.get("/analytics")
async def get_analytics():
    """Get usage analytics with time-series data for charts."""
    db = await get_database()
    try:
        action_counts = await db.execute_fetchall(
            "SELECT action, COUNT(*) as count FROM usage_logs GROUP BY action"
        )
        total_documents = await db.execute_fetchall("SELECT COUNT(*) as count FROM documents")
        total_sessions = await db.execute_fetchall("SELECT COUNT(*) as count FROM chat_sessions")
        recent_activity = await db.execute_fetchall(
            "SELECT action, detail, created_at FROM usage_logs ORDER BY created_at DESC LIMIT 20"
        )

        daily_activity = await db.execute_fetchall(
            "SELECT DATE(created_at) as day, action, COUNT(*) as count "
            "FROM usage_logs "
            "WHERE created_at >= datetime('now', '-7 days') "
            "GROUP BY DATE(created_at), action "
            "ORDER BY day ASC"
        )

        hourly_activity = await db.execute_fetchall(
            "SELECT strftime('%H', created_at) as hour, COUNT(*) as count "
            "FROM usage_logs "
            "GROUP BY strftime('%H', created_at) "
            "ORDER BY hour ASC"
        )

        subject_dist = await db.execute_fetchall(
            "SELECT subject, COUNT(*) as count FROM documents GROUP BY subject"
        )

        return {
            "action_counts": {row["action"]: row["count"] for row in action_counts},
            "total_documents": total_documents[0]["count"] if total_documents else 0,
            "total_chat_sessions": total_sessions[0]["count"] if total_sessions else 0,
            "recent_activity": [dict(row) for row in recent_activity],
            "daily_activity": [dict(row) for row in daily_activity],
            "hourly_activity": [dict(row) for row in hourly_activity],
            "subject_distribution": [dict(row) for row in subject_dist],
        }
    finally:
        await db.close()
