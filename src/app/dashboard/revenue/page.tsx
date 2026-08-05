"use client";

import { useQuery } from "@tanstack/react-query";
import { RevenueChart } from "@/components/dashboard/revenue-chart";
import { getRevenue } from "@/services/dashboard.service";
import { DollarSign } from "lucide-react";

const breakdownLabels: Record<string, string> = {
  ads: "Ad Revenue",
  sponsorships: "Sponsorships",
  affiliate: "Affiliate",
  membership: "Membership",
};

export default function RevenuePage() {
  const { data: revenueData } = useQuery({
    queryKey: ["revenue"],
    queryFn: getRevenue,
  });

  if (!revenueData) return null;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)] flex items-center gap-2">
          <DollarSign size={20} className="text-[var(--color-primary)]" /> Revenue
        </h1>
        <p className="text-sm text-[var(--color-secondary)] mt-0.5">
          Track earnings across all your revenue streams.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {Object.entries(revenueData.breakdown).map(([key, val]) => (
          <div key={key} className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-5">
            <p className="text-xs text-[var(--color-secondary)]">{breakdownLabels[key]}</p>
            <p className="text-xl font-bold font-[family-name:var(--font-mono)] mt-1">${val.toLocaleString()}</p>
          </div>
        ))}
      </div>

      <div className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold font-[family-name:var(--font-heading)]">Revenue Trend</h2>
          <div className="text-sm text-[var(--color-secondary)]">
            Total this month: <span className="font-[family-name:var(--font-mono)] font-medium text-[var(--color-success)]">${revenueData.current.toLocaleString()}</span>
          </div>
        </div>
        <RevenueChart />
      </div>

      <div className="rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[var(--color-border)]">
              <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-secondary)] uppercase tracking-wider">Month</th>
              <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-secondary)] uppercase tracking-wider">Total</th>
              <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-secondary)] uppercase tracking-wider">Ads</th>
              <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-secondary)] uppercase tracking-wider">Sponsors</th>
            </tr>
          </thead>
          <tbody>
            {revenueData.monthly.map((m) => (
              <tr key={m.month} className="border-b border-[var(--color-border)] hover:bg-white/[0.02] transition-colors">
                <td className="px-5 py-3.5 font-medium">{m.month}</td>
                <td className="px-5 py-3.5 font-[family-name:var(--font-mono)] font-medium">${m.revenue.toLocaleString()}</td>
                <td className="px-5 py-3.5 font-[family-name:var(--font-mono)]">${m.ads.toLocaleString()}</td>
                <td className="px-5 py-3.5 font-[family-name:var(--font-mono)]">${m.sponsors.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
