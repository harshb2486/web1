"use client";

import { TrendingUp, TrendingDown, Minus } from "lucide-react";

interface TrendCardProps {
  topic: string;
  searchVolume: string;
  growthDays: number;
  competition: "Low" | "Medium" | "High";
  fit: number;
  direction: "up" | "down" | "stable";
}

const competitionColor = { Low: "text-[var(--color-success)]", Medium: "text-[var(--color-warning)]", High: "text-[var(--color-danger)]" } as const;

const DirectionIcon = { up: TrendingUp, down: TrendingDown, stable: Minus } as const;

export function TrendCard({ topic, searchVolume, growthDays, competition, fit, direction }: TrendCardProps) {
  const Icon = DirectionIcon[direction];

  return (
    <div className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-5 transition-colors hover:border-[var(--color-border-hover)]">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-medium">{topic}</h3>
        <Icon size={16} className={direction === "up" ? "text-[var(--color-success)]" : direction === "down" ? "text-[var(--color-danger)]" : "text-[var(--color-muted)]"} />
      </div>
      <div className="grid grid-cols-2 gap-3 text-sm">
        <div>
          <p className="text-xs text-[var(--color-secondary)]">Search volume</p>
          <p className="font-[family-name:var(--font-mono)] font-medium text-[var(--color-success)]">{searchVolume}</p>
        </div>
        <div>
          <p className="text-xs text-[var(--color-secondary)]">Growth</p>
          <p className="font-[family-name:var(--font-mono)]">{growthDays} days</p>
        </div>
        <div>
          <p className="text-xs text-[var(--color-secondary)]">Competition</p>
          <p className={`font-medium ${competitionColor[competition]}`}>{competition}</p>
        </div>
        <div>
          <p className="text-xs text-[var(--color-secondary)]">Your fit</p>
          <div className="flex items-center gap-2">
            <div className="w-12 h-1.5 bg-white/5 rounded-full overflow-hidden">
              <div className="h-full bg-[var(--color-primary)] rounded-full" style={{ width: `${fit}%` }} />
            </div>
            <span className="font-[family-name:var(--font-mono)] text-xs">{fit}%</span>
          </div>
        </div>
      </div>
    </div>
  );
}
