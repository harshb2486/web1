"use client";

import Link from "next/link";
import { LoginForm } from "@/components/auth/login-form";

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center px-6">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/3 left-1/3 w-[400px] h-[400px] rounded-full bg-[var(--color-primary)]/5 blur-[100px]" />
      </div>
      <div className="w-full max-w-md relative z-10">
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-[var(--radius-xs)] bg-[var(--color-primary)] flex items-center justify-center">
              <span className="text-white font-bold font-[family-name:var(--font-heading)]">CI</span>
            </div>
          </Link>
          <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)]">Welcome back</h1>
          <p className="text-sm text-[var(--color-secondary)] mt-1">Sign in to your CreatorOS account</p>
        </div>
        <LoginForm />
        <p className="text-center text-sm text-[var(--color-secondary)] mt-6">
          Don&apos;t have an account?{" "}
          <Link href="/auth/signup" className="text-[var(--color-primary)] hover:underline">Sign up</Link>
        </p>
      </div>
    </div>
  );
}
