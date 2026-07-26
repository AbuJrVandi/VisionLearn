import { NavLink, Outlet } from "react-router-dom";
import {
  Home,
  ScanText,
  Mic,
  MessageSquare,
  BookOpen,
  BarChart3,
  Sun,
  Moon,
  Minus,
  Plus,
  Volume2,
} from "lucide-react";
import { useAccessibility } from "../hooks/useAccessibility";

const NAV_ITEMS = [
  { to: "/", icon: Home, label: "Home" },
  { to: "/scanner", icon: ScanText, label: "Scanner" },
  { to: "/voice", icon: Mic, label: "Voice" },
  { to: "/chat", icon: MessageSquare, label: "AI Tutor" },
  { to: "/library", icon: BookOpen, label: "Library" },
  { to: "/analytics", icon: BarChart3, label: "Progress" },
];

export default function Layout() {
  const {
    fontLabel,
    darkMode,
    canIncrease,
    canDecrease,
    increaseFontSize,
    decreaseFontSize,
    toggleDarkMode,
  } = useAccessibility();

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 transition-colors duration-200">
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      <header className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 px-4 py-3 sticky top-0 z-40 transition-colors duration-200">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center shadow-sm">
              <Volume2 className="w-5 h-5 text-white" aria-hidden="true" />
            </div>
            <h1 className="text-xl font-bold text-slate-900 dark:text-white tracking-tight">
              VisionLearn
            </h1>
          </div>

          <nav
            className="hidden md:flex items-center gap-1"
            aria-label="Main navigation"
          >
            {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                    isActive
                      ? "bg-blue-50 text-blue-700 dark:bg-blue-950 dark:text-blue-400"
                      : "text-slate-500 hover:bg-slate-100 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white"
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <Icon className="w-4 h-4" aria-hidden="true" />
                    <span>{label}</span>
                    {isActive && <span className="sr-only">(current page)</span>}
                  </>
                )}
              </NavLink>
            ))}
          </nav>

          <div className="flex items-center gap-1">
            <button
              onClick={decreaseFontSize}
              disabled={!canDecrease}
              className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 dark:text-slate-400 disabled:opacity-30 transition-colors"
              aria-label="Decrease text size"
              title="Decrease text size"
            >
              <Minus className="w-4 h-4" />
            </button>
            <span className="text-xs font-medium text-slate-500 dark:text-slate-400 w-14 text-center select-none" aria-live="polite">
              {fontLabel}
            </span>
            <button
              onClick={increaseFontSize}
              disabled={!canIncrease}
              className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 dark:text-slate-400 disabled:opacity-30 transition-colors"
              aria-label="Increase text size"
              title="Increase text size"
            >
              <Plus className="w-4 h-4" />
            </button>

            <div className="w-px h-6 bg-slate-200 dark:bg-slate-700 mx-1" />

            <button
              onClick={toggleDarkMode}
              className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 dark:text-slate-400 transition-colors"
              aria-label={`Switch to ${darkMode ? "light" : "dark"} mode`}
              title={`Switch to ${darkMode ? "light" : "dark"} mode`}
            >
              {darkMode ? (
                <Sun className="w-5 h-5" />
              ) : (
                <Moon className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>
      </header>

      <main id="main-content" className="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full">
        <Outlet />
      </main>

      <footer className="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 mt-auto transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 py-8 md:py-10 text-center">
          <p className="text-sm font-semibold text-slate-800 dark:text-slate-200 tracking-wide">
            Developed by Alusine Manasary
          </p>
          <p className="mt-2 text-xs leading-relaxed text-slate-500 dark:text-slate-400 max-w-2xl mx-auto">
            Applying Artificial Intelligence (AI) Solutions for Empowering Visually
            Impaired Students: A Case Study of Milton Margai School for the Blind,
            Sierra Leone
          </p>
          <div className="mt-4 flex items-center justify-center gap-2 text-xs text-slate-400 dark:text-slate-500">
            <span className="w-8 h-px bg-slate-300 dark:bg-slate-700" />
            <span>VisionLearn</span>
            <span className="w-8 h-px bg-slate-300 dark:bg-slate-700" />
          </div>
        </div>
      </footer>

      <nav
        className="md:hidden fixed bottom-0 left-0 right-0 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border-t border-slate-200 dark:border-slate-800 z-40 transition-colors duration-200"
        aria-label="Mobile navigation"
      >
        <div className="flex justify-around py-2">
          {NAV_ITEMS.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex flex-col items-center gap-1 px-2 py-1 text-xs transition-colors ${
                  isActive
                    ? "text-blue-600 dark:text-blue-400"
                    : "text-slate-400 dark:text-slate-500"
                }`
              }
            >
              <Icon className="w-5 h-5" aria-hidden="true" />
              <span>{label}</span>
            </NavLink>
          ))}
        </div>
      </nav>
    </div>
  );
}
