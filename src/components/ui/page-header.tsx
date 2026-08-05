"use client";

import { ReactNode } from "react";
import { cn } from "@/lib/utils";

interface PageHeaderProps {
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}

export function PageHeader({ title, description, action, className }: PageHeaderProps) {
  return (
    <div className={cn("flex items-center justify-between mb-6", className)}>
      <div>
        <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)]">{title}</h1>
        {description && <p className="text-sm text-[var(--color-secondary)] mt-1">{description}</p>}
      </div>
      {action}
    </div>
  );
}
