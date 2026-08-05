"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, label, error, ...props }, ref) => {
    return (
      <div className="space-y-1.5">
        {label && (
          <label className="text-sm font-medium text-[var(--color-secondary)]">{label}</label>
        )}
        <textarea
          className={cn(
            "flex min-h-[80px] w-full rounded-[var(--radius-sm)] bg-white/5 border border-[var(--color-border)] px-3 py-2 text-sm text-[var(--color-foreground)] placeholder-[var(--color-muted)]",
            "focus:outline-none focus:border-[var(--color-primary)]/50 focus:ring-1 focus:ring-[var(--color-primary)]/20",
            "transition-colors duration-200 resize-none",
            error && "border-[var(--color-danger)]",
            className
          )}
          ref={ref}
          {...props}
        />
        {error && <p className="text-xs text-[var(--color-danger)]">{error}</p>}
      </div>
    );
  }
);
Textarea.displayName = "Textarea";

export { Textarea };
