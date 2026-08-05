"use client";

import { useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { Search, Bell, Sparkles, Command, Menu, User, Settings, CreditCard, LogOut, Info, DollarSign, Handshake, Sun, Moon } from "lucide-react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { useCommandPalette } from "@/hooks/use-command-palette";
import { useAppStore } from "@/store/use-app-store";
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator } from "@/components/ui/dropdown-menu";
import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import { getNotifications } from "@/services/dashboard.service";
import type { Notification } from "@/types";

const typeIcon: Record<Notification["type"], React.ReactNode> = {
  info: <Info size={14} className="text-[var(--color-primary)]" />,
  success: <DollarSign size={14} className="text-[var(--color-success)]" />,
  warning: <Handshake size={14} className="text-[var(--color-warning)]" />,
};

export function Topbar() {
  const router = useRouter();
  const { setOpen } = useCommandPalette();
  const { setMobileSidebarOpen, logout, theme, setTheme } = useAppStore();

  const { data: notifications = [] } = useQuery({
    queryKey: ["notifications"],
    queryFn: getNotifications,
  });

  const unreadCount = notifications.filter((n) => !n.read).length;

  const handleLogout = () => {
    logout();
    router.push("/auth/login");
  };

  return (
    <header className="h-16 border-b border-[var(--color-border)] bg-[var(--color-surface)]/50 backdrop-blur-sm flex items-center justify-between px-4 lg:px-6 sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <button
          onClick={() => setMobileSidebarOpen(true)}
          className="lg:hidden p-2 rounded-[var(--radius-sm)] text-[var(--color-muted)] hover:text-[var(--color-secondary)] hover:bg-white/5 transition-colors"
        >
          <Menu size={18} />
        </button>
        <button
          onClick={() => setOpen(true)}
          className="flex items-center gap-3 h-9 px-4 rounded-[var(--radius-sm)] bg-white/5 border border-[var(--color-border)] text-sm text-[var(--color-muted)] hover:border-[var(--color-border-hover)] transition-colors cursor-pointer w-48 lg:w-72"
        >
          <Search size={14} />
          <span className="hidden sm:inline">Search...</span>
          <kbd className="ml-auto hidden sm:flex items-center gap-0.5 text-[10px] bg-white/5 px-1.5 py-0.5 rounded font-[family-name:var(--font-mono)]">
            <Command size={10} /> K
          </kbd>
        </button>
      </div>

      <div className="flex items-center gap-2 lg:gap-4">
        <button
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="p-2 rounded-[var(--radius-sm)] text-[var(--color-muted)] hover:text-[var(--color-secondary)] hover:bg-white/5 transition-colors"
          title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
        >
          {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <Popover>
          <PopoverTrigger className="relative p-2 rounded-[var(--radius-sm)] text-[var(--color-muted)] hover:text-[var(--color-secondary)] hover:bg-white/5 transition-colors">
            <Bell size={18} />
            {unreadCount > 0 && (
              <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-[var(--color-danger)]" />
            )}
          </PopoverTrigger>
          <PopoverContent align="end" className="w-80 p-0">
            <div className="flex items-center justify-between px-4 py-3 border-b border-[var(--color-border)]">
              <h3 className="font-semibold text-sm">Notifications</h3>
            </div>
            <div className="max-h-80 overflow-y-auto">
              {notifications.map((n) => (
                <div
                  key={n.id}
                  className={`flex items-start gap-3 px-4 py-3 border-b border-[var(--color-border)] last:border-0 transition-colors hover:bg-white/[0.02] ${
                    !n.read ? "bg-[var(--color-primary)]/5" : ""
                  }`}
                >
                  <div className="mt-0.5 shrink-0">{typeIcon[n.type]}</div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium">{n.title}</p>
                    <p className="text-xs text-[var(--color-secondary)] mt-0.5 line-clamp-2">{n.message}</p>
                    <p className="text-[10px] text-[var(--color-muted)] mt-1">{n.time}</p>
                  </div>
                  {!n.read && <span className="w-2 h-2 rounded-full bg-[var(--color-primary)] mt-1.5 shrink-0" />}
                </div>
              ))}
            </div>
          </PopoverContent>
        </Popover>
        <button className="hidden sm:flex items-center gap-2 h-9 px-3 rounded-[var(--radius-sm)] bg-white/5 border border-[var(--color-border)] text-sm text-[var(--color-secondary)] hover:bg-white/[0.08] transition-colors">
          <Sparkles size={14} className="text-[var(--color-primary)]" />
          <span>Quick AI</span>
        </button>

        <DropdownMenu>
          <DropdownMenuTrigger className="focus:outline-none">
            <Avatar className="h-8 w-8 cursor-pointer">
              <AvatarFallback>H</AvatarFallback>
            </Avatar>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-48">
            <div className="px-2 py-1.5">
              <p className="text-sm font-medium">Harsh</p>
              <p className="text-xs text-[var(--color-muted)]">TechWithHarsh</p>
            </div>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => router.push("/dashboard/settings")}>
              <User size={14} className="mr-2" /> Profile
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => router.push("/dashboard/settings")}>
              <Settings size={14} className="mr-2" /> Settings
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => router.push("/dashboard/revenue")}>
              <CreditCard size={14} className="mr-2" /> Billing
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={handleLogout} className="text-[var(--color-danger)] focus:text-[var(--color-danger)]">
              <LogOut size={14} className="mr-2" /> Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
