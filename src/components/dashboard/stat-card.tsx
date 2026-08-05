"use client";

import { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface StatCardProps {
  icon: ReactNode;
  label: string;
  value: string | ReactNode;
  change?: string;
  changeType?: "positive" | "negative" | "neutral";
  className?: string;
}

export function StatCard({ icon, label, value, change, changeType = "neutral", className }: StatCardProps) {
  return (
    <div className={cn("rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-5 transition-colors hover:border-[var(--color-border-hover)]", className)}>
      <div className="flex items-center gap-2 mb-3">
        <div className="w-8 h-8 rounded-[var(--radius-xs)] bg-white/5 flex items-center justify-center text-[var(--color-secondary)]">
          {icon}
        </div>
        <span className="text-xs text-[var(--color-secondary)]">{label}</span>
      </div>
      <div className="text-2xl font-bold font-[family-name:var(--font-mono)]">{value}</div>
      {change && (
        <div className={cn("text-xs mt-1 font-medium", {
          "text-[var(--color-success)]": changeType === "positive",
          "text-[var(--color-danger)]": changeType === "negative",
          "text-[var(--color-secondary)]": changeType === "neutral",
        })}>
          {change}
        </div>
      )}
    </div>
  );
}
