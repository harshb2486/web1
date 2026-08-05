"use client";

import { Card, CardContent } from "@/components/ui/card";
import { AlertTriangle, Clock, TrendingDown, Target } from "lucide-react";

const problems = [
  {
    icon: Clock,
    title: "Hours wasted researching",
    description: "You spend more time figuring out what to make than actually making it.",
  },
  {
    icon: TrendingDown,
    title: "Inconsistent performance",
    description: "Some videos hit, most don't. You have no idea why.",
  },
  {
    icon: Target,
    title: "No data-driven decisions",
    description: "You're guessing based on gut feeling while competitors use analytics.",
  },
  {
    icon: AlertTriangle,
    title: "Missing trends early",
    description: "By the time you notice a trend, it's already saturated.",
  },
];

export function Problem() {
  return (
    <section className="py-24">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-14">
          <h2 className="text-3xl md:text-4xl font-bold font-[family-name:var(--font-heading)] mb-4">
            Why creators struggle to grow
          </h2>
          <p className="text-[var(--color-secondary)] text-lg max-w-lg mx-auto">
            Most creators are making decisions based on guesswork, not data.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {problems.map((p, i) => (
            <Card key={i}>
              <CardContent className="pt-6">
                <div className="w-10 h-10 rounded-[var(--radius-sm)] bg-[var(--color-danger)]/10 flex items-center justify-center mb-4">
                  <p.icon size={20} className="text-[var(--color-danger)]" />
                </div>
                <h3 className="font-semibold mb-2">{p.title}</h3>
                <p className="text-sm text-[var(--color-secondary)] leading-relaxed">{p.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
