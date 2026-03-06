"use client";
import { useState, useRef, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import {
  UploadCloud, FileText, AlertCircle, Activity, Image as ImageIcon,
  Loader2, Shield, Users, PlusCircle, Clock, BarChart2, Search,
  Scan, Eye, EyeOff, X, ChevronRight
} from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell
} from "recharts";
import { useAuth } from "@/context/AuthContext";
import {
  apiUploadScan, apiGetHistory, apiGetPatients, apiCreatePatient,
  type ScanResult, type Patient
} from "@/lib/api";

type Tab = "analyze" | "history" | "analytics";

// ─── Confidence Bar ────────────────────────────────────────────────────────────
function ConfidenceBar({ label, probability }: { label: string; probability: number }) {
  const isHigh = probability > 0.5;
  const isMedium = probability > 0.3 && probability <= 0.5;
  return (
    <div className="mb-4">
      <div className="flex justify-between text-sm font-medium mb-1.5">
        <span className="text-gray-700">{label}</span>
        <span className={isHigh ? "text-red-600 font-bold" : isMedium ? "text-yellow-600 font-semibold" : "text-green-600 font-semibold"}>
          {(probability * 100).toFixed(1)}%
        </span>
      </div>
      <div className="w-full bg-gray-100 rounded-full h-2.5">
        <div
          className={`h-2.5 rounded-full transition-all duration-1000 ${isHigh ? "bg-red-500" : isMedium ? "bg-yellow-400" : "bg-green-500"}`}
          style={{ width: `${Math.max(probability * 100, 2)}%` }}
        />
      </div>
    </div>
  );
}

