"use client";

import { useQuery } from "@tanstack/react-query";
import { CompetitorsTable } from "@/components/dashboard/competitors-table";
import { getCompetitors } from "@/services/dashboard.service";
import { Users } from "lucide-react";

export default function CompetitorsPage() {
  const { data: competitors = [] } = useQuery({
    queryKey: ["competitors"],
    queryFn: getCompetitors,
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)] flex items-center gap-2">
          <Users size={20} className="text-[var(--color-primary)]" /> Competitor Analysis
        </h1>
        <p className="text-sm text-[var(--color-secondary)] mt-0.5">
          Track what similar creators are publishing and identify opportunities.
        </p>
      </div>
      <CompetitorsTable data={competitors} />
    </div>
  );
}
