"use client";

import { cn } from "@/lib/utils";

interface MetricCardProps {
  label: string;
  value: string;
  percent: number;
  color?: string;
  className?: string;
}

export function MetricCard({ label, value, percent, color = "var(--color-primary)", className }: MetricCardProps) {
  return (
    <div className={cn("rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-5 transition-colors hover:border-[var(--color-border-hover)]", className)}>
      <span className="text-xs text-[var(--color-secondary)]">{label}</span>
      <div className="text-xl font-bold font-[family-name:var(--font-mono)] mt-1">{value}</div>
      <div className="mt-3">
        <div className="flex items-center justify-between mb-1">
          <div className="h-1.5 flex-1 bg-white/5 rounded-full overflow-hidden">
            <div className="h-full rounded-full transition-all duration-700" style={{ width: `${percent}%`, background: color }} />
          </div>
          <span className="text-xs font-[family-name:var(--font-mono)] text-[var(--color-secondary)] ml-2">{percent}%</span>
        </div>
      </div>
    </div>
  );
}
