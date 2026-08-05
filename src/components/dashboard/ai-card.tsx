"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Calendar, AlertTriangle, ArrowRight } from "lucide-react";
import type { Recommendation } from "@/types";

interface AICardProps {
  recommendation: Recommendation;
}

export function AICard({ recommendation: rec }: AICardProps) {
  const potentialColor = { high: "success", medium: "warning", low: "danger" } as const;

  return (
    <div className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-6 transition-colors hover:border-[var(--color-border-hover)]">
      <div className="flex items-center gap-3 mb-3">
        <Badge variant="primary">{rec.category}</Badge>
        <Badge variant={potentialColor[rec.potential]}>{rec.potential} potential</Badge>
        <span className="ml-auto text-sm font-[family-name:var(--font-mono)] text-[var(--color-secondary)]">
          {rec.confidence}% confidence
        </span>
      </div>

      <h3 className="text-lg font-semibold font-[family-name:var(--font-heading)] mb-3">{rec.topic}</h3>

      <div className="mb-4">
        <p className="text-xs font-medium text-[var(--color-secondary)] mb-2 uppercase tracking-wider">Why we recommend this</p>
        <ul className="space-y-1.5">
          {rec.evidence.map((e, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-[var(--color-secondary)]">
              <span className="text-[var(--color-success)] mt-0.5">•</span>
              {e}
            </li>
          ))}
        </ul>
      </div>

      <div className="mb-4">
        <p className="text-xs font-medium text-[var(--color-secondary)] mb-2 uppercase tracking-wider">Risks</p>
        <ul className="space-y-1.5">
          {rec.risks.map((r, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-[var(--color-secondary)]">
              <AlertTriangle size={12} className="text-[var(--color-warning)] mt-0.5 shrink-0" />
              {r}
            </li>
          ))}
        </ul>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-[var(--color-border)]">
        <div>
          <p className="text-xs text-[var(--color-secondary)] mb-1">Expected views</p>
          <p className="font-[family-name:var(--font-mono)] font-medium text-sm">
            {(rec.expectedViews.low / 1000).toFixed(0)}K–{(rec.expectedViews.high / 1000).toFixed(0)}K
          </p>
        </div>
        <div>
          <p className="text-xs text-[var(--color-secondary)] mb-1">Expected revenue</p>
          <p className="font-[family-name:var(--font-mono)] font-medium text-sm">
            ${rec.expectedRevenue.low.toLocaleString()}–${rec.expectedRevenue.high.toLocaleString()}
          </p>
        </div>
        <div>
          <p className="text-xs text-[var(--color-secondary)] mb-1">Similar content</p>
          <p className="text-sm truncate">{rec.similarContent.title}</p>
        </div>
        <div>
          <p className="text-xs text-[var(--color-secondary)] mb-1">Publish time</p>
          <p className="font-[family-name:var(--font-mono)] font-medium text-sm flex items-center gap-1">
            <Calendar size={12} className="text-[var(--color-primary)]" />
            {rec.publishTime}
          </p>
        </div>
      </div>

      <div className="mt-4 flex gap-2">
        <Button size="sm" variant="ghost">
          Add to Calendar
        </Button>
        <Button size="sm" variant="ghost">
          View full analysis <ArrowRight size={14} className="ml-1" />
        </Button>
      </div>
    </div>
  );
}
