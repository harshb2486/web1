"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { AICard } from "@/components/dashboard/ai-card";
import { Button } from "@/components/ui/button";
import { getRecommendations } from "@/services/dashboard.service";
import { Sparkles, Filter } from "lucide-react";

const CATEGORIES = ["All", "Video", "Blog", "Social", "Newsletter", "Podcast"];

export default function RecommendationsPage() {
  const [activeCategory, setActiveCategory] = useState("All");
  const { data: recommendations = [] } = useQuery({
    queryKey: ["recommendations"],
    queryFn: getRecommendations,
  });

  const filtered = activeCategory === "All" ? recommendations : recommendations.filter((r) => r.category === activeCategory);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)] flex items-center gap-2">
            <Sparkles size={20} className="text-[var(--color-primary)]" /> AI Recommendations
          </h1>
          <p className="text-sm text-[var(--color-secondary)] mt-0.5">
            Evidence-based content ideas tailored to your niche.
          </p>
        </div>
        <Button variant="outline" size="sm">
          <Filter size={14} className="mr-1.5" /> Filter
        </Button>
      </div>

      <div className="flex gap-2">
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
              activeCategory === cat
                ? "bg-[var(--color-primary)]/10 text-[var(--color-primary)] border border-[var(--color-primary)]/30"
                : "bg-white/5 text-[var(--color-muted)] border border-[var(--color-border)] hover:text-[var(--color-secondary)]"
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      <div className="space-y-4">
        {filtered.map((rec) => (
          <AICard key={rec.id} recommendation={rec} />
        ))}
        {filtered.length === 0 && (
          <div className="text-center py-12 text-[var(--color-muted)]">No recommendations in this category yet.</div>
        )}
      </div>
    </div>
  );
}