// ─── Add Patient Modal ─────────────────────────────────────────────────────────
function AddPatientModal({ onClose, onAdded }: { onClose: () => void; onAdded: (p: Patient) => void }) {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [phone, setPhone] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    setLoading(true);
    try {
      const patient = await apiCreatePatient({
        name: name.trim(),
        age: age ? parseInt(age) : undefined,
        phone: phone.trim() || undefined,
      });
      onAdded(patient);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 animate-in fade-in slide-in-from-bottom-4 duration-300">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-bold text-gray-900">Add New Patient</h3>
          <button onClick={onClose} className="h-8 w-8 flex items-center justify-center rounded-lg hover:bg-gray-100 transition-colors">
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Full Name *</label>
            <input
              type="text" required value={name}
              onChange={e => setName(e.target.value)}
              placeholder="John Doe"
              className="w-full px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-medical-blue/30 focus:border-medical-blue"
            />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Age</label>
              <input
                type="number" min="0" max="120" value={age}
                onChange={e => setAge(e.target.value)}
                placeholder="45"
                className="w-full px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-medical-blue/30 focus:border-medical-blue"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">Phone</label>
              <input
                type="tel" value={phone}
                onChange={e => setPhone(e.target.value)}
                placeholder="+91 9876543210"
                className="w-full px-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-medical-blue/30 focus:border-medical-blue"
              />
            </div>
          </div>
          {error && <p className="text-red-600 text-sm bg-red-50 border border-red-100 px-3 py-2 rounded-lg">{error}</p>}
          <div className="flex gap-3 pt-2">
            <button type="button" onClick={onClose} className="flex-1 border border-gray-200 text-gray-700 py-2.5 rounded-xl font-medium hover:bg-gray-50 text-sm">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="flex-1 bg-medical-blue text-white py-2.5 rounded-xl font-semibold hover:bg-medical-dark disabled:opacity-60 text-sm flex items-center justify-center gap-2">
              {loading ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" /> : "Add Patient"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// ─── History Table ─────────────────────────────────────────────────────────────
function HistoryTab({ history, loading }: { history: ScanResult[]; loading: boolean }) {
  const [search, setSearch] = useState("");
  const filtered = history.filter(s => {
    const q = search.toLowerCase();
    const topDisease = Object.entries(s.predictions).sort(([,a],[,b]) => b - a)[0]?.[0] ?? "";
    return (
      (s.patient_name ?? "").toLowerCase().includes(q) ||
      topDisease.toLowerCase().includes(q) ||
      s.report.impression?.toLowerCase().includes(q)
    );
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="h-8 w-8 text-medical-blue animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3 bg-white border border-gray-200 rounded-xl px-4 py-2.5 shadow-sm">
        <Search className="h-4 w-4 text-gray-400" />
        <input
          type="text" value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search by patient, disease, or impression…"
          className="flex-1 text-sm outline-none text-gray-700 placeholder-gray-400"
        />
      </div>

      {filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center">
          <div className="h-20 w-20 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Clock className="h-10 w-10 text-gray-300" />
          </div>
          <h3 className="font-semibold text-gray-700 mb-1">No History Found</h3>
          <p className="text-gray-400 text-sm">{search ? "No scans match your search." : "Upload and analyze your first X-ray to see history here."}</p>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 text-left border-b border-gray-100">
                <th className="px-5 py-3 font-semibold text-gray-600">Patient</th>
                <th className="px-5 py-3 font-semibold text-gray-600">Top Finding</th>
                <th className="px-5 py-3 font-semibold text-gray-600">Impression</th>
                <th className="px-5 py-3 font-semibold text-gray-600">Date</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((scan, i) => {
                const [topDisease, topProb] = Object.entries(scan.predictions).sort(([,a],[,b]) => b - a)[0] ?? ["—", 0];
                const isPositive = topProb > 0.5 && topDisease !== "Normal";
                return (
                  <tr key={scan.id} className={`border-b border-gray-50 hover:bg-gray-50/50 transition-colors ${i % 2 === 0 ? "" : "bg-gray-50/30"}`}>
                    <td className="px-5 py-3.5 font-medium text-gray-900">{scan.patient_name ?? "—"}</td>
                    <td className="px-5 py-3.5">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold ${isPositive ? "bg-red-50 text-red-700" : "bg-green-50 text-green-700"}`}>
                        {topDisease} {(topProb * 100).toFixed(0)}%
                      </span>
                    </td>
                    <td className="px-5 py-3.5 text-gray-500 max-w-xs truncate">{scan.report.impression ?? "—"}</td>
                    <td className="px-5 py-3.5 text-gray-400 whitespace-nowrap">{new Date(scan.created_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// ─── Analytics Tab ─────────────────────────────────────────────────────────────
const DISEASE_COLORS: Record<string, string> = {
  Pneumonia: "#ef4444", Tuberculosis: "#f97316", "Lung Opacity": "#eab308",
  Cardiomegaly: "#a855f7", "Pleural Effusion": "#3b82f6", Normal: "#22c55e",
};

function AnalyticsTab({ history }: { history: ScanResult[] }) {
  // Aggregate disease counts (where prob > 0.5)
  const counts: Record<string, number> = {};
  history.forEach(scan => {
    Object.entries(scan.predictions).forEach(([disease, prob]) => {
      if (prob > 0.5) counts[disease] = (counts[disease] ?? 0) + 1;
    });
  });
  const chartData = Object.entries(counts)
    .sort(([,a],[,b]) => b - a)
    .map(([name, count]) => ({ name, count }));

  return (
    <div className="space-y-6">
      {/* Stats row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {[
          { label: "Total Scans", value: history.length },
          { label: "Positive Cases", value: history.filter(s => Object.entries(s.predictions).some(([k,v]) => v > 0.5 && k !== "Normal")).length },
          { label: "Unique Patients", value: new Set(history.map(s => s.patient_user_id)).size },
          { label: "Avg Confidence", value: history.length ? (history.map(s => Math.max(...Object.values(s.predictions))).reduce((a,b) => a+b, 0) / history.length * 100).toFixed(0) + "%" : "—" },
        ].map(({ label, value }) => (
          <div key={label} className="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm">
            <div className="text-2xl font-extrabold text-gray-900">{value}</div>
            <div className="text-xs text-gray-500 mt-0.5">{label}</div>
          </div>
        ))}
      </div>

      {chartData.length === 0 ? (
        <div className="bg-white border border-gray-100 rounded-2xl p-12 text-center shadow-sm">
          <BarChart2 className="h-12 w-12 text-gray-200 mx-auto mb-3" />
          <p className="text-gray-500 text-sm">No positive findings yet. Analyze scans to populate the chart.</p>
        </div>
      ) : (
        <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
          <h3 className="text-sm font-bold text-gray-700 uppercase tracking-wider mb-6">Disease Distribution (Positive Findings)</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={chartData} barSize={40}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
              <XAxis dataKey="name" tick={{ fontSize: 12, fill: "#6b7280" }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 12, fill: "#6b7280" }} axisLine={false} tickLine={false} allowDecimals={false} />
              <Tooltip
                contentStyle={{ borderRadius: 12, border: "1px solid #e5e7eb", boxShadow: "0 4px 20px rgba(0,0,0,0.08)" }}
                cursor={{ fill: "rgba(26,86,219,0.04)" }}
              />
              <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                {chartData.map(({ name }) => (
                  <Cell key={name} fill={DISEASE_COLORS[name] ?? "#1a56db"} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

// ─── Main Dashboard ────────────────────────────────────────────────────────────
export default function DashboardPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  const [activeTab, setActiveTab] = useState<Tab>("analyze");
  const [file, setFile] = useState<File | null>(null);
  const [previewURL, setPreviewURL] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState<ScanResult | null>(null);
  const [showHeatmap, setShowHeatmap] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Doctor-specific state
  const [patients, setPatients] = useState<Patient[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string>("");
  const [showAddPatient, setShowAddPatient] = useState(false);

  // History state
  const [history, setHistory] = useState<ScanResult[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  // ── Auth guard ────────────────────────────────────────────────────────────
  useEffect(() => {
    if (!isLoading && !user) {
      router.replace("/login");
    }
  }, [user, isLoading, router]);

  // ── Load doctor's patients ─────────────────────────────────────────────────
  useEffect(() => {
    if (user?.role === "doctor") {
      apiGetPatients()
        .then(setPatients)
        .catch(console.error);
    }
  }, [user]);

  // ── Load history when switching to history/analytics tab ──────────────────
  useEffect(() => {
    if (activeTab === "history" || activeTab === "analytics") {
      setHistoryLoading(true);
      apiGetHistory()
        .then(setHistory)
        .catch(console.error)
        .finally(() => setHistoryLoading(false));
    }
  }, [activeTab]);

  // ── File handling ─────────────────────────────────────────────────────────
  const handleFile = useCallback((f: File) => {
    if (!f.type.startsWith("image/")) { setError("Please upload an image file."); return; }
    setFile(f);
    setPreviewURL(URL.createObjectURL(f));
    setResults(null);
    setError(null);
    setShowHeatmap(true);
  }, []);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  };

  const handleAnalyze = async () => {
    if (!file) return;
    if (user?.role === "doctor" && !selectedPatientId) {
      setError("Please select a patient before analyzing.");
      return;
    }
    setIsAnalyzing(true);
    setError(null);
    try {
      const data = await apiUploadScan(file, user?.role === "doctor" ? selectedPatientId : undefined);
      setResults(data);
      // Refresh history counts silently
      apiGetHistory().then(setHistory).catch(() => {});
    } catch (err: any) {
      setError(err.message || "Analysis failed. Please ensure the backend is running.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const clearSession = () => {
    setFile(null);
    setPreviewURL(null);
    setResults(null);
    setError(null);
    setIsAnalyzing(false);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 text-medical-blue animate-spin" />
      </div>
    );
  }

  if (!user) return null;

  const TABS = [
    { id: "analyze" as Tab, label: "Analyze", icon: Scan },
    { id: "history" as Tab, label: "History", icon: Clock },
    ...(user.role === "doctor" ? [{ id: "analytics" as Tab, label: "Analytics", icon: BarChart2 }] : []),
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* ── Sidebar ────────────────────────────────────────────────────────── */}
      <aside className="w-64 bg-white border-r border-gray-100 hidden md:flex flex-col shadow-sm">
        <div className="p-6 space-y-1">
          {TABS.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-colors ${
                activeTab === id
                  ? "bg-medical-blue text-white shadow-md shadow-medical-blue/30"
                  : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
              }`}
            >
              <Icon className="h-4 w-4" />
              {label}
            </button>
          ))}
        </div>

        {/* Doctor: Add Patient button */}
        {user.role === "doctor" && (
          <div className="px-6 mt-2">
            <button
              onClick={() => setShowAddPatient(true)}
              className="w-full flex items-center gap-2 px-4 py-2.5 border border-dashed border-gray-300 rounded-xl text-gray-500 hover:text-medical-blue hover:border-medical-blue text-sm font-medium transition-colors"
            >
              <PlusCircle className="h-4 w-4" />
              Add Patient
            </button>
          </div>
        )}

        {/* User info card */}
        <div className="mt-auto p-6">
          <div className="bg-gradient-to-br from-medical-blue to-cyan-500 rounded-2xl p-4 text-white shadow-lg">
            <div className="flex items-center gap-2 mb-2">
              <div className="h-8 w-8 bg-white/20 rounded-full flex items-center justify-center text-xs font-bold">
                {user.full_name.charAt(0).toUpperCase()}
              </div>
              <div>
                <p className="text-sm font-semibold leading-none">{user.full_name}</p>
                <p className="text-xs opacity-80 capitalize mt-0.5">{user.role}</p>
              </div>
            </div>
            <div className="text-xs bg-white/20 py-1 px-2 rounded-lg inline-block">
              {history.length} Scan{history.length !== 1 ? "s" : ""} Total
            </div>
          </div>
        </div>
      </aside>

      {/* ── Main Content ───────────────────────────────────────────────────── */}
      <main className="flex-1 p-6 lg:p-8 overflow-y-auto">
        <div className="max-w-6xl mx-auto space-y-6">

          {/* Header */}
          <header className="flex justify-between items-center bg-white p-5 rounded-2xl shadow-sm border border-gray-100">
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                {activeTab === "analyze" ? "New Diagnostic Session" : activeTab === "history" ? "Scan History" : "Analytics Dashboard"}
              </h1>
              <p className="text-gray-400 text-sm mt-0.5">
                Welcome back, {user.full_name}
              </p>
            </div>
            {activeTab === "analyze" && (
              <button
                onClick={clearSession}
                className="bg-white border border-gray-200 text-gray-600 hover:bg-gray-50 px-4 py-2 rounded-lg text-sm font-medium transition-colors"
              >
                Clear Session
              </button>
            )}
          </header>

          {/* Mobile tab bar */}
          <div className="flex md:hidden gap-1 bg-white border border-gray-100 rounded-xl p-1 shadow-sm">
            {TABS.map(({ id, label }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`flex-1 py-2 rounded-lg text-xs font-semibold transition-colors ${activeTab === id ? "bg-medical-blue text-white" : "text-gray-500"}`}
              >
                {label}
              </button>
            ))}
          </div>

          {/* ────────────── ANALYZE TAB ────────────── */}
          {activeTab === "analyze" && (
            <div className="space-y-5">
              {/* Doctor: Patient selector */}
              {user.role === "doctor" && (
                <div className="bg-white border border-gray-100 rounded-2xl p-5 shadow-sm">
                  <div className="flex items-center gap-3 flex-wrap">
                    <Users className="h-5 w-5 text-medical-blue flex-shrink-0" />
                    <label className="text-sm font-semibold text-gray-700">Select Patient:</label>
                    <select
                      value={selectedPatientId}
                      onChange={e => setSelectedPatientId(e.target.value)}
                      className="flex-1 min-w-[200px] border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-medical-blue/30 focus:border-medical-blue bg-gray-50"
                    >
                      <option value="">— Choose a patient —</option>
                      {patients.map(p => (
                        <option key={p.id} value={p.id}>
                          {p.name}{p.age ? `, ${p.age}y` : ""}
                        </option>
                      ))}
                    </select>
                    <button
                      onClick={() => setShowAddPatient(true)}
                      className="flex items-center gap-1.5 text-medical-blue hover:text-medical-dark text-sm font-semibold transition-colors"
                    >
                      <PlusCircle className="h-4 w-4" /> Add New
                    </button>
                  </div>
                </div>
              )}

              {/* Upload + Results */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Upload zone */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col" style={{ minHeight: 480 }}>
                  <h2 className="text-base font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <ImageIcon className="h-5 w-5 text-medical-blue" />
                    Image Input
                  </h2>

                  {!previewURL ? (
                    <div
                      onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
                      onDragLeave={() => setIsDragging(false)}
                      onDrop={handleDrop}
                      onClick={() => fileInputRef.current?.click()}
                      className={`flex-1 border-2 border-dashed rounded-xl transition-all cursor-pointer flex flex-col items-center justify-center text-center p-6 ${
                        isDragging ? "border-medical-blue bg-blue-50 scale-[1.01]" : "border-gray-200 bg-gray-50 hover:bg-gray-100 hover:border-gray-300"
                      }`}
                    >
                      <div className="h-16 w-16 bg-white shadow-sm rounded-full flex items-center justify-center mb-4 border border-gray-100">
                        <UploadCloud className={`h-8 w-8 ${isDragging ? "text-medical-blue" : "text-gray-400"}`} />
                      </div>
                      <p className="font-semibold text-gray-700 mb-1">
                        {isDragging ? "Drop to upload!" : "Drag & drop or click to upload"}
                      </p>
                      <p className="text-xs text-gray-400">Supported: JPG, PNG, DICOM</p>
                      <input
                        type="file" className="hidden" ref={fileInputRef}
                        accept="image/*" onChange={e => { if (e.target.files?.[0]) handleFile(e.target.files[0]); }}
                      />
                    </div>
                  ) : (
                    <div className="flex-1 relative rounded-xl overflow-hidden bg-black flex flex-col items-center justify-center group">
                      <img
                        src={showHeatmap && results?.heatmap_base64 ? results.heatmap_base64 : previewURL}
                        alt="X-Ray"
                        className="object-contain h-full w-full"
                      />
                      {/* Heatmap toggle */}
                      {results?.heatmap_base64 && (
                        <button
                          onClick={() => setShowHeatmap(v => !v)}
                          className="absolute top-3 right-3 bg-black/60 text-white px-3 py-1.5 rounded-lg text-xs flex items-center gap-1.5 hover:bg-black/80 transition-colors"
                        >
                          {showHeatmap ? <><EyeOff className="h-3.5 w-3.5" /> Original</> : <><Eye className="h-3.5 w-3.5" /> Heatmap</>}
                        </button>
                      )}
                      {!results && !isAnalyzing && (
                        <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                          <button onClick={() => fileInputRef.current?.click()} className="bg-white/90 text-gray-900 px-4 py-2 rounded-lg font-medium text-sm">
                            Change Image
                          </button>
                        </div>
                      )}
                      {isAnalyzing && (
                        <div className="absolute inset-0 bg-medical-blue/80 flex flex-col items-center justify-center text-white backdrop-blur-sm">
                          <Loader2 className="h-10 w-10 animate-spin mb-3" />
                          <p className="font-semibold text-lg">Running AI Engine…</p>
                          <p className="text-sm opacity-80 mt-1">Generating Grad-CAM heatmap</p>
                        </div>
                      )}
                    </div>
                  )}

                  {error && (
                    <div className="mt-3 bg-red-50 border border-red-100 text-red-700 text-sm px-4 py-2.5 rounded-xl">
                      {error}
                    </div>
                  )}

                  <button
                    onClick={handleAnalyze}
                    disabled={!file || isAnalyzing || !!results}
                    className="mt-4 w-full bg-medical-blue hover:bg-medical-dark disabled:bg-gray-200 disabled:cursor-not-allowed disabled:text-gray-400 text-white font-semibold py-3.5 rounded-xl shadow-md shadow-medical-blue/20 transition-all flex items-center justify-center gap-2"
                  >
                    {isAnalyzing ? (
                      <><Loader2 className="h-4 w-4 animate-spin" /> Analyzing…</>
                    ) : results ? (
                      <><Shield className="h-4 w-4" /> Analysis Complete</>
                    ) : (
                      <><Scan className="h-4 w-4" /> Analyze Imaging Scan</>
                    )}
                  </button>
                </div>

                {/* Results Panel */}
                <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col" style={{ minHeight: 480 }}>
                  <h2 className="text-base font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <Activity className="h-5 w-5 text-medical-blue" />
                    AI Diagnostic Results
                  </h2>

                  {!results && !isAnalyzing && (
                    <div className="flex-1 flex flex-col items-center justify-center text-center px-6">
                      <div className="h-24 w-24 bg-gray-50 rounded-full flex items-center justify-center mb-5 border border-gray-100">
                        <Shield className="h-10 w-10 text-gray-200" />
                      </div>
                      <h3 className="text-gray-700 font-semibold mb-1.5">Awaiting Image Upload</h3>
                      <p className="text-sm text-gray-400 leading-relaxed max-w-xs">
                        Upload a chest X-ray and click Analyze. The AI will scan for 6 distinct pathologies and compute disease probabilities.
                      </p>
                    </div>
                  )}

                  {isAnalyzing && (
                    <div className="flex-1 flex flex-col items-center justify-center gap-4">
                      <div className="w-48 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                        <div className="h-full bg-medical-blue animate-[scanning_1.5s_ease-in-out_infinite] rounded-full" />
                      </div>
                      <p className="text-sm text-gray-400 animate-pulse">Computing multi-label probabilities…</p>
                    </div>
                  )}

                  {results && (
                    <div className="flex-1 overflow-y-auto space-y-5 pr-1 custom-scrollbar">
                      {/* Confidence scores */}
                      <div className="p-5 bg-gray-50 rounded-xl border border-gray-100">
                        <h3 className="text-xs font-bold text-gray-600 uppercase tracking-wider mb-4 pb-2 border-b border-gray-200">Confidence Scores</h3>
                        {Object.entries(results.predictions)
                          .sort(([,a],[,b]) => b - a)
                          .map(([label, prob]) => (
                            <ConfidenceBar key={label} label={label} probability={prob as number} />
                          ))}
                      </div>

                      {/* Report */}
                      <div className="p-5 bg-blue-50/60 rounded-xl border border-blue-100">
                        <h3 className="text-xs font-bold text-medical-dark uppercase tracking-wider mb-3 pb-2 border-b border-blue-100 flex items-center gap-1.5">
                          <FileText className="h-3.5 w-3.5" /> Structured Radiology Report
                        </h3>
                        <div className="space-y-2.5 text-sm text-gray-700">
                          <p><span className="font-semibold text-gray-900">Findings:</span> {results.report.findings}</p>
                          <p><span className="font-semibold text-gray-900">Impression:</span> {results.report.impression}</p>
                          <p><span className="font-semibold text-gray-900">Recommendation:</span> {results.report.recommendation}</p>
                        </div>
                      </div>

                      {/* Patient explanation */}
                      <div className="p-5 bg-green-50/60 rounded-xl border border-green-100">
                        <h3 className="text-xs font-bold text-green-800 uppercase tracking-wider mb-3 pb-2 border-b border-green-100 flex items-center gap-1.5">
                          <AlertCircle className="h-3.5 w-3.5" /> Patient Explanation
                        </h3>
                        <p className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">{results.patient_explanation}</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* ────────────── HISTORY TAB ────────────── */}
          {activeTab === "history" && (
            <HistoryTab history={history} loading={historyLoading} />
          )}

          {/* ────────────── ANALYTICS TAB (Doctor only) ────────────── */}
          {activeTab === "analytics" && user.role === "doctor" && (
            <AnalyticsTab history={history} />
          )}
        </div>
      </main>

      {/* Add Patient Modal */}
      {showAddPatient && (
        <AddPatientModal
          onClose={() => setShowAddPatient(false)}
          onAdded={newPatient => {
            setPatients(prev => [...prev, newPatient]);
            setSelectedPatientId(newPatient.id);
            setShowAddPatient(false);
          }}
        />
      )}

      <style dangerouslySetInnerHTML={{ __html: `
        @keyframes scanning { 0% { transform: translateX(-100%); } 50% { transform: translateX(0); } 100% { transform: translateX(100%); } }
        @keyframes scan { 0% { top: 0; opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { top: 100%; opacity: 0; } }
        .custom-scrollbar::-webkit-scrollbar { width: 5px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: #f9f9f9; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 4px; }
      `}} />
    </div>
  );
}
