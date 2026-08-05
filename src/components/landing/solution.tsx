"use client";

import { Card, CardContent } from "@/components/ui/card";
import { BarChart3, Lightbulb, Calendar } from "lucide-react";

const steps = [
  {
    icon: BarChart3,
    step: "1",
    title: "Connect your channels",
    description: "We analyze your content history, audience demographics, and engagement patterns.",
  },
  {
    icon: Lightbulb,
    step: "2",
    title: "Get recommendations",
    description: "AI suggests topics with evidence, expected outcomes, competition analysis, and timing.",
  },
  {
    icon: Calendar,
    step: "3",
    title: "Publish with confidence",
    description: "Follow the calendar, track results, and let the AI learn what works for your audience.",
  },
];

export function Solution() {
  return (
    <section className="py-24 bg-[var(--color-surface)]/50">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-14">
          <h2 className="text-3xl md:text-4xl font-bold font-[family-name:var(--font-heading)] mb-4">
            How CreatorOS works
          </h2>
          <p className="text-[var(--color-secondary)] text-lg max-w-lg mx-auto">
            Three steps from guessing to knowing.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {steps.map((s, i) => (
            <div key={i} className="relative">
              {i < steps.length - 1 && (
                <div className="hidden md:block absolute top-10 left-[calc(50%+40px)] w-[calc(100%-40px)] h-px bg-gradient-to-r from-[var(--color-primary)]/30 to-transparent" />
              )}
              <Card>
                <CardContent className="pt-6 text-center">
                  <div className="w-16 h-16 rounded-full bg-[var(--color-primary)]/10 flex items-center justify-center mx-auto mb-4 relative">
                    <s.icon size={24} className="text-[var(--color-primary)]" />
                    <span className="absolute -top-1 -right-1 w-6 h-6 rounded-full bg-[var(--color-primary)] text-white text-xs flex items-center justify-center font-bold">
                      {s.step}
                    </span>
                  </div>
                  <h3 className="font-semibold mb-2 font-[family-name:var(--font-heading)]">{s.title}</h3>
                  <p className="text-sm text-[var(--color-secondary)] leading-relaxed">{s.description}</p>
                </CardContent>
              </Card>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
