import { useState, useCallback, useRef } from "react";
import { strip_markdown } from "../utils/text";

const PREFERRED_VOICES = [
  "Samantha",
  "Karen",
  "Moira",
  "Zarvox",
  "Tessa",
  "Veena",
];

export function useSpeechSynthesis() {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voices, setVoices] = useState([]);
  const utteranceRef = useRef(null);

  const isSupported =
    typeof window !== "undefined" && "speechSynthesis" in window;

  const loadVoices = useCallback(() => {
    if (!isSupported) return [];
    const available = window.speechSynthesis.getVoices();
    setVoices(available);
    return available;
  }, [isSupported]);

  const speak = useCallback(
    (text, options = {}) => {
      if (!isSupported || !text) return;

      window.speechSynthesis.cancel();

      const cleanText = strip_markdown(text);
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.rate = options.rate || 0.9;
      utterance.pitch = options.pitch || 1.0;
      utterance.volume = options.volume || 1.0;
      utterance.lang = options.lang || "en-US";

      if (options.voice) {
        utterance.voice = options.voice;
      } else {
        const preferred = voices.find((v) => PREFERRED_VOICES.includes(v.name));
        if (preferred) {
          utterance.voice = preferred;
        } else {
          const englishVoice = voices.find(
            (v) => v.lang.startsWith("en") && v.localService
          );
          if (englishVoice) utterance.voice = englishVoice;
        }
      }

      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);

      utteranceRef.current = utterance;
      window.speechSynthesis.speak(utterance);
    },
    [isSupported, voices]
  );

  const stop = useCallback(() => {
    if (isSupported) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  }, [isSupported]);

  const pause = useCallback(() => {
    if (isSupported && isSpeaking) {
      window.speechSynthesis.pause();
    }
  }, [isSupported, isSpeaking]);

  const resume = useCallback(() => {
    if (isSupported) {
      window.speechSynthesis.resume();
    }
  }, [isSupported]);

  return {
    isSpeaking,
    voices,
    isSupported,
    loadVoices,
    speak,
    stop,
    pause,
    resume,
  };
}
