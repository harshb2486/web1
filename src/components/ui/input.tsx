"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, label, error, icon, ...props }, ref) => {
    return (
      <div className="space-y-1.5">
        {label && (
          <label className="text-sm font-medium text-[var(--color-secondary)]">{label}</label>
        )}
        <div className="relative">
          {icon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--color-muted)]">{icon}</div>
          )}
          <input
            type={type}
            className={cn(
              "flex h-10 w-full rounded-[var(--radius-sm)] bg-white/5 border border-[var(--color-border)] px-3 py-2 text-sm text-[var(--color-foreground)] placeholder-[var(--color-muted)]",
              "focus:outline-none focus:border-[var(--color-primary)]/50 focus:ring-1 focus:ring-[var(--color-primary)]/20",
              "transition-colors duration-200",
              icon && "pl-10",
              error && "border-[var(--color-danger)]",
              className
            )}
            ref={ref}
            {...props}
          />
        </div>
        {error && <p className="text-xs text-[var(--color-danger)]">{error}</p>}
      </div>
    );
  }
);
Input.displayName = "Input";

export { Input };
