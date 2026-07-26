import { useState } from "react";
import { ScanText, Loader2, AlertCircle, CheckCircle } from "lucide-react";
import FileUpload from "../components/FileUpload";
import TTSPlayer from "../components/TTSPlayer";
import { processOCR } from "../services/api";

export default function ScannerPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileSelect = async (file) => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await processOCR(file);
      setResult(data);
      if (!data.success) {
        setError(data.error || "Could not extract text from this image.");
      }
    } catch (err) {
      setError(err.message || "Failed to process image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section aria-labelledby="scanner-heading">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950 flex items-center justify-center">
          <ScanText className="w-5 h-5 text-blue-600 dark:text-blue-400" aria-hidden="true" />
        </div>
        <h1 id="scanner-heading" className="page-title mb-0">
          Document Scanner
        </h1>
      </div>
      <p className="page-subtitle">
        Take a photo or upload an image of text. The system will extract the
        text and read it aloud for you.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="card">
            <h2 className="text-lg font-semibold mb-4 text-slate-900 dark:text-white">
              Upload Image
            </h2>
            <FileUpload onFileSelect={handleFileSelect} accept="image/*" />
            <p className="mt-4 text-xs text-slate-400 dark:text-slate-500">
              Tip: Hold the camera steady and ensure good lighting for best
              results.
            </p>
          </div>

          {loading && (
            <div className="card flex items-center gap-3" role="status">
              <Loader2 className="w-6 h-6 text-blue-600 dark:text-blue-400 animate-spin" />
              <span className="text-slate-600 dark:text-slate-300">Processing image...</span>
            </div>
          )}

          {error && (
            <div
              className="card bg-red-50 dark:bg-red-950 border-red-200 dark:border-red-800 flex items-start gap-3"
              role="alert"
            >
              <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 mt-0.5 shrink-0" />
              <div>
                <p className="font-medium text-red-800 dark:text-red-300">Error</p>
                <p className="text-red-700 dark:text-red-400 text-sm">{error}</p>
              </div>
            </div>
          )}
        </div>

        <div className="space-y-6">
          {result && result.success && (
            <div className="card">
              <div className="flex items-center gap-2 mb-3">
                <CheckCircle className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
                <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
                  Extracted Text
                </h2>
              </div>

              <div className="flex items-center gap-4 text-sm text-slate-500 dark:text-slate-400 mb-4">
                <span>Words: {result.word_count}</span>
                <span>Confidence: {result.confidence}%</span>
              </div>

              <div
                className="bg-slate-50 dark:bg-slate-800 rounded-xl p-4 max-h-64 overflow-y-auto"
                aria-live="polite"
              >
                <p className="text-slate-800 dark:text-slate-200 leading-relaxed whitespace-pre-wrap">
                  {result.text}
                </p>
              </div>

              <div className="mt-4">
                <TTSPlayer text={result.text} />
              </div>
            </div>
          )}

          {result && !result.success && !error && (
            <div className="card bg-amber-50 dark:bg-amber-950 border-amber-200 dark:border-amber-800">
              <p className="text-amber-800 dark:text-amber-300">
                No text could be detected in this image. Try using a clearer
                image with visible text.
              </p>
            </div>
          )}

          {!result && !loading && (
            <div className="card bg-slate-50 dark:bg-slate-800/50 text-center py-12">
              <ScanText className="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
              <p className="text-slate-500 dark:text-slate-400">
                Upload an image to see extracted text here
              </p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
