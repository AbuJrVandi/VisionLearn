import { useState, useEffect } from "react";
import {
  BookOpen,
  Trash2,
  Search,
  FileText,
  Image,
  File,
  Loader2,
  ChevronDown,
  ChevronUp,
  Volume2,
} from "lucide-react";
import FileUpload from "../components/FileUpload";
import TTSPlayer from "../components/TTSPlayer";
import { uploadDocument, listDocuments, deleteDocument } from "../services/api";
import { strip_markdown } from "../utils/text";

const SUBJECTS = [
  "General",
  "Mathematics",
  "Science",
  "English",
  "Social Studies",
  "Vocational",
];

function FileTypeIcon({ fileType, className = "" }) {
  if (fileType?.startsWith("image/")) {
    return <Image className={`w-5 h-5 ${className}`} />;
  }
  if (fileType === "application/pdf") {
    return <FileText className={`w-5 h-5 text-red-500 ${className}`} />;
  }
  if (fileType?.includes("word") || fileType?.includes("document")) {
    return <FileText className={`w-5 h-5 text-blue-500 ${className}`} />;
  }
  return <File className={`w-5 h-5 ${className}`} />;
}

function FileBadge({ fileType }) {
  if (fileType?.startsWith("image/")) return null;
  if (fileType === "application/pdf") {
    return (
      <span className="text-[10px] font-bold uppercase px-1.5 py-0.5 rounded bg-red-100 dark:bg-red-900 text-red-600 dark:text-red-400">
        PDF
      </span>
    );
  }
  if (fileType?.includes("word") || fileType?.includes("document")) {
    return (
      <span className="text-[10px] font-bold uppercase px-1.5 py-0.5 rounded bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400">
        DOCX
      </span>
    );
  }
  if (fileType === "text/plain") {
    return (
      <span className="text-[10px] font-bold uppercase px-1.5 py-0.5 rounded bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400">
        TXT
      </span>
    );
  }
  return null;
}

