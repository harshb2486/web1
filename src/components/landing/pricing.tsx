"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Check } from "lucide-react";
import { pricingTiers } from "@/lib/mock-data";
import Link from "next/link";

export function Pricing() {
  return (
    <section id="pricing" className="py-24 bg-[var(--color-surface)]/50">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-14">
          <h2 className="text-3xl md:text-4xl font-bold font-[family-name:var(--font-heading)] mb-4">
            Simple, transparent pricing
          </h2>
          <p className="text-[var(--color-secondary)] text-lg max-w-lg mx-auto">
            Start free, upgrade when you're ready.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {pricingTiers.map((tier) => (
            <Card key={tier.name} className={tier.highlighted ? "border-[var(--color-primary)]/30 shadow-[0_0_30px_rgba(91,124,255,0.1)]" : ""}>
              <CardContent className="pt-6">
                {tier.highlighted && (
                  <Badge variant="primary" className="mb-3">Most Popular</Badge>
                )}
                <h3 className="font-semibold text-lg font-[family-name:var(--font-heading)]">{tier.name}</h3>
                <div className="mt-3 mb-4">
                  <span className="text-3xl font-bold font-[family-name:var(--font-mono)]">{tier.price}</span>
                  {tier.period && <span className="text-sm text-[var(--color-secondary)]">{tier.period}</span>}
                </div>
                <p className="text-sm text-[var(--color-secondary)] mb-4">{tier.description}</p>
                <ul className="space-y-2 mb-6">
                  {tier.features.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-sm">
                      <Check size={14} className="text-[var(--color-success)] shrink-0" />
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
                <Link href="/auth/signup">
                  <Button variant={tier.highlighted ? "primary" : "outline"} className="w-full">
                    {tier.cta}
                  </Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
