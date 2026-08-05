"use client";

import Link from "next/link";

export default function ForgotPasswordPage() {
  return (
    <div className="min-h-screen flex items-center justify-center px-6">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-[var(--radius-xs)] bg-[var(--color-primary)] flex items-center justify-center">
              <span className="text-white font-bold font-[family-name:var(--font-heading)]">CI</span>
            </div>
          </Link>
          <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)]">Reset your password</h1>
          <p className="text-sm text-[var(--color-secondary)] mt-1">Enter your email and we'll send you a reset link</p>
        </div>
        <div className="bg-[var(--color-card)] border border-[var(--color-border)] rounded-[var(--radius)] p-6">
          <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-[var(--color-secondary)]">Email</label>
              <input
                type="email"
                placeholder="you@example.com"
                className="flex h-10 w-full rounded-[var(--radius-sm)] bg-white/5 border border-[var(--color-border)] px-3 py-2 text-sm text-[var(--color-foreground)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-primary)]/50"
              />
            </div>
            <button className="w-full h-10 rounded-[var(--radius-sm)] bg-[var(--color-primary)] text-white text-sm font-medium hover:bg-[#4a6bff] transition-colors">
              Send reset link
            </button>
          </form>
          <p className="text-center text-sm text-[var(--color-secondary)] mt-4">
            <Link href="/auth/login" className="text-[var(--color-primary)] hover:underline">Back to login</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
