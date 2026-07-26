import { Mic, Square } from "lucide-react";
import clsx from "clsx";

export default function VoiceButton({ isListening, onClick, size = "lg", label }) {
  const sizeClasses = {
    sm: "w-12 h-12",
    md: "w-16 h-16",
    lg: "w-20 h-20",
  };

  const iconSize = {
    sm: "w-5 h-5",
    md: "w-6 h-6",
    lg: "w-8 h-8",
  };

  return (
    <button
      onClick={onClick}
      className={clsx(
        "rounded-full flex items-center justify-center transition-all duration-200 shadow-lg",
        sizeClasses[size],
        isListening
          ? "bg-red-500 text-white hover:bg-red-600 animate-pulse"
          : "bg-blue-600 text-white hover:bg-blue-700 hover:shadow-xl"
      )}
      aria-label={isListening ? "Stop listening" : label || "Start voice input"}
      aria-pressed={isListening}
    >
      {isListening ? (
        <Square className={iconSize[size]} aria-hidden="true" />
      ) : (
        <Mic className={iconSize[size]} aria-hidden="true" />
      )}
    </button>
  );
}
