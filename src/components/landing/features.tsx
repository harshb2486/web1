"use client";

import { Card, CardContent } from "@/components/ui/card";
import {
  Brain, TrendingUp, Users, DollarSign, Calendar, Target,
  BarChart3, Lightbulb, Sparkles, Eye, Clock, Zap,
} from "lucide-react";

const features = [
  { icon: Brain, title: "AI Recommendations", description: "Get evidence-based content suggestions with confidence scores and reasoning." },
  { icon: TrendingUp, title: "Trend Scanner", description: "Track emerging topics across platforms before they peak." },
  { icon: Users, title: "Competitor Analysis", description: "Monitor competitor growth, engagement, and content strategy." },
  { icon: DollarSign, title: "Revenue Prediction", description: "See projected earnings for each content idea before you create it." },
  { icon: Calendar, title: "Smart Calendar", description: "AI picks the optimal publish time based on your audience data." },
  { icon: Target, title: "Audience Insights", description: "Deep demographics, watch time patterns, and behavior analysis." },
  { icon: BarChart3, title: "Performance Tracking", description: "Compare predicted vs actual results and learn what works." },
  { icon: Lightbulb, title: "Content Ideas", description: "Infinite content ideas ranked by potential and audience fit." },
  { icon: Sparkles, title: "AI Copilot", description: "Ask questions about your content strategy in natural language." },
  { icon: Eye, title: "Competitor Gaps", description: "Find topics your competitors haven't covered yet." },
  { icon: Clock, title: "Optimal Timing", description: "Publish when your audience is most active and engaged." },
  { icon: Zap, title: "Real-time Alerts", description: "Get notified about trending topics and competitor moves." },
];

export function Features() {
  return (
    <section id="features" className="py-24">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-14">
          <h2 className="text-3xl md:text-4xl font-bold font-[family-name:var(--font-heading)] mb-4">
            Everything you need to grow
          </h2>
          <p className="text-[var(--color-secondary)] text-lg max-w-lg mx-auto">
            A complete toolkit for data-driven content decisions.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f, i) => (
            <Card key={i} className="group">
              <CardContent className="pt-6">
                <div className="w-10 h-10 rounded-[var(--radius-sm)] bg-[var(--color-primary)]/10 flex items-center justify-center mb-4 group-hover:bg-[var(--color-primary)]/20 transition-colors">
                  <f.icon size={20} className="text-[var(--color-primary)]" />
                </div>
                <h3 className="font-semibold mb-2">{f.title}</h3>
                <p className="text-sm text-[var(--color-secondary)] leading-relaxed">{f.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
