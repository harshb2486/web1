"use client";

import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-[var(--color-border)] py-12">
      <div className="max-w-6xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-10">
          <div className="col-span-2 md:col-span-1">
            <Link href="/" className="flex items-center gap-3 mb-4">
              <div className="w-8 h-8 rounded-[var(--radius-xs)] bg-[var(--color-primary)] flex items-center justify-center">
                <span className="text-white font-bold text-sm font-[family-name:var(--font-heading)]">CI</span>
              </div>
              <span className="font-semibold font-[family-name:var(--font-heading)]">CreatorOS</span>
            </Link>
            <p className="text-sm text-[var(--color-secondary)] leading-relaxed">
              The AI operating system for content creators.
            </p>
          </div>
          <div>
            <h4 className="text-sm font-semibold mb-3">Product</h4>
            <ul className="space-y-2 text-sm text-[var(--color-secondary)]">
              <li><a href="#features" className="hover:text-[var(--color-foreground)] transition-colors">Features</a></li>
              <li><a href="#pricing" className="hover:text-[var(--color-foreground)] transition-colors">Pricing</a></li>
              <li><Link href="/auth/login" className="hover:text-[var(--color-foreground)] transition-colors">Login</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-semibold mb-3">Resources</h4>
            <ul className="space-y-2 text-sm text-[var(--color-secondary)]">
              <li><a href="#" className="hover:text-[var(--color-foreground)] transition-colors">Documentation</a></li>
              <li><a href="#" className="hover:text-[var(--color-foreground)] transition-colors">Blog</a></li>
              <li><a href="#" className="hover:text-[var(--color-foreground)] transition-colors">Changelog</a></li>
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-semibold mb-3">Company</h4>
            <ul className="space-y-2 text-sm text-[var(--color-secondary)]">
              <li><a href="#" className="hover:text-[var(--color-foreground)] transition-colors">About</a></li>
              <li><a href="#" className="hover:text-[var(--color-foreground)] transition-colors">Privacy</a></li>
              <li><a href="#" className="hover:text-[var(--color-foreground)] transition-colors">Terms</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-[var(--color-border)] pt-8 text-center text-sm text-[var(--color-muted)]">
          &copy; 2026 CreatorOS. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
