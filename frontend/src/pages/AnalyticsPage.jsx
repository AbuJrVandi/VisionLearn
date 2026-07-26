import { useState, useEffect } from "react";
import {
  BarChart3,
  FileText,
  MessageSquare,
  ScanText,
  Mic,
  BookOpen,
  TrendingUp,
  Clock,
  Activity,
  Upload,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  Legend,
} from "recharts";
import { getAnalytics } from "../services/api";
import { useAccessibility } from "../hooks/useAccessibility";

const ACTION_CONFIG = {
  ocr: { icon: ScanText, label: "Scans", color: "#3b82f6" },
  tts: { icon: FileText, label: "Read Aloud", color: "#10b981" },
  stt: { icon: Mic, label: "Voice Input", color: "#f59e0b" },
  chat: { icon: MessageSquare, label: "AI Chat", color: "#8b5cf6" },
  upload: { icon: Upload, label: "Uploads", color: "#ef4444" },
};

const PIE_COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ef4444", "#06b6d4"];

const DAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function formatHour(h) {
  const hour = parseInt(h, 10);
  if (hour === 0) return "12am";
  if (hour < 12) return `${hour}am`;
  if (hour === 12) return "12pm";
  return `${hour - 12}pm`;
}

function ChartTooltip({ active, payload, label, darkMode }) {
  if (!active || !payload?.length) return null;
  return (
    <div
      className="rounded-xl shadow-lg px-4 py-3 text-sm"
      style={{
        backgroundColor: darkMode ? "#1e293b" : "#ffffff",
        border: `1px solid ${darkMode ? "#334155" : "#e2e8f0"}`,
      }}
    >
      <p className="font-semibold mb-1" style={{ color: darkMode ? "#f1f5f9" : "#0f172a" }}>
        {label}
      </p>
      {payload.map((entry, i) => (
        <p key={i} style={{ color: darkMode ? "#cbd5e1" : "#475569" }}>
          <span
            className="inline-block w-2.5 h-2.5 rounded-full mr-2"
            style={{ backgroundColor: entry.color }}
          />
          {entry.name}: <span className="font-medium">{entry.value}</span>
        </p>
      ))}
    </div>
  );
}

