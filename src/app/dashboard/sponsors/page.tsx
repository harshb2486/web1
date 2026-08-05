"use client";

import { useQuery } from "@tanstack/react-query";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { getSponsors } from "@/services/dashboard.service";
import { Handshake, ExternalLink } from "lucide-react";

const statusColor: Record<string, "default" | "primary" | "success" | "warning" | "danger"> = {
  lead: "default",
  contacted: "primary",
  proposal: "warning",
  contract: "primary",
  invoice: "warning",
  paid: "success",
};

export default function SponsorsPage() {
  const { data: sponsors = [] } = useQuery({
    queryKey: ["sponsors"],
    queryFn: getSponsors,
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)] flex items-center gap-2">
          <Handshake size={20} className="text-[var(--color-primary)]" /> Sponsor Pipeline
        </h1>
        <p className="text-sm text-[var(--color-secondary)] mt-0.5">
          Track and manage your brand partnership opportunities.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {sponsors.map((s) => (
          <div key={s.id} className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-5 transition-colors hover:border-[var(--color-border-hover)]">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-lg">{s.name}</h3>
              <Badge variant={statusColor[s.status]}>{s.status}</Badge>
            </div>
            <div className="text-xs text-[var(--color-secondary)] mb-3">{s.category}</div>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <p className="text-xs text-[var(--color-secondary)]">Fit Score</p>
                <div className="flex items-center gap-2 mt-1">
                  <div className="w-16 h-1.5 bg-white/5 rounded-full overflow-hidden">
                    <div className="h-full bg-[var(--color-primary)] rounded-full" style={{ width: `${s.fit}%` }} />
                  </div>
                  <span className="font-[family-name:var(--font-mono)] text-xs">{s.fit}%</span>
                </div>
              </div>
              <div>
                <p className="text-xs text-[var(--color-secondary)]">Est. Price</p>
                <p className="font-[family-name:var(--font-mono)] font-medium mt-1">{s.estimatedPrice}</p>
              </div>
              <div>
                <p className="text-xs text-[var(--color-secondary)]">Response Prob.</p>
                <p className="font-[family-name:var(--font-mono)] mt-1">{s.responseProb}%</p>
              </div>
            </div>
            <div className="mt-4 flex gap-2">
              <Button size="sm" variant="ghost" className="flex-1">
                View Details
              </Button>
              <Button size="sm" variant="ghost">
                <ExternalLink size={14} />
              </Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
