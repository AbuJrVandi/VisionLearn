import { useState, useRef, useEffect } from "react";
import { Send, Loader2, MessageSquare, RotateCcw, BookOpen } from "lucide-react";
import { useSpeechSynthesis } from "../hooks/useSpeechSynthesis";
import { sendChatMessage, getChatSessions } from "../services/api";

const SUBJECTS = [
  "General",
  "Mathematics",
  "Science",
  "English",
  "Social Studies",
  "Vocational",
];

export default function ChatTutorPage() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [subject, setSubject] = useState("General");
  const [sessions, setSessions] = useState([]);
  const messagesEndRef = useRef(null);
  const { speak, isSpeaking, stop: stopSpeaking } = useSpeechSynthesis();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const data = await getChatSessions();
      setSessions(data.sessions || []);
    } catch {
      /* silent */
    }
  };

  const handleSend = async () => {
    const text = inputText.trim();
    if (!text || loading) return;

    const userMessage = { role: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);
    setInputText("");
    setLoading(true);

    try {
      const data = await sendChatMessage(text, sessionId, subject);
      setSessionId(data.session_id);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
          provider: data.provider,
          knowledgeMode: data.knowledge_mode,
          knowledgeSources: data.knowledge_sources || [],
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setSessionId(null);
    setSubject("General");
  };

  return (
    <section aria-labelledby="chat-heading">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-violet-50 dark:bg-violet-950 flex items-center justify-center">
            <MessageSquare className="w-5 h-5 text-violet-600 dark:text-violet-400" aria-hidden="true" />
          </div>
          <h1 id="chat-heading" className="page-title mb-0">
            AI Tutor
          </h1>
        </div>
        <button
          onClick={handleNewChat}
          className="btn-secondary text-sm flex items-center gap-2"
          aria-label="Start new chat"
        >
          <RotateCcw className="w-4 h-4" />
          New Chat
        </button>
      </div>
      <p className="page-subtitle">
        Chat with an AI tutor for help with any school subject. Upload lessons to the
        Library to use them as a free online knowledge base.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-3">
          <div className="card h-[520px] flex flex-col">
            <div className="flex items-center gap-2 mb-3 pb-3 border-b border-slate-200 dark:border-slate-700">
              <BookOpen className="w-4 h-4 text-slate-400" />
              <span className="text-sm text-slate-500 dark:text-slate-400">Subject:</span>
              <select
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="text-sm rounded-lg px-2 py-1 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700"
                aria-label="Select subject"
              >
                {SUBJECTS.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>

            <div
              className="flex-1 overflow-y-auto space-y-4 mb-4 p-2"
              role="log"
              aria-live="polite"
              aria-label="Chat messages"
            >
              {messages.length === 0 && (
                <div className="text-center py-12 text-slate-400 dark:text-slate-500">
                  <MessageSquare className="w-12 h-12 mx-auto mb-3 opacity-50" />
                  <p className="text-lg font-medium mb-1 text-slate-600 dark:text-slate-300">
                    Start a conversation
                  </p>
                  <p className="text-sm">
                    Ask me anything about your school subjects. Materials in the
                    Document Library are used as a free online knowledge base.
                  </p>
                </div>
              )}

              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[85%] rounded-2xl px-4 py-3 ${
                      msg.role === "user"
                        ? "bg-violet-600 text-white"
                        : "bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200"
                    }`}
                  >
                    <p className="leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                    {msg.role === "assistant" && msg.provider && (
                      <p className="text-xs mt-2 opacity-50">
                        via {msg.provider}
                        {msg.knowledgeMode === "online_library_rag" ||
                        msg.knowledgeMode === "online_library_extractive"
                          ? " · online library knowledge"
                          : msg.knowledgeMode === "offline_curriculum"
                            ? " · offline curriculum"
                            : ""}
                      </p>
                    )}
                    {msg.role === "assistant" &&
                      msg.knowledgeSources &&
                      msg.knowledgeSources.length > 0 && (
                        <p className="text-xs mt-1 opacity-70" aria-label="Knowledge sources used">
                          Sources:{" "}
                          {msg.knowledgeSources
                            .map((s) => s.title || "Document")
                            .join("; ")}
                        </p>
                      )}
                    {msg.role === "assistant" && (
                      <button
                        onClick={() =>
                          isSpeaking ? stopSpeaking() : speak(msg.content, { rate: 0.9 })
                        }
                        className="mt-2 text-xs text-violet-600 dark:text-violet-400 hover:underline flex items-center gap-1"
                        aria-label={isSpeaking ? "Stop reading" : "Read aloud"}
                      >
                        {isSpeaking ? "Stop" : "Read aloud"}
                      </button>
                    )}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="bg-slate-100 dark:bg-slate-800 rounded-2xl px-4 py-3 flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin text-violet-600 dark:text-violet-400" />
                    <span className="text-slate-500 dark:text-slate-400 text-sm">
                      Tutor is thinking...
                    </span>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            <div className="border-t border-slate-200 dark:border-slate-700 pt-4">
              <div className="flex items-center gap-3">
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask a question about any subject..."
                  className="input-field flex-1"
                  aria-label="Type your question"
                  disabled={loading}
                />
                <button
                  onClick={handleSend}
                  disabled={!inputText.trim() || loading}
                  className="btn-primary px-4"
                  aria-label="Send message"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="card">
            <h2 className="text-lg font-semibold mb-3 text-slate-900 dark:text-white">
              Recent Chats
            </h2>
            {sessions.length === 0 ? (
              <p className="text-sm text-slate-500 dark:text-slate-400">No chat history yet.</p>
            ) : (
              <ul className="space-y-2">
                {sessions.slice(0, 5).map((s) => (
                  <li
                    key={s.id}
                    className="text-sm text-slate-600 dark:text-slate-400 border-b border-slate-100 dark:border-slate-700 pb-2 last:border-0"
                  >
                    Session #{s.id}
                    <span className="text-slate-400 dark:text-slate-500 ml-2 text-xs">
                      {new Date(s.created_at).toLocaleDateString()}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="card bg-violet-50 dark:bg-violet-950/50 border-violet-200 dark:border-violet-800">
            <h2 className="text-lg font-semibold text-violet-900 dark:text-violet-200 mb-2">
              Study Tips
            </h2>
            <ul className="space-y-2 text-sm text-violet-800 dark:text-violet-300">
              <li>Ask one question at a time for clearer answers</li>
              <li>Specify the subject (e.g., "In Mathematics, what is...?")</li>
              <li>Request examples: "Give me an example of..."</li>
              <li>Ask for step-by-step explanations</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
