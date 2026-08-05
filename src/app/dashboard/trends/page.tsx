"use client";

import { useQuery } from "@tanstack/react-query";
import { TrendCard } from "@/components/dashboard/trend-card";
import { getTrends } from "@/services/dashboard.service";
import { TrendingUp, Filter } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function TrendsPage() {
  const { data: trends = [] } = useQuery({
    queryKey: ["trends"],
    queryFn: getTrends,
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)] flex items-center gap-2">
            <TrendingUp size={20} className="text-[var(--color-primary)]" /> Trending Topics
          </h1>
          <p className="text-sm text-[var(--color-secondary)] mt-0.5">
            Real-time signals from search, social, and forums.
          </p>
        </div>
        <Button variant="outline" size="sm">
          <Filter size={14} className="mr-1.5" /> Sort by Fit
        </Button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {trends.map((trend) => (
          <TrendCard key={trend.id} {...trend} />
        ))}
      </div>
    </div>
  );
}
