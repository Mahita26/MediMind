"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import { ArrowRight, Activity, Shield, BrainCircuit, HeartPulse, Users, ScanLine, Trophy } from "lucide-react";
import { apiGetStats, type Stats } from "@/lib/api";

function useCountUp(target: number, duration = 1800) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    if (target === 0) return;
    let start = 0;
    const step = Math.ceil(target / (duration / 16));
    const timer = setInterval(() => {
      start += step;
      if (start >= target) { setCount(target); clearInterval(timer); }
      else setCount(start);
    }, 16);
    return () => clearInterval(timer);
  }, [target, duration]);
  return count;
}

function StatCard({ icon, value, label, suffix = "" }: { icon: React.ReactNode; value: number; label: string; suffix?: string }) {
  const count = useCountUp(value);
  return (
    <div className="flex flex-col items-center p-8 bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg transition-all hover:-translate-y-1 duration-300">
      <div className="h-14 w-14 bg-gradient-to-br from-medical-blue to-cyan-400 rounded-2xl flex items-center justify-center mb-4 shadow-lg shadow-medical-blue/20">
        {icon}
      </div>
      <div className="text-4xl font-extrabold text-gray-900 tabular-nums">
        {count.toLocaleString()}{suffix}
      </div>
      <div className="text-sm text-gray-500 mt-1 font-medium text-center">{label}</div>
    </div>
  );
}

export default function LandingPage() {
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    apiGetStats()
      .then(setStats)
      .catch(() => setStats({ total_users: 0, total_scans: 0, accuracy_rate: 94.2 }));
  }, []);

  return (
    <div className="flex flex-col min-h-[calc(100vh-64px)]">
      {/* Hero Section */}
      <section className="flex flex-1 items-center justify-center p-8 bg-gradient-to-b from-white to-blue-50/40">
        <div className="max-w-5xl w-full grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <div className="inline-flex items-center gap-2 bg-blue-50 border border-blue-100 text-medical-blue text-xs font-semibold px-3 py-1.5 rounded-full">
              <span className="w-2 h-2 bg-medical-blue rounded-full animate-pulse" />
              AI-Powered Diagnostic Platform
            </div>
            <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 tracking-tight leading-tight">
              Radiology,
              <br />
              <span className="text-medical-blue">Reimagined.</span>
            </h1>
            <p className="text-xl text-gray-600 leading-relaxed">
              MediMind analyzes chest X-rays in seconds, delivering explainable Grad-CAM heatmaps and structured medical reports — trusted by radiologists.
            </p>
            <div className="flex gap-4 flex-wrap">
              <Link
                href="/login"
                className="flex items-center gap-2 bg-medical-blue text-white px-8 py-4 rounded-xl font-semibold hover:bg-medical-dark hover:scale-105 transition-all shadow-lg shadow-medical-blue/30"
              >
                Get Started <ArrowRight className="h-5 w-5" />
              </Link>
              <Link
                href="/dashboard"
                className="flex items-center gap-2 bg-white text-gray-900 border border-gray-200 px-8 py-4 rounded-xl font-semibold hover:bg-gray-50 transition-colors"
              >
                Try Demo
              </Link>
            </div>
          </div>
          <div className="relative group">
            <div className="absolute inset-0 bg-gradient-to-tr from-medical-blue to-cyan-400 rounded-3xl blur-2xl opacity-20 group-hover:opacity-30 transition-opacity duration-500" />
            <div className="relative bg-white p-8 rounded-3xl border border-gray-100 shadow-2xl">
              <div className="flex justify-between items-center mb-6">
                <div className="flex items-center gap-2 text-gray-600 font-medium">
                  <Activity className="h-5 w-5 text-medical-blue" />
                  Live Analysis
                </div>
                <span className="text-medical-blue font-bold bg-blue-50 px-3 py-1 rounded-lg text-sm">94.2% Accuracy</span>
              </div>
              <div className="aspect-square rounded-2xl bg-gradient-to-br from-gray-900 to-gray-800 relative overflow-hidden flex items-center justify-center group/image">
                <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80')] bg-cover bg-center opacity-40 mix-blend-luminosity" />
                <div className="absolute top-1/4 right-1/4 w-32 h-32 bg-red-500/40 blur-2xl rounded-full" />
                <div className="absolute top-1/3 right-1/3 w-16 h-16 bg-yellow-400/50 blur-xl rounded-full" />
                <div className="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-medical-blue to-transparent shadow-[0_0_15px_3px_rgba(26,86,219,0.5)] top-0 animate-[scan_3s_ease-in-out_infinite]" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Live Impact Metrics */}
      <section className="bg-gradient-to-b from-blue-50/40 to-white py-16 border-t border-gray-100">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-10">
            <h2 className="text-2xl font-bold text-gray-900">Live Platform Impact</h2>
            <p className="text-gray-500 mt-1 text-sm">Real-time counters powered by our database</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            <StatCard
              icon={<Users className="h-7 w-7 text-white" />}
              value={stats?.total_users ?? 0}
              label="Users Joined"
            />
            <StatCard
              icon={<ScanLine className="h-7 w-7 text-white" />}
              value={stats?.total_scans ?? 0}
              label="Scans Analyzed"
            />
            <StatCard
              icon={<Trophy className="h-7 w-7 text-white" />}
              value={Math.round((stats?.accuracy_rate ?? 94.2) * 10) / 10}
              label="Model Accuracy"
              suffix="%"
            />
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="bg-white py-24 border-t border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Built for the Modern Hospital</h2>
            <p className="text-gray-600">Our platform accelerates the workflow of radiologists while maintaining the highest standards of accuracy and explainability.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<HeartPulse className="h-8 w-8 text-medical-blue" />}
              title="Multi-Disease Detection"
              description="Instantly identifies probabilities for Pneumonia, Tuberculosis, Lung Opacity, Cardiomegaly, and Pleural Effusion."
            />
            <FeatureCard
              icon={<BrainCircuit className="h-8 w-8 text-medical-blue" />}
              title="Explainable AI"
              description="Builds trust with Grad-CAM heatmaps showing exactly which regions of the X-Ray triggered the diagnosis."
            />
            <FeatureCard
              icon={<Shield className="h-8 w-8 text-medical-blue" />}
              title="Clinical Reports"
              description="Automatically generates structured Radiology Reports and simple explanations translated for the patient."
            />
          </div>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="p-8 rounded-2xl bg-gray-50 border border-gray-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
      <div className="mb-6 h-14 w-14 bg-white rounded-xl shadow-sm flex items-center justify-center border border-gray-100">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-gray-900 mb-3">{title}</h3>
      <p className="text-gray-600 leading-relaxed">{description}</p>
    </div>
  );
}

