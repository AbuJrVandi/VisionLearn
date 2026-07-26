export function strip_markdown(text) {
  if (!text) return "";

  let cleaned = text;

  cleaned = cleaned.replace(/#{1,6}\s*/g, "");

  cleaned = cleaned.replace(/\*\*(.+?)\*\*/g, "$1");
  cleaned = cleaned.replace(/\*(.+?)\*/g, "$1");
  cleaned = cleaned.replace(/__(.+?)__/g, "$1");
  cleaned = cleaned.replace(/_(.+?)_/g, "$1");

  cleaned = cleaned.replace(/`(.+?)`/g, "$1");
  cleaned = cleaned.replace(/```[\s\S]*?```/g, "");

  cleaned = cleaned.replace(/\[(.+?)\]\(.+?\)/g, "$1");

  cleaned = cleaned.replace(/^[\-\*\+]\s+/gm, "");
  cleaned = cleaned.replace(/^\d+\.\s+/gm, "");

  cleaned = cleaned.replace(/^>\s?/gm, "");

  cleaned = cleaned.replace(/---+/g, "");
  cleaned = cleaned.replace(/\*\*\*+/g, "");

  cleaned = cleaned.replace(/\n{3,}/g, "\n\n");

  return cleaned.trim();
}
