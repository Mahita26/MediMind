"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Activity, LogOut, User, ChevronDown } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useState } from "react";

export default function NavBar() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleLogout = () => {
    logout();
    router.push("/");
  };

  return (
    <nav className="border-b bg-white sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group">
          <div className="h-8 w-8 bg-medical-blue rounded-lg flex items-center justify-center group-hover:scale-105 transition-transform">
            <Activity className="h-5 w-5 text-white" />
          </div>
          <span className="font-bold text-xl text-gray-900">MediMind</span>
          <span className="hidden sm:inline-flex text-xs bg-blue-50 text-medical-blue border border-blue-100 px-2 py-0.5 rounded-full font-medium">
            AI Radiology
          </span>
        </Link>

        {/* Right side */}
        <div className="flex items-center gap-3">
          {user ? (
            // ── Authenticated state ────────────────────────────────────
            <div className="relative">
              <button
                onClick={() => setDropdownOpen((v) => !v)}
                className="flex items-center gap-2 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-xl px-3 py-2 transition-colors"
              >
                <div className="h-7 w-7 bg-gradient-to-br from-medical-blue to-cyan-500 rounded-full flex items-center justify-center">
                  <User className="h-4 w-4 text-white" />
                </div>
                <div className="text-left hidden sm:block">
                  <p className="text-sm font-semibold text-gray-900 leading-none">
                    {user.full_name}
                  </p>
                  <p className="text-xs text-gray-500 capitalize">{user.role}</p>
                </div>
                <ChevronDown className={`h-4 w-4 text-gray-400 transition-transform ${dropdownOpen ? "rotate-180" : ""}`} />
              </button>

              {dropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white border border-gray-100 rounded-xl shadow-lg py-1 z-50">
                  <Link
                    href="/dashboard"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                    onClick={() => setDropdownOpen(false)}
                  >
                    Dashboard
                  </Link>
                  <hr className="my-1 border-gray-100" />
                  <button
                    onClick={() => { setDropdownOpen(false); handleLogout(); }}
                    className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
                  >
                    <LogOut className="h-4 w-4" />
                    Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            // ── Unauthenticated state ──────────────────────────────────
            <>
              <Link href="/login" className="text-gray-600 hover:text-gray-900 text-sm font-medium">
                Sign in
              </Link>
              <Link
                href="/login"
                className="bg-medical-blue text-white px-4 py-2 rounded-lg hover:bg-medical-dark transition-colors text-sm font-medium shadow-sm shadow-medical-blue/30"
              >
                Get Started
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
