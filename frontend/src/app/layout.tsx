import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";
import NavBar from "@/components/NavBar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "MediMind | AI Radiology Assistant",
  description:
    "AI-powered medical imaging assistant for detecting lung abnormalities.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <NavBar />
          <main>{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}
