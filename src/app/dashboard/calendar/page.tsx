"use client";

import { useQuery } from "@tanstack/react-query";
import { CalendarSlots } from "@/components/dashboard/calendar-slots";
import { getCalendarSlots } from "@/services/dashboard.service";
import { Calendar } from "lucide-react";

export default function CalendarPage() {
  const { data: calendarSlots = [] } = useQuery({
    queryKey: ["calendar"],
    queryFn: getCalendarSlots,
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)] flex items-center gap-2">
          <Calendar size={20} className="text-[var(--color-primary)]" /> Best Times to Publish
        </h1>
        <p className="text-sm text-[var(--color-secondary)] mt-0.5">
          AI-optimized publish windows based on your audience&apos;s activity patterns.
        </p>
      </div>

      <div className="rounded-[var(--radius)] bg-[var(--color-primary)]/5 border border-[var(--color-primary)]/20 p-5">
        <p className="text-sm font-medium text-[var(--color-primary)] mb-1">AI Insight</p>
        <p className="text-sm text-[var(--color-secondary)]">
          Your audience peaks on Tuesday and Thursday evenings. Publishing between 7–9 PM EST gives you the highest engagement. Midday slots on weekdays also perform well for viewers watching during lunch breaks.
        </p>
      </div>

      <CalendarSlots slots={calendarSlots} />
    </div>
  );
}
