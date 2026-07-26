import { Link } from "react-router-dom";
import {
  ScanText,
  Mic,
  MessageSquare,
  BookOpen,
  BarChart3,
  ArrowRight,
} from "lucide-react";

const FEATURES = [
  {
    to: "/scanner",
    icon: ScanText,
    title: "Document Scanner",
    description: "Take a photo of any text and hear it read aloud instantly.",
    color: "bg-blue-50 dark:bg-blue-950 text-blue-600 dark:text-blue-400",
    ring: "group-hover:ring-blue-200 dark:group-hover:ring-blue-800",
  },
  {
    to: "/voice",
    icon: Mic,
    title: "Voice Assistant",
    description: "Ask questions using your voice and get spoken answers.",
    color: "bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400",
    ring: "group-hover:ring-emerald-200 dark:group-hover:ring-emerald-800",
  },
  {
    to: "/chat",
    icon: MessageSquare,
    title: "AI Tutor",
    description: "Chat with an AI tutor for help with any school subject.",
    color: "bg-violet-50 dark:bg-violet-950 text-violet-600 dark:text-violet-400",
    ring: "group-hover:ring-violet-200 dark:group-hover:ring-violet-800",
  },
  {
    to: "/library",
    icon: BookOpen,
    title: "Document Library",
    description: "Upload, organise, and read your learning materials.",
    color: "bg-amber-50 dark:bg-amber-950 text-amber-600 dark:text-amber-400",
    ring: "group-hover:ring-amber-200 dark:group-hover:ring-amber-800",
  },
  {
    to: "/analytics",
    icon: BarChart3,
    title: "Learning Progress",
    description: "Track your study activity and progress over time.",
    color: "bg-rose-50 dark:bg-rose-950 text-rose-600 dark:text-rose-400",
    ring: "group-hover:ring-rose-200 dark:group-hover:ring-rose-800",
  },
];

export default function HomePage() {
  return (
    <section aria-labelledby="home-heading">
      <div className="mb-10">
        <h1 id="home-heading" className="page-title text-4xl md:text-5xl">
          Welcome to VisionLearn
        </h1>
        <p className="page-subtitle max-w-2xl">
          Your AI-powered learning companion. Scan documents, ask questions
          with your voice, and study independently.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {FEATURES.map(({ to, icon: Icon, title, description, color, ring }) => (
          <Link
            key={to}
            to={to}
            className={`card group relative overflow-hidden ring-2 ring-transparent hover:shadow-lg transition-all duration-200 ${ring}`}
          >
            <div
              className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${color}`}
            >
              <Icon
                className="w-6 h-6 group-hover:scale-110 transition-transform duration-200"
                aria-hidden="true"
              />
            </div>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
              {title}
            </h2>
            <p className="text-slate-500 dark:text-slate-400 text-sm leading-relaxed">
              {description}
            </p>
            <ArrowRight
              className="absolute right-4 bottom-6 w-4 h-4 text-slate-300 dark:text-slate-600 group-hover:text-blue-500 group-hover:translate-x-1 transition-all duration-200"
              aria-hidden="true"
            />
          </Link>
        ))}
      </div>

      <div className="mt-12 card bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/50 dark:to-indigo-950/50 border-blue-200 dark:border-blue-800">
        <h2 className="text-lg font-semibold text-blue-900 dark:text-blue-200 mb-3">
          Getting Started
        </h2>
        <ol className="space-y-2 text-blue-800 dark:text-blue-300 text-sm list-decimal list-inside">
          <li>
            Use the <strong>Document Scanner</strong> to photograph and read any
            printed text.
          </li>
          <li>
            Try the <strong>Voice Assistant</strong> to ask questions out loud.
          </li>
          <li>
            Explore the <strong>AI Tutor</strong> for detailed explanations on
            any topic.
          </li>
          <li>
            Upload materials to your <strong>Library</strong> for easy access.
          </li>
        </ol>
      </div>
    </section>
  );
}
