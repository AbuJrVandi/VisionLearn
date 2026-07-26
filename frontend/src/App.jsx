import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import HomePage from "./pages/HomePage";
import ScannerPage from "./pages/ScannerPage";
import VoiceAssistantPage from "./pages/VoiceAssistantPage";
import ChatTutorPage from "./pages/ChatTutorPage";
import LibraryPage from "./pages/LibraryPage";
import AnalyticsPage from "./pages/AnalyticsPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/scanner" element={<ScannerPage />} />
          <Route path="/voice" element={<VoiceAssistantPage />} />
          <Route path="/chat" element={<ChatTutorPage />} />
          <Route path="/library" element={<LibraryPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
