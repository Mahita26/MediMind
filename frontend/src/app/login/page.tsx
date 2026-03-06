"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { Activity, Stethoscope, User } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { apiLogin, apiRegister } from "@/lib/api";

type Tab = "login" | "register";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();

  const [tab, setTab] = useState<Tab>("login");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Shared fields
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  // Register-only fields
  const [fullName, setFullName] = useState("");
  const [role, setRole] = useState<"doctor" | "patient">("doctor");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      let data;
      if (tab === "login") {
        data = await apiLogin({ email, password });
      } else {
        data = await apiRegister({ email, password, full_name: fullName, role });
      }

      login(data.access_token, {
        user_id: data.user_id,
        full_name: data.full_name,
        role: data.role as "doctor" | "patient",
      });
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50/30 py-12 px-4">
      <div className="max-w-md w-full">
        {/* Logo + Title */}
        <div className="text-center mb-8">
          <div className="inline-flex h-14 w-14 bg-gradient-to-br from-medical-blue to-cyan-500 rounded-2xl items-center justify-center shadow-lg shadow-medical-blue/30 mb-4">
            <Activity className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-3xl font-extrabold text-gray-900">MediMind</h1>
          <p className="text-gray-500 mt-1 text-sm">AI-Powered Radiology Platform</p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 overflow-hidden">
          {/* Tabs */}
          <div className="flex border-b border-gray-100">
            {(["login", "register"] as Tab[]).map((t) => (
              <button
                key={t}
                onClick={() => { setTab(t); setError(null); }}
                className={`flex-1 py-4 text-sm font-semibold transition-colors ${
                  tab === t
                    ? "text-medical-blue border-b-2 border-medical-blue bg-blue-50/50"
                    : "text-gray-500 hover:text-gray-700"
                }`}
              >
                {t === "login" ? "Sign In" : "Create Account"}
              </button>
            ))}
          </div>

          <form onSubmit={handleSubmit} className="p-8 space-y-5">
            {/* Full name (register only) */}
            {tab === "register" && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">
                  Full Name
                </label>
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Dr. Jane Smith"
                  className="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-medical-blue/30 focus:border-medical-blue transition-all"
                />
              </div>
            )}

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="doctor@hospital.com"
                className="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-medical-blue/30 focus:border-medical-blue transition-all"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-4 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-medical-blue/30 focus:border-medical-blue transition-all"
              />
            </div>

            {/* Role selector (register only) */}
            {tab === "register" && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  I am a…
                </label>
                <div className="grid grid-cols-2 gap-3">
                  {(["doctor", "patient"] as const).map((r) => (
                    <button
                      key={r}
                      type="button"
                      onClick={() => setRole(r)}
                      className={`flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all ${
                        role === r
                          ? "border-medical-blue bg-blue-50 text-medical-blue"
                          : "border-gray-200 text-gray-500 hover:border-gray-300"
                      }`}
                    >
                      {r === "doctor" ? (
                        <Stethoscope className="h-6 w-6" />
                      ) : (
                        <User className="h-6 w-6" />
                      )}
                      <span className="text-sm font-semibold capitalize">{r}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-3 rounded-xl">
                {error}
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-medical-blue hover:bg-medical-dark disabled:opacity-60 disabled:cursor-not-allowed text-white font-semibold py-3.5 rounded-xl transition-all flex items-center justify-center gap-2 shadow-md shadow-medical-blue/30"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : tab === "login" ? (
                "Sign In"
              ) : (
                "Create Account"
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
