"use client";

import { Badge } from "@/components/ui/badge";
import type { CalendarSlot } from "@/types";

interface Props {
  slots: CalendarSlot[];
}

const typeStyle: Record<CalendarSlot["type"], { border: string; badge: "success" | "primary" | "default"; label: string }> = {
  recommended: { border: "border-[var(--color-success)]/30 bg-[var(--color-success)]/5", badge: "success", label: "Best" },
  good: { border: "border-[var(--color-primary)]/20", badge: "primary", label: "Good" },
  okay: { border: "border-[var(--color-border)]", badge: "default", label: "Okay" },
};

const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

export function CalendarSlots({ slots }: Props) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {days.map((day) => {
        const daySlots = slots.filter((s) => s.day === day);
        return (
          <div key={day} className="space-y-3">
            <h3 className="text-sm font-semibold text-[var(--color-secondary)] uppercase tracking-wider">{day}</h3>
            {daySlots.length === 0 && (
              <div className="rounded-[var(--radius-sm)] border border-dashed border-[var(--color-border)] p-4 text-center text-xs text-[var(--color-muted)]">
                No data
              </div>
            )}
            {daySlots.map((slot) => {
              const style = typeStyle[slot.type];
              return (
                <div
                  key={slot.id}
                  className={`rounded-[var(--radius-sm)] border p-4 transition-colors hover:border-[var(--color-border-hover)] ${style.border}`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium font-[family-name:var(--font-mono)]">{slot.time}</span>
                    <Badge variant={style.badge}>{style.label}</Badge>
                  </div>
                  <div className="mb-2">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[10px] text-[var(--color-muted)] uppercase tracking-wider">Score</span>
                      <span className="text-xs font-[family-name:var(--font-mono)] font-medium">{slot.score}</span>
                    </div>
                    <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-700"
                        style={{
                          width: `${slot.score}%`,
                          background: slot.type === "recommended" ? "var(--color-success)" : slot.type === "good" ? "var(--color-primary)" : "var(--color-muted)",
                        }}
                      />
                    </div>
                  </div>
                  <p className="text-xs text-[var(--color-secondary)]">{slot.reason}</p>
                </div>
              );
            })}
          </div>
        );
      })}
    </div>
  );
}
