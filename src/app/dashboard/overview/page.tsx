"use client";

import { useQuery } from "@tanstack/react-query";
import { StatCard } from "@/components/dashboard/stat-card";
import { AICard } from "@/components/dashboard/ai-card";
import { RevenueChart } from "@/components/dashboard/revenue-chart";
import { Button } from "@/components/ui/button";
import { getDashboardStats, getRecommendations } from "@/services/dashboard.service";
import { TrendingUp, Eye, DollarSign, Users, Bell, Sparkles } from "lucide-react";
import Link from "next/link";

export default function OverviewPage() {
  const { data: stats } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: getDashboardStats,
  });

  const { data: recommendations } = useQuery({
    queryKey: ["recommendations"],
    queryFn: getRecommendations,
  });

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)]">Good evening, Harsh</h1>
          <p className="text-sm text-[var(--color-secondary)] mt-0.5">Here&apos;s your content intelligence at a glance.</p>
        </div>
        <Button variant="primary" className="gap-2">
          <Sparkles size={14} /> Get AI Suggestion
        </Button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon={<TrendingUp size={16} />} label="Total Views" value={stats?.totalViews ?? "—"} change="+18% vs last week" changeType="positive" />
        <StatCard icon={<DollarSign size={16} />} label="Revenue This Month" value={stats?.revenue ?? "—"} change="+12% vs last month" changeType="positive" />
        <StatCard icon={<Eye size={16} />} label="Engagement Rate" value={stats?.engagementRate ?? "—"} change="+0.3% this week" changeType="positive" />
        <StatCard icon={<Users size={16} />} label="Subscribers" value={stats?.subscribers ?? "—"} change="+340 this week" changeType="positive" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div className="lg:col-span-3 rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold font-[family-name:var(--font-heading)]">Revenue Trend</h2>
            <span className="text-xs text-[var(--color-secondary)]">Last 12 months</span>
          </div>
          <RevenueChart />
        </div>
        <div className="lg:col-span-2 rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold font-[family-name:var(--font-heading)]">Upcoming Content</h2>
            <Bell size={16} className="text-[var(--color-muted)]" />
          </div>
          <div className="space-y-3">
            <div className="p-3 rounded-[var(--radius-sm)] bg-white/[0.03] border border-[var(--color-border)]">
              <p className="text-sm font-medium">AI Agents Explained</p>
              <p className="text-xs text-[var(--color-secondary)] mt-0.5">YouTube • Tomorrow, 10:00 AM</p>
            </div>
            <div className="p-3 rounded-[var(--radius-sm)] bg-white/[0.03] border border-[var(--color-border)]">
              <p className="text-sm font-medium">React 20 Features</p>
              <p className="text-xs text-[var(--color-secondary)] mt-0.5">Blog • Thu, 2:00 PM</p>
            </div>
            <div className="p-3 rounded-[var(--radius-sm)] bg-white/[0.03] border border-[var(--color-border)]">
              <p className="text-sm font-medium">Creator Economy Trends</p>
              <p className="text-xs text-[var(--color-secondary)] mt-0.5">LinkedIn • Fri, 9:00 AM</p>
            </div>
          </div>
        </div>
      </div>

      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold font-[family-name:var(--font-heading)]">AI Recommendations</h2>
          <Link href="/dashboard/recommendations">
            <Button variant="ghost" size="sm">View All →</Button>
          </Link>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {recommendations?.slice(0, 2).map((rec) => (
            <AICard key={rec.id} recommendation={rec} />
          ))}
        </div>
      </div>
    </div>
  );
}
