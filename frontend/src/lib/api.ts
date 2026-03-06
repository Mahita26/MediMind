const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("mm_token");
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: HeadersInit = {
    ...(options.headers || {}),
  };
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }
  // Only set Content-Type to JSON when NOT sending FormData
  if (!(options.body instanceof FormData)) {
    (headers as Record<string, string>)["Content-Type"] = "application/json";
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

// ─── Auth ────────────────────────────────────────────────────────────────────
export interface AuthPayload {
  access_token: string;
  token_type: string;
  user_id: string;
  full_name: string;
  role: string;
}

export const apiRegister = (data: {
  email: string;
  password: string;
  full_name: string;
  role: string;
}) => request<AuthPayload>("/auth/register", { method: "POST", body: JSON.stringify(data) });

export const apiLogin = (data: { email: string; password: string }) =>
  request<AuthPayload>("/auth/login", { method: "POST", body: JSON.stringify(data) });

// ─── Patients ─────────────────────────────────────────────────────────────────
export interface Patient {
  id: string;
  name: string;
  age: number | null;
  phone: string | null;
  created_at: string;
}

export const apiGetPatients = () => request<Patient[]>("/patients");

export const apiCreatePatient = (data: { name: string; age?: number; phone?: string }) =>
  request<Patient>("/patients", { method: "POST", body: JSON.stringify(data) });

// ─── Scans ────────────────────────────────────────────────────────────────────
export interface Report {
  findings: string | null;
  impression: string | null;
  recommendation: string | null;
}

export interface ScanResult {
  id: string;
  patient_user_id: string;
  patient_name: string | null;
  predictions: Record<string, number>;
  report: Report;
  patient_explanation: string | null;
  heatmap_base64: string | null;
  created_at: string;
}

export const apiUploadScan = (file: File, patientProfileId?: string): Promise<ScanResult> => {
  const form = new FormData();
  form.append("file", file);
  const url = patientProfileId
    ? `/scans/upload?patient_profile_id=${patientProfileId}`
    : "/scans/upload";
  return request<ScanResult>(url, { method: "POST", body: form });
};

export const apiGetHistory = () => request<ScanResult[]>("/scans/history");

// ─── Stats ────────────────────────────────────────────────────────────────────
export interface Stats {
  total_users: number;
  total_scans: number;
  accuracy_rate: number;
}

export const apiGetStats = () => request<Stats>("/stats");
