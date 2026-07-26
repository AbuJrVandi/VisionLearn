import { useState, useEffect, useCallback } from "react";

const FONT_SIZES = [
  { label: "Small", value: "14px" },
  { label: "Normal", value: "16px" },
  { label: "Large", value: "18px" },
  { label: "X-Large", value: "22px" },
  { label: "XX-Large", value: "26px" },
];
const STORAGE_KEY_FONT = "visionlearn_font_index";
const STORAGE_KEY_DARK = "visionlearn_dark_mode";

export function useAccessibility() {
  const [fontSizeIndex, setFontSizeIndex] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY_FONT);
    return saved !== null ? parseInt(saved, 10) : 1;
  });

  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY_DARK);
    if (saved !== null) return saved === "true";
    return window.matchMedia?.("(prefers-color-scheme: dark)").matches;
  });

  useEffect(() => {
    document.documentElement.style.setProperty(
      "--font-size-base",
      FONT_SIZES[fontSizeIndex].value
    );
    localStorage.setItem(STORAGE_KEY_FONT, String(fontSizeIndex));
  }, [fontSizeIndex]);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
    localStorage.setItem(STORAGE_KEY_DARK, String(darkMode));
  }, [darkMode]);

  const increaseFontSize = useCallback(() => {
    setFontSizeIndex((prev) => Math.min(prev + 1, FONT_SIZES.length - 1));
  }, []);

  const decreaseFontSize = useCallback(() => {
    setFontSizeIndex((prev) => Math.max(prev - 1, 0));
  }, []);

  const toggleDarkMode = useCallback(() => {
    setDarkMode((prev) => !prev);
  }, []);

  const fontSize = FONT_SIZES[fontSizeIndex].value;
  const fontLabel = FONT_SIZES[fontSizeIndex].label;
  const canIncrease = fontSizeIndex < FONT_SIZES.length - 1;
  const canDecrease = fontSizeIndex > 0;

  return {
    fontSize,
    fontLabel,
    darkMode,
    canIncrease,
    canDecrease,
    increaseFontSize,
    decreaseFontSize,
    toggleDarkMode,
  };
}
