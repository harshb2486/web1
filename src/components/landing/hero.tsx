"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Lightbulb, TrendingUp, Users, Calendar } from "lucide-react";

export function Hero() {
  return (
    <section className="relative min-h-screen flex items-center pt-24 pb-16">
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] rounded-full bg-[var(--color-primary)]/5 blur-[100px]" />
        <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] rounded-full bg-[var(--color-accent)]/5 blur-[80px]" />
      </div>

      <div className="max-w-6xl mx-auto px-6 grid lg:grid-cols-2 gap-12 items-center relative z-10">
        <div>
          <Badge variant="primary" className="mb-6">AI-Powered Content Intelligence</Badge>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold font-[family-name:var(--font-heading)] leading-tight mb-6">
            Stop guessing what to{" "}
            <span className="bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-accent)] bg-clip-text text-transparent">
              publish
            </span>.
          </h1>
          <p className="text-lg text-[var(--color-secondary)] mb-8 max-w-lg leading-relaxed">
            CreatorOS analyzes your audience, competitors, and trends to tell you exactly what to create, when to publish, and what results to expect.
          </p>
          <div className="flex flex-col sm:flex-row gap-3">
            <Link href="/auth/signup">
              <Button size="lg">Start Free Trial</Button>
            </Link>
            <Link href="#features">
              <Button variant="ghost" size="lg">See how it works</Button>
            </Link>
          </div>
        </div>

        <div className="relative">
          <Card className="overflow-hidden">
            <CardContent className="p-0">
              <div className="bg-[var(--color-surface)] p-4 border-b border-[var(--color-border)]">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-2 h-2 rounded-full bg-[var(--color-success)]" />
                  <span className="text-xs text-[var(--color-secondary)]">AI Recommendation</span>
                </div>
                <h3 className="font-semibold font-[family-name:var(--font-heading)]">AI Agents for Students</h3>
                <div className="flex items-center gap-3 mt-2">
                  <Badge variant="success">81% confidence</Badge>
                  <Badge variant="primary">Education</Badge>
                </div>
              </div>
              <div className="p-4 space-y-3">
                <div className="flex items-center gap-3 text-sm">
                  <Lightbulb size={14} className="text-[var(--color-warning)]" />
                  <span className="text-[var(--color-secondary)]">Search interest up 340% in 12 days</span>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <TrendingUp size={14} className="text-[var(--color-success)]" />
                  <span className="text-[var(--color-secondary)]">Expected views: 180K–240K</span>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <Users size={14} className="text-[var(--color-primary)]" />
                  <span className="text-[var(--color-secondary)]">Low competition, high audience fit</span>
                </div>
                <div className="flex items-center gap-3 text-sm">
                  <Calendar size={14} className="text-[var(--color-accent)]" />
                  <span className="text-[var(--color-secondary)]">Best time: Tuesday 7:30 PM</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
