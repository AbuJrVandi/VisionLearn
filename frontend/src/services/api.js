const API_BASE = import.meta.env.VITE_API_URL || "https://visionlearn.onrender.com";

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: {},
    ...options,
  };

  if (config.body && !(config.body instanceof FormData)) {
    config.headers["Content-Type"] = "application/json";
    config.body = JSON.stringify(config.body);
  }

  const response = await fetch(url, config);

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(errorData.detail || `HTTP ${response.status}`);
  }

  return response;
}

export async function uploadDocument(file, subject = "General") {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("subject", subject);

  const response = await request("/documents/upload", { method: "POST", body: formData });
  return response.json();
}

export async function processOCR(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await request("/documents/ocr", { method: "POST", body: formData });
  return response.json();
}

export async function listDocuments(subject = null) {
  const params = subject ? `?subject=${encodeURIComponent(subject)}` : "";
  const response = await request(`/documents/list${params}`);
  return response.json();
}

export async function getDocument(docId) {
  const response = await request(`/documents/${docId}`);
  return response.json();
}

export async function deleteDocument(docId) {
  const response = await request(`/documents/${docId}`, { method: "DELETE" });
  return response.json();
}

export async function textToSpeech(text, lang = "en", slow = false) {
  const formData = new FormData();
  formData.append("text", text);
  formData.append("lang", lang);
  formData.append("slow", slow);

  const response = await request("/voice/tts", { method: "POST", body: formData });
  return response.blob();
}

export async function speechToText(audioBlob) {
  const formData = new FormData();
  formData.append("file", audioBlob, "recording.wav");

  const response = await request("/voice/stt", { method: "POST", body: formData });
  return response.json();
}

export async function sendChatMessage(message, sessionId = null, subject = "General") {
  const response = await request("/chat/send", {
    method: "POST",
    body: { message, session_id: sessionId, subject },
  });
  return response.json();
}

export async function getChatSessions() {
  const response = await request("/chat/sessions");
  return response.json();
}

export async function getChatMessages(sessionId) {
  const response = await request(`/chat/sessions/${sessionId}/messages`);
  return response.json();
}

export async function getAnalytics() {
  const response = await request("/chat/analytics");
  return response.json();
}

export async function healthCheck() {
  const response = await request("/health");
  return response.json();
}
