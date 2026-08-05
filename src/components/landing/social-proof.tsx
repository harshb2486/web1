"use client";

import { AnimatedCounter } from "@/components/ui/animated-counter";

const stats = [
  { label: "Creators using CreatorOS", target: 12000, suffix: "+", prefix: "" },
  { label: "Videos analyzed", target: 50, suffix: "M+", prefix: "" },
  { label: "Predictions made", target: 2.4, suffix: "M+", prefix: "", decimals: 1 },
  { label: "Revenue tracked", target: 12.8, suffix: "M+", prefix: "$", decimals: 1 },
];

export function SocialProof() {
  return (
    <section className="py-16 border-y border-[var(--color-border)]">
      <div className="max-w-6xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {stats.map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-3xl md:text-4xl font-bold font-[family-name:var(--font-mono)] mb-1">
                <AnimatedCounter target={stat.target} prefix={stat.prefix} suffix={stat.suffix} decimals={stat.decimals} />
              </div>
              <p className="text-sm text-[var(--color-secondary)]">{stat.label}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
