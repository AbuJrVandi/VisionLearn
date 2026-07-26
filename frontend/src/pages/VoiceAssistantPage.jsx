import { useState, useRef, useEffect, useCallback } from "react";
import { Mic, Send, Loader2, Volume2 } from "lucide-react";
import VoiceButton from "../components/VoiceButton";
import { useSpeechRecognition } from "../hooks/useSpeechRecognition";
import { useSpeechSynthesis } from "../hooks/useSpeechSynthesis";
import { sendChatMessage, textToSpeech } from "../services/api";

export default function VoiceAssistantPage() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const {
    isListening,
    transcript,
    isSupported: sttSupported,
    startListening,
    stopListening,
    resetTranscript,
  } = useSpeechRecognition();

  const { isSpeaking, speak, stop: stopSpeaking, isSupported: ttsSupported } =
    useSpeechSynthesis();
  const audioRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleVoiceResult = (text) => {
    setInputText(text);
    resetTranscript();
  };

  const playBackendTTS = useCallback(async (text) => {
    try {
      if (isListening) stopListening();
      const blob = await textToSpeech(text);
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      audioRef.current = audio;
      await audio.play();
      audio.onended = () => URL.revokeObjectURL(url);
    } catch {
      if (ttsSupported) speak(text, { rate: 0.9 });
    }
  }, [isListening, stopListening, ttsSupported, speak]);

  const handleSend = async () => {
    const text = inputText.trim();
    if (!text || loading) return;

    const userMessage = { role: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);
    setInputText("");
    setLoading(true);

    if (isListening) stopListening();

    try {
      const data = await sendChatMessage(text, sessionId, "General");
      setSessionId(data.session_id);
      const aiMessage = { role: "assistant", content: data.response };
      setMessages((prev) => [...prev, aiMessage]);
      playBackendTTS(data.response);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I could not process your request. Please try again." },
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

  const toggleListening = () => {
    if (isListening) {
      stopListening();
    } else {
      startListening(handleVoiceResult);
    }
  };

  return (
    <section aria-labelledby="voice-heading">
      <h1 id="voice-heading" className="page-title">
        Voice Assistant
      </h1>
      <p className="page-subtitle">
        Ask a question using your voice or by typing. The AI tutor will answer
        and read the response aloud.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="card h-[500px] flex flex-col">
            <div className="flex-1 overflow-y-auto space-y-4 mb-4 p-2" role="log" aria-live="polite">
              {messages.length === 0 && (
                <div className="text-center py-12 text-slate-400 dark:text-slate-500">
                  <Mic className="w-12 h-12 mx-auto mb-3 opacity-50" />
                  <p>Tap the microphone and ask a question</p>
                  <p className="text-sm mt-1">
                    Try: "What is photosynthesis?" or "Explain fractions"
                  </p>
                </div>
              )}

              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                      msg.role === "user"
                        ? "bg-blue-600 text-white"
                        : "bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-slate-200"
                    }`}
                  >
                    <p className="leading-relaxed">{msg.content}</p>
                    {msg.role === "assistant" && ttsSupported && (
                      <button
                        onClick={() =>
                          isSpeaking ? stopSpeaking() : speak(msg.content, { rate: 0.9 })
                        }
                        className="mt-2 text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 flex items-center gap-1"
                        aria-label={isSpeaking ? "Stop reading" : "Read aloud"}
                      >
                        <Volume2 className="w-3 h-3" />
                        {isSpeaking ? "Stop" : "Read aloud"}
                      </button>
                    )}
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="bg-slate-100 dark:bg-slate-800 rounded-2xl px-4 py-3 flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin text-blue-600 dark:text-blue-400" />
                    <span className="text-slate-500 dark:text-slate-400 text-sm">Thinking...</span>
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
                  placeholder="Type or use the microphone..."
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
          <div className="card text-center">
            <h2 className="text-lg font-semibold mb-4 text-slate-900 dark:text-white">
              Voice Input
            </h2>

            <div className="flex flex-col items-center gap-4">
              <VoiceButton
                isListening={isListening}
                onClick={toggleListening}
                label={isListening ? "Stop listening" : "Start voice input"}
              />

              {!sttSupported && (
                <p className="text-sm text-amber-600 dark:text-amber-400">
                  Voice input is not supported in this browser. Please type
                  your questions instead.
                </p>
              )}

              {isListening && transcript && (
                <div
                  className="bg-blue-50 dark:bg-blue-950 rounded-xl p-3 w-full"
                  aria-live="polite"
                >
                  <p className="text-sm text-blue-800 dark:text-blue-300 italic">
                    "{transcript}"
                  </p>
                </div>
              )}

              {isSpeaking && (
                <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400">
                  <Volume2 className="w-4 h-4 animate-pulse" />
                  <span className="text-sm">Speaking...</span>
                </div>
              )}
            </div>
          </div>

          <div className="card">
            <h2 className="text-lg font-semibold mb-3 text-slate-900 dark:text-white">
              Try Asking
            </h2>
            <ul className="space-y-2">
              {[
                "What is photosynthesis?",
                "Explain fractions simply",
                "Who was Milton Margai?",
                "What is the water cycle?",
                "Help me with basic algebra",
              ].map((q) => (
                <li key={q}>
                  <button
                    onClick={() => setInputText(q)}
                    className="text-left text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 hover:underline w-full"
                  >
                    &ldquo;{q}&rdquo;
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
