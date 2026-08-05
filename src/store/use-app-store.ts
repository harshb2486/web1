import { create } from "zustand";
import { getAccessToken, clearTokens } from "@/services/api";

interface AppState {
  sidebarCollapsed: boolean;
  toggleSidebar: () => void;
  mobileSidebarOpen: boolean;
  setMobileSidebarOpen: (open: boolean) => void;
  commandPaletteOpen: boolean;
  setCommandPaletteOpen: (open: boolean) => void;
  theme: "dark" | "light" | "system";
  setTheme: (theme: "dark" | "light" | "system") => void;
  onboardingComplete: boolean;
  setOnboardingComplete: (complete: boolean) => void;
  isAuthenticated: boolean;
  login: () => void;
  logout: () => void;
  checkAuth: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  sidebarCollapsed: false,
  toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),
  mobileSidebarOpen: false,
  setMobileSidebarOpen: (open) => set({ mobileSidebarOpen: open }),
  commandPaletteOpen: false,
  setCommandPaletteOpen: (open) => set({ commandPaletteOpen: open }),
  theme: "dark",
  setTheme: (theme) => set({ theme }),
  onboardingComplete: false,
  setOnboardingComplete: (complete) => set({ onboardingComplete: complete }),
  isAuthenticated: false,
  login: () => set({ isAuthenticated: true }),
  logout: () => {
    clearTokens();
    set({ isAuthenticated: false, onboardingComplete: false });
  },
  checkAuth: () => {
    const token = getAccessToken();
    set({ isAuthenticated: !!token });
  },
}));
