import { Play, Pause, Square, Volume2 } from "lucide-react";
import { useSpeechSynthesis } from "../hooks/useSpeechSynthesis";

export default function TTSPlayer({ text, className = "" }) {
  const { isSpeaking, isSupported, speak, stop, pause } = useSpeechSynthesis();

  if (!text || !isSupported) return null;

  const handleToggle = () => {
    if (isSpeaking) {
      pause();
    } else {
      speak(text, { rate: 0.9 });
    }
  };

  return (
    <div
      className={`flex items-center gap-2 bg-slate-50 dark:bg-slate-800 rounded-xl px-4 py-2 ${className}`}
      role="region"
      aria-label="Text to speech player"
    >
      <Volume2 className="w-4 h-4 text-blue-600 dark:text-blue-400" aria-hidden="true" />
      <button
        onClick={handleToggle}
        className="p-2 rounded-lg bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-blue-800 transition-colors"
        aria-label={isSpeaking ? "Pause reading" : "Read aloud"}
      >
        {isSpeaking ? (
          <Pause className="w-4 h-4" aria-hidden="true" />
        ) : (
          <Play className="w-4 h-4" aria-hidden="true" />
        )}
      </button>
      {isSpeaking && (
        <button
          onClick={stop}
          className="p-2 rounded-lg bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 hover:bg-red-200 dark:hover:bg-red-800 transition-colors"
          aria-label="Stop reading"
        >
          <Square className="w-4 h-4" aria-hidden="true" />
        </button>
      )}
      <span className="text-xs text-slate-500 dark:text-slate-400">
        {isSpeaking ? "Reading..." : "Click to read aloud"}
      </span>
    </div>
  );
}