function StatCard({ icon: Icon, label, value, color, bg }) {
  return (
    <div className="card flex items-center gap-4">
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 ${bg}`}>
        <Icon className={`w-6 h-6 ${color}`} aria-hidden="true" />
      </div>
      <div>
        <p className="text-2xl font-bold text-slate-900 dark:text-white">{value}</p>
        <p className="text-xs text-slate-500 dark:text-slate-400">{label}</p>
      </div>
    </div>
  );
}

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const { darkMode } = useAccessibility();

  const gridColor = darkMode ? "#1e293b" : "#f1f5f9";
  const tickColor = darkMode ? "#64748b" : "#94a3b8";
  const labelColor = darkMode ? "#94a3b8" : "#64748b";

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const data = await getAnalytics();
      setAnalytics(data);
    } catch {
      setAnalytics({
        action_counts: {},
        total_documents: 0,
        total_chat_sessions: 0,
        recent_activity: [],
        daily_activity: [],
        hourly_activity: [],
        subject_distribution: [],
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-20">
        <BarChart3 className="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-3 animate-pulse" />
        <p className="text-slate-500 dark:text-slate-400">Loading analytics...</p>
      </div>
    );
  }

  const actions = analytics?.action_counts || {};
  const totalActions = Object.values(actions).reduce((sum, v) => sum + v, 0);

  const featureData = Object.entries(ACTION_CONFIG).map(([key, cfg]) => ({
    name: cfg.label,
    count: actions[key] || 0,
    fill: cfg.color,
  }));

  const dailyData = buildDailyData(analytics?.daily_activity || []);
  const hourlyData = buildHourlyData(analytics?.hourly_activity || []);
  const subjectData = (analytics?.subject_distribution || []).map((s) => ({
    name: s.subject || "General",
    value: s.count,
  }));

  return (
    <section aria-labelledby="analytics-heading">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-10 h-10 rounded-xl bg-rose-50 dark:bg-rose-950 flex items-center justify-center">
          <BarChart3 className="w-5 h-5 text-rose-600 dark:text-rose-400" aria-hidden="true" />
        </div>
        <h1 id="analytics-heading" className="page-title mb-0">
          Learning Progress
        </h1>
      </div>
      <p className="page-subtitle">
        Track your study activity and how you use VisionLearn.
      </p>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatCard icon={Activity} label="Total Activities" value={totalActions} color="text-blue-600 dark:text-blue-400" bg="bg-blue-50 dark:bg-blue-950" />
        <StatCard icon={BookOpen} label="Documents" value={analytics?.total_documents || 0} color="text-amber-600 dark:text-amber-400" bg="bg-amber-50 dark:bg-amber-950" />
        <StatCard icon={MessageSquare} label="Chat Sessions" value={analytics?.total_chat_sessions || 0} color="text-violet-600 dark:text-violet-400" bg="bg-violet-50 dark:bg-violet-950" />
        <StatCard icon={ScanText} label="Text Scans" value={actions.ocr || 0} color="text-emerald-600 dark:text-emerald-400" bg="bg-emerald-50 dark:bg-emerald-950" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="lg:col-span-2 card">
          <div className="flex items-center gap-2 mb-6">
            <TrendingUp className="w-4 h-4 text-slate-400" />
            <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-200 uppercase tracking-wide">
              Daily Activity — Last 7 Days
            </h2>
          </div>
          {dailyData.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={dailyData} barGap={2}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} vertical={false} />
                <XAxis dataKey="day" tick={{ fontSize: 12, fill: tickColor }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 12, fill: tickColor }} axisLine={false} tickLine={false} allowDecimals={false} />
                <Tooltip content={<ChartTooltip darkMode={darkMode} />} />
                <Legend wrapperStyle={{ fontSize: 12, paddingTop: 8, color: labelColor }} />
                <Bar dataKey="Scans" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="AI Chat" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Uploads" fill="#ef4444" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Read Aloud" fill="#10b981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Voice Input" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <EmptyChart message="No activity recorded yet" />
          )}
        </div>

        <div className="card">
          <div className="flex items-center gap-2 mb-6">
            <BookOpen className="w-4 h-4 text-slate-400" />
            <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-200 uppercase tracking-wide">
              Subject Distribution
            </h2>
          </div>
          {subjectData.length > 0 ? (
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={subjectData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={4}
                  dataKey="value"
                  strokeWidth={0}
                >
                  {subjectData.map((_, i) => (
                    <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip
                  content={({ active, payload }) => {
                    if (!active || !payload?.length) return null;
                    return (
                      <div
                        className="rounded-xl shadow-lg px-4 py-3 text-sm"
                        style={{
                          backgroundColor: darkMode ? "#1e293b" : "#ffffff",
                          border: `1px solid ${darkMode ? "#334155" : "#e2e8f0"}`,
                        }}
                      >
                        <p className="font-semibold" style={{ color: darkMode ? "#f1f5f9" : "#0f172a" }}>
                          {payload[0].name}: {payload[0].value}
                        </p>
                      </div>
                    );
                  }}
                />
                <Legend
                  verticalAlign="bottom"
                  height={36}
                  formatter={(value) => (
                    <span style={{ color: darkMode ? "#94a3b8" : "#64748b", fontSize: 12 }}>
                      {value}
                    </span>
                  )}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <EmptyChart message="No documents uploaded yet" />
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="card">
          <div className="flex items-center gap-2 mb-6">
            <Clock className="w-4 h-4 text-slate-400" />
            <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-200 uppercase tracking-wide">
              Activity by Time of Day
            </h2>
          </div>
          {hourlyData.some((d) => d.count > 0) ? (
            <ResponsiveContainer width="100%" height={240}>
              <AreaChart data={hourlyData}>
                <defs>
                  <linearGradient id="colorActivity" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} vertical={false} />
                <XAxis dataKey="hour" tick={{ fontSize: 11, fill: tickColor }} axisLine={false} tickLine={false} interval={2} />
                <YAxis tick={{ fontSize: 12, fill: tickColor }} axisLine={false} tickLine={false} allowDecimals={false} />
                <Tooltip content={<ChartTooltip darkMode={darkMode} />} />
                <Area type="monotone" dataKey="count" name="Activities" stroke="#3b82f6" strokeWidth={2} fill="url(#colorActivity)" />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <EmptyChart message="No hourly data yet" />
          )}
        </div>

        <div className="card">
          <div className="flex items-center gap-2 mb-6">
            <BarChart3 className="w-4 h-4 text-slate-400" />
            <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-200 uppercase tracking-wide">
              Feature Usage
            </h2>
          </div>
          {featureData.some((d) => d.count > 0) ? (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={featureData} layout="vertical" barSize={20}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridColor} horizontal={false} />
                <XAxis type="number" tick={{ fontSize: 12, fill: tickColor }} axisLine={false} tickLine={false} allowDecimals={false} />
                <YAxis type="category" dataKey="name" tick={{ fontSize: 12, fill: labelColor }} axisLine={false} tickLine={false} width={90} />
                <Tooltip content={<ChartTooltip darkMode={darkMode} />} />
                <Bar dataKey="count" name="Usage" radius={[0, 6, 6, 0]}>
                  {featureData.map((entry, i) => (
                    <Cell key={i} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <EmptyChart message="No feature usage yet" />
          )}
        </div>
      </div>

      <div className="card">
        <div className="flex items-center gap-2 mb-4">
          <Clock className="w-4 h-4 text-slate-400" />
          <h2 className="text-sm font-semibold text-slate-700 dark:text-slate-200 uppercase tracking-wide">
            Recent Activity
          </h2>
        </div>
        {analytics?.recent_activity?.length === 0 ? (
          <p className="text-sm text-slate-500 dark:text-slate-400 text-center py-8">
            No activity yet. Start using VisionLearn to see your progress here.
          </p>
        ) : (
          <div className="space-y-0">
            {analytics?.recent_activity?.slice(0, 5).map((activity, idx) => {
              const cfg = ACTION_CONFIG[activity.action] || { icon: FileText, label: activity.action, color: "#64748b" };
              const Icon = cfg.icon;
              return (
                <div
                  key={idx}
                  className="flex items-center gap-3 py-3 border-b border-slate-100 dark:border-slate-800 last:border-0"
                >
                  <div className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0" style={{ backgroundColor: `${cfg.color}15` }}>
                    <Icon className="w-4 h-4" style={{ color: cfg.color }} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm text-slate-700 dark:text-slate-300">
                      {cfg.label}
                    </p>
                    {activity.detail && (
                      <p className="text-xs text-slate-400 dark:text-slate-500 truncate">
                        {activity.detail}
                      </p>
                    )}
                  </div>
                  <span className="text-xs text-slate-400 dark:text-slate-500 shrink-0">
                    {new Date(activity.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}

function EmptyChart({ message }) {
  return (
    <div className="flex items-center justify-center h-[240px] text-slate-400 dark:text-slate-500 text-sm">
      {message}
    </div>
  );
}

function buildDailyData(raw) {
  const map = {};
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const key = d.toISOString().split("T")[0];
    const label = DAY_NAMES[d.getDay()];
    map[key] = { day: label, date: key, Scans: 0, "AI Chat": 0, Uploads: 0, "Read Aloud": 0, "Voice Input": 0 };
  }

  const labelMap = { ocr: "Scans", chat: "AI Chat", upload: "Uploads", tts: "Read Aloud", stt: "Voice Input" };

  for (const row of raw) {
    const entry = map[row.day];
    if (entry) {
      const label = labelMap[row.action] || row.action;
      if (entry[label] !== undefined) {
        entry[label] = row.count;
      }
    }
  }

  return Object.values(map);
}

function buildHourlyData(raw) {
  const map = {};
  for (let h = 0; h < 24; h++) {
    const key = String(h).padStart(2, "0");
    map[key] = { hour: formatHour(key), count: 0 };
  }
  for (const row of raw) {
    if (map[row.hour]) {
      map[row.hour].count = row.count;
    }
  }
  return Object.values(map);
}
