"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { NAV_ITEMS } from "@/lib/constants";
import { useAppStore } from "@/store/use-app-store";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { ChevronLeft, ChevronRight, X } from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();
  const { sidebarCollapsed, toggleSidebar, mobileSidebarOpen, setMobileSidebarOpen } = useAppStore();

  return (
    <>
      {/* Mobile backdrop */}
      {mobileSidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/50 lg:hidden"
          onClick={() => setMobileSidebarOpen(false)}
        />
      )}

      <aside
        className={cn(
          "fixed left-0 top-0 bottom-0 z-50 bg-[var(--color-surface)] border-r border-[var(--color-border)] flex flex-col transition-all duration-300",
          sidebarCollapsed ? "w-[68px]" : "w-[240px]",
          "max-lg:w-[280px] max-lg:-translate-x-full max-lg:data-[open=true]:translate-x-0"
        )}
        data-open={mobileSidebarOpen}
      >
        <div className={cn("flex items-center border-b border-[var(--color-border)]", sidebarCollapsed ? "justify-center h-16 px-2" : "justify-between h-16 px-4")}>
          {!sidebarCollapsed && (
            <Link href="/dashboard/overview" className="flex items-center gap-2.5" onClick={() => setMobileSidebarOpen(false)}>
              <div className="w-8 h-8 rounded-[var(--radius-xs)] bg-[var(--color-primary)] flex items-center justify-center">
                <span className="text-white font-bold text-sm font-[family-name:var(--font-heading)]">CI</span>
              </div>
              <span className="font-semibold font-[family-name:var(--font-heading)]">CreatorOS</span>
            </Link>
          )}
          {sidebarCollapsed && (
            <div className="w-8 h-8 rounded-[var(--radius-xs)] bg-[var(--color-primary)] flex items-center justify-center">
              <span className="text-white font-bold text-sm font-[family-name:var(--font-heading)]">CI</span>
            </div>
          )}
          <button
            onClick={() => setMobileSidebarOpen(false)}
            className="lg:hidden p-1 rounded text-[var(--color-muted)] hover:text-[var(--color-secondary)]"
          >
            <X size={18} />
          </button>
        </div>

        <nav className="flex-1 py-3 px-2 space-y-0.5 overflow-y-auto">
          {NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            const link = (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileSidebarOpen(false)}
                className={cn(
                  "flex items-center gap-3 rounded-[var(--radius-sm)] text-sm font-medium transition-colors",
                  sidebarCollapsed ? "justify-center h-10 w-10 mx-auto" : "h-10 px-3",
                  isActive
                    ? "bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
                    : "text-[var(--color-muted)] hover:text-[var(--color-secondary)] hover:bg-white/5"
                )}
              >
                <item.icon size={18} />
                {!sidebarCollapsed && <span>{item.label}</span>}
              </Link>
            );

            return sidebarCollapsed ? (
              <Tooltip key={item.href}>
                <TooltipTrigger asChild>{link}</TooltipTrigger>
                <TooltipContent side="right">{item.label}</TooltipContent>
              </Tooltip>
            ) : (
              link
            );
          })}
        </nav>

        <div className={cn("border-t border-[var(--color-border)] p-2", sidebarCollapsed && "flex justify-center")}>
          <Link
            href="/dashboard/settings"
            onClick={() => setMobileSidebarOpen(false)}
            className={cn(
              "flex items-center gap-3 rounded-[var(--radius-sm)] text-sm transition-colors hover:bg-white/5",
              sidebarCollapsed ? "justify-center h-10 w-10 mx-auto" : "px-3 py-2"
            )}
          >
            <Avatar className="h-8 w-8">
              <AvatarFallback>H</AvatarFallback>
            </Avatar>
            {!sidebarCollapsed && (
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">Harsh</p>
                <p className="text-xs text-[var(--color-muted)] truncate">TechWithHarsh</p>
              </div>
            )}
          </Link>
        </div>

        <button
          onClick={toggleSidebar}
          className="absolute -right-3 top-20 w-6 h-6 rounded-full bg-[var(--color-card)] border border-[var(--color-border)] items-center justify-center text-[var(--color-muted)] hover:text-[var(--color-secondary)] transition-colors hidden lg:flex"
        >
          {sidebarCollapsed ? <ChevronRight size={12} /> : <ChevronLeft size={12} />}
        </button>
      </aside>
    </>
  );
}
