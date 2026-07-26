import { useCallback, useRef, useState } from "react";
import { Upload, Camera, X } from "lucide-react";

export default function FileUpload({ onFileSelect, accept = "image/*", label }) {
  const [preview, setPreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const handleFile = useCallback(
    (file) => {
      if (!file) return;
      if (file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => setPreview(e.target.result);
        reader.readAsDataURL(file);
      } else {
        setPreview(null);
      }
      onFileSelect(file);
    },
    [onFileSelect]
  );

  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      setDragActive(false);
      if (e.dataTransfer.files?.[0]) handleFile(e.dataTransfer.files[0]);
    },
    [handleFile]
  );

  const clearPreview = () => {
    setPreview(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
          {label}
        </label>
      )}

      {preview ? (
        <div className="relative">
          <img
            src={preview}
            alt="Upload preview"
            className="w-full max-h-80 object-contain rounded-xl border border-slate-200 dark:border-slate-700"
          />
          <button
            onClick={clearPreview}
            className="absolute top-2 right-2 p-1.5 bg-white dark:bg-slate-800 rounded-full shadow-md hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
            aria-label="Remove image"
          >
            <X className="w-4 h-4 text-slate-600 dark:text-slate-300" />
          </button>
        </div>
      ) : (
        <div
          onDrop={handleDrop}
          onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
          onDragLeave={(e) => { e.preventDefault(); setDragActive(false); }}
          onClick={() => inputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-150 ${
            dragActive
              ? "border-blue-500 bg-blue-50 dark:bg-blue-950"
              : "border-slate-300 dark:border-slate-600 hover:border-blue-400 hover:bg-slate-50 dark:hover:bg-slate-800"
          }`}
          role="button"
          tabIndex={0}
          aria-label="Upload file. Click or drag and drop."
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              inputRef.current?.click();
            }
          }}
        >
          <div className="flex flex-col items-center gap-3">
            <div className="p-3 bg-blue-100 dark:bg-blue-900 rounded-full">
              {accept === "image/*" ? (
                <Camera className="w-8 h-8 text-blue-600 dark:text-blue-400" aria-hidden="true" />
              ) : (
                <Upload className="w-8 h-8 text-blue-600 dark:text-blue-400" aria-hidden="true" />
              )}
            </div>
            <div>
              <p className="text-lg font-medium text-slate-700 dark:text-slate-200">
                {accept === "image/*"
                  ? "Take a photo or upload an image"
                  : "Upload a document"}
              </p>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                PNG, JPEG, WebP up to 10 MB
              </p>
            </div>
          </div>
        </div>
      )}

      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={(e) => handleFile(e.target.files?.[0])}
        className="hidden"
        aria-hidden="true"
      />
    </div>
  );
}
