"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

export function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 px-6 py-4">
      <div className="max-w-6xl mx-auto flex items-center justify-between bg-[var(--color-surface)]/80 backdrop-blur-md border border-[var(--color-border)] rounded-[var(--radius)] px-6 py-3">
        <Link href="/" className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-[var(--radius-xs)] bg-[var(--color-primary)] flex items-center justify-center">
            <span className="text-white font-bold text-sm font-[family-name:var(--font-heading)]">CI</span>
          </div>
          <span className="font-semibold text-lg font-[family-name:var(--font-heading)]">CreatorOS</span>
        </Link>

        <div className="hidden md:flex items-center gap-8 text-sm text-[var(--color-secondary)]">
          <a href="#features" className="hover:text-[var(--color-foreground)] transition-colors">Features</a>
          <a href="#pricing" className="hover:text-[var(--color-foreground)] transition-colors">Pricing</a>
          <Link href="/auth/login" className="hover:text-[var(--color-foreground)] transition-colors">Login</Link>
        </div>

        <Link href="/auth/signup">
          <Button size="sm">Get Started</Button>
        </Link>
      </div>
    </nav>
  );
}
