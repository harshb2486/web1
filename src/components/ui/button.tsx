"use client";

import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap font-medium transition-colors duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--color-primary)]/50",
  {
    variants: {
      variant: {
        primary: "bg-[var(--color-primary)] hover:bg-[#4a6bff] text-white shadow-[0_2px_8px_rgba(91,124,255,0.25)]",
        ghost: "bg-transparent hover:bg-white/5 text-[var(--color-foreground)]",
        outline: "border border-[var(--color-border)] hover:border-[var(--color-border-hover)] hover:bg-white/5 text-[var(--color-foreground)]",
        danger: "bg-[var(--color-danger)] hover:bg-[#e6526f] text-white",
        accent: "bg-[var(--color-accent)] hover:bg-[#6a4bee] text-white",
      },
      size: {
        sm: "h-8 px-3 text-xs rounded-[var(--radius-xs)]",
        md: "h-10 px-4 text-sm rounded-[var(--radius-sm)]",
        lg: "h-12 px-6 text-base rounded-[var(--radius-sm)]",
        icon: "h-10 w-10 rounded-[var(--radius-sm)]",
      },
    },
    defaultVariants: { variant: "primary", size: "md" },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
    );
  }
);
Button.displayName = "Button";

export { Button, buttonVariants };
