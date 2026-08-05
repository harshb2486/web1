"use client";

import { Badge } from "@/components/ui/badge";
import type { Competitor } from "@/types";

interface Props {
  data: Competitor[];
}

export function CompetitorsTable({ data }: Props) {
  return (
    <div className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[var(--color-border)]">
              <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-secondary)] uppercase tracking-wider">Creator</th>
              <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-secondary)] uppercase tracking-wider">Subscribers</th>
              <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-secondary)] uppercase tracking-wider">Growth</th>
              <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-secondary)] uppercase tracking-wider">Overlap</th>
              <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-secondary)] uppercase tracking-wider">Engagement</th>
              <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-secondary)] uppercase tracking-wider">Last Video</th>
              <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-secondary)] uppercase tracking-wider">Trending</th>
            </tr>
          </thead>
          <tbody>
            {data.map((c) => (
              <tr key={c.id} className="border-b border-[var(--color-border)] hover:bg-white/[0.02] transition-colors">
                <td className="px-5 py-3.5 font-medium">{c.name}</td>
                <td className="px-5 py-3.5 font-[family-name:var(--font-mono)]">{(c.subscribers / 1000).toFixed(0)}K</td>
                <td className="px-5 py-3.5 font-[family-name:var(--font-mono)]">
                  <span className="text-[var(--color-success)]">+{c.growthRate}%</span>
                </td>
                <td className="px-5 py-3.5 font-[family-name:var(--font-mono)]">{c.overlap}%</td>
                <td className="px-5 py-3.5 font-[family-name:var(--font-mono)]">{c.engagement}%</td>
                <td className="px-5 py-3.5 text-[var(--color-secondary)] truncate max-w-[200px]">{c.lastVideo}</td>
                <td className="px-5 py-3.5">
                  {c.trending ? (
                    <Badge variant="success">Trending</Badge>
                  ) : (
                    <span className="text-[var(--color-muted)] text-xs">—</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