export default function LibraryPage() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [filterSubject, setFilterSubject] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [error, setError] = useState(null);
  const [showSummary, setShowSummary] = useState(false);

  useEffect(() => {
    loadDocuments();
  }, [filterSubject]);

  const loadDocuments = async () => {
    setLoading(true);
    try {
      const data = await listDocuments(filterSubject);
      setDocuments(data.documents || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (file) => {
    if (!file) return;
    setUploading(true);
    setError(null);
    try {
      await uploadDocument(file, "General");
      await loadDocuments();
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (docId) => {
    if (!window.confirm("Delete this document?")) return;
    try {
      await deleteDocument(docId);
      setDocuments((prev) => prev.filter((d) => d.id !== docId));
      if (selectedDoc?.id === docId) setSelectedDoc(null);
    } catch (err) {
      setError(err.message);
    }
  };

  const filteredDocs = documents.filter((doc) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      doc.original_name?.toLowerCase().includes(q) ||
      doc.subject?.toLowerCase().includes(q)
    );
  });

  const formatSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const hasExtractableText = (doc) => {
    return doc.file_type?.startsWith("image/") ||
      doc.file_type === "application/pdf" ||
      doc.file_type?.includes("word") ||
      doc.file_type?.includes("document") ||
      doc.file_type === "text/plain";
  };

  return (
    <section aria-labelledby="library-heading">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-10 h-10 rounded-xl bg-amber-50 dark:bg-amber-950 flex items-center justify-center">
          <BookOpen className="w-5 h-5 text-amber-600 dark:text-amber-400" aria-hidden="true" />
        </div>
        <h1 id="library-heading" className="page-title mb-0">
          Document Library
        </h1>
      </div>
      <p className="page-subtitle">
        Upload PDFs, Word documents, or images. Text is extracted automatically and can be read aloud.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-4">
          <div className="card">
            <h2 className="text-lg font-semibold mb-3 text-slate-900 dark:text-white">
              Upload Document
            </h2>
            <FileUpload
              onFileSelect={handleUpload}
              accept="image/*,.pdf,.txt,.doc,.docx"
            />
            <p className="mt-3 text-xs text-slate-400 dark:text-slate-500">
              Supported: PDF, Word (.docx), Text, Images (PNG, JPEG, WebP)
            </p>
            {uploading && (
              <div className="mt-3 flex items-center gap-2 text-blue-600 dark:text-blue-400" role="status">
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-sm">Uploading and extracting text...</span>
              </div>
            )}
          </div>

          <div className="card">
            <h2 className="text-lg font-semibold mb-3 text-slate-900 dark:text-white">
              Filter
            </h2>
            <div className="space-y-3">
              <div>
                <label className="text-sm text-slate-600 dark:text-slate-400 block mb-1">
                  Search
                </label>
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search documents..."
                    className="input-field pl-10 text-sm"
                    aria-label="Search documents"
                  />
                </div>
              </div>
              <div>
                <label className="text-sm text-slate-600 dark:text-slate-400 block mb-1">
                  Subject
                </label>
                <select
                  value={filterSubject || ""}
                  onChange={(e) => setFilterSubject(e.target.value || null)}
                  className="input-field text-sm"
                  aria-label="Filter by subject"
                >
                  <option value="">All Subjects</option>
                  {SUBJECTS.map((s) => (
                    <option key={s} value={s}>
                      {s}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2 space-y-4">
          {error && (
            <div className="card bg-red-50 dark:bg-red-950 border-red-200 dark:border-red-800 text-red-800 dark:text-red-300" role="alert">
              {error}
            </div>
          )}

          {loading ? (
            <div className="card text-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-slate-400 mx-auto" />
              <p className="text-slate-500 dark:text-slate-400 mt-3">Loading documents...</p>
            </div>
          ) : filteredDocs.length === 0 ? (
            <div className="card text-center py-12 bg-slate-50 dark:bg-slate-800/50">
              <FileText className="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
              <p className="text-slate-500 dark:text-slate-400">
                {documents.length === 0
                  ? "No documents yet. Upload your first document above."
                  : "No documents match your search."}
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              <p className="text-sm text-slate-500 dark:text-slate-400">
                {filteredDocs.length} document{filteredDocs.length !== 1 ? "s" : ""}
              </p>

              {filteredDocs.map((doc) => (
                <div
                  key={doc.id}
                  className={`card cursor-pointer transition-all duration-150 ${
                    selectedDoc?.id === doc.id
                      ? "ring-2 ring-blue-500 bg-blue-50 dark:bg-blue-950"
                      : "hover:bg-slate-50 dark:hover:bg-slate-800"
                  }`}
                  onClick={() => {
                    setSelectedDoc(doc);
                    setShowSummary(false);
                  }}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      setSelectedDoc(doc);
                      setShowSummary(false);
                    }
                  }}
                  aria-label={`Document: ${doc.original_name}`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start gap-3">
                      <div className="p-2 bg-slate-100 dark:bg-slate-800 rounded-lg">
                        <FileTypeIcon fileType={doc.file_type} className="text-slate-600 dark:text-slate-400" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="font-medium text-slate-900 dark:text-white">
                            {doc.original_name}
                          </h3>
                          <FileBadge fileType={doc.file_type} />
                        </div>
                        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
                          {doc.subject} &middot; {formatSize(doc.file_size)} &middot;{" "}
                          {new Date(doc.created_at).toLocaleDateString()}
                        </p>
                        {doc.extracted_text && (
                          <p className="text-xs text-emerald-600 dark:text-emerald-400 mt-1">
                            Text extracted ({doc.extracted_text.split(/\s+/).length} words)
                          </p>
                        )}
                      </div>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDelete(doc.id);
                      }}
                      className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-950 rounded-lg transition-colors"
                      aria-label={`Delete ${doc.original_name}`}
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {selectedDoc && (
            <div className="card">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <FileTypeIcon fileType={selectedDoc.file_type} className="text-slate-600 dark:text-slate-400" />
                  <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
                    {selectedDoc.original_name}
                  </h2>
                </div>
                <FileBadge fileType={selectedDoc.file_type} />
              </div>

              {selectedDoc.summary && (
                <div className="mb-4">
                  <button
                    onClick={() => setShowSummary(!showSummary)}
                    className="flex items-center gap-2 text-sm font-medium text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 mb-2"
                    aria-expanded={showSummary}
                  >
                    <Volume2 className="w-4 h-4" />
                    AI Summary
                    {showSummary ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </button>
                  {showSummary && (
                    <div className="bg-blue-50 dark:bg-blue-950/50 border border-blue-200 dark:border-blue-800 rounded-xl p-4">
                      <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                        {strip_markdown(selectedDoc.summary)}
                      </p>
                      <div className="mt-3">
                        <TTSPlayer text={selectedDoc.summary} />
                      </div>
                    </div>
                  )}
                </div>
              )}

              {selectedDoc.extracted_text && (
                <div>
                  <h3 className="text-sm font-medium text-slate-600 dark:text-slate-400 mb-2">
                    Extracted Text
                  </h3>
                  <div className="bg-slate-50 dark:bg-slate-800 rounded-xl p-4 max-h-64 overflow-y-auto mb-4">
                    <p className="text-slate-800 dark:text-slate-200 text-sm leading-relaxed whitespace-pre-wrap">
                      {strip_markdown(selectedDoc.extracted_text)}
                    </p>
                  </div>
                  <TTSPlayer text={selectedDoc.extracted_text} />
                </div>
              )}

              {selectedDoc.file_type?.startsWith("image/") && !selectedDoc.extracted_text && (
                <div className="text-center py-8 text-slate-500 dark:text-slate-400">
                  <Image className="w-10 h-10 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">No text was detected in this image.</p>
                </div>
              )}

              {!selectedDoc.extracted_text && !selectedDoc.file_type?.startsWith("image/") && (
                <div className="text-center py-8 text-slate-500 dark:text-slate-400">
                  <FileText className="w-10 h-10 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">No text could be extracted from this file.</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
