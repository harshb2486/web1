"use client";

import { useQuery } from "@tanstack/react-query";
import { getAudience } from "@/services/dashboard.service";
import { Users } from "lucide-react";

export default function AudiencePage() {
  const { data: audienceData } = useQuery({
    queryKey: ["audience"],
    queryFn: getAudience,
  });

  if (!audienceData) return null;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)] flex items-center gap-2">
          <Users size={20} className="text-[var(--color-primary)]" /> Audience Insights
        </h1>
        <p className="text-sm text-[var(--color-secondary)] mt-0.5">
          Deep dive into who&apos;s watching and when they&apos;re active.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-5">
          <p className="text-xs text-[var(--color-secondary)] mb-2">Returning Viewers</p>
          <div className="text-2xl font-bold font-[family-name:var(--font-mono)]">{audienceData.returningViewers}%</div>
        </div>
        <div className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-5">
          <p className="text-xs text-[var(--color-secondary)] mb-2">Avg. Watch Time</p>
          <div className="text-2xl font-bold font-[family-name:var(--font-mono)]">{audienceData.avgWatchTime}</div>
        </div>
        <div className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-5">
          <p className="text-xs text-[var(--color-secondary)] mb-2">Peak Hours</p>
          <div className="flex gap-2 mt-1">
            {audienceData.peakHours.map((h) => (
              <span key={h} className="text-xs px-2 py-1 rounded-full bg-white/5 border border-[var(--color-border)]">{h}</span>
            ))}
          </div>
        </div>
        <div className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-5">
          <p className="text-xs text-[var(--color-secondary)] mb-2">Top Devices</p>
          <div className="space-y-1.5 mt-2">
            {audienceData.devices.map((d) => (
              <div key={d.name} className="flex items-center justify-between text-xs">
                <span>{d.name}</span>
                <span className="font-[family-name:var(--font-mono)]">{d.percent}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-6">
          <h2 className="text-lg font-semibold font-[family-name:var(--font-heading)] mb-4">Age Distribution</h2>
          <div className="space-y-3">
            {audienceData.age.map((a) => (
              <div key={a.range} className="flex items-center gap-3">
                <span className="text-xs text-[var(--color-secondary)] w-12">{a.range}</span>
                <div className="flex-1 h-2 bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-[var(--color-primary)] rounded-full" style={{ width: `${a.percent}%` }} />
                </div>
                <span className="text-xs font-[family-name:var(--font-mono)] w-8 text-right">{a.percent}%</span>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-6">
          <h2 className="text-lg font-semibold font-[family-name:var(--font-heading)] mb-4">Countries</h2>
          <div className="space-y-3">
            {audienceData.countries.map((c) => (
              <div key={c.name} className="flex items-center gap-3">
                <span className="text-xs text-[var(--color-secondary)] w-28 truncate">{c.name}</span>
                <div className="flex-1 h-2 bg-white/5 rounded-full overflow-hidden">
                  <div className="h-full bg-[var(--color-accent)] rounded-full" style={{ width: `${c.percent}%` }} />
                </div>
                <span className="text-xs font-[family-name:var(--font-mono)] w-8 text-right">{c.percent}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="rounded-[var(--radius)] bg-[var(--color-primary)]/5 border border-[var(--color-primary)]/20 p-5">
        <p className="text-sm font-medium text-[var(--color-primary)] mb-1">AI Insight</p>
        <p className="text-sm text-[var(--color-secondary)]">{audienceData.insight}</p>
      </div>
    </div>
  );
}
