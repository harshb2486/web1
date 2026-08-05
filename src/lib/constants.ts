import {
  Home, Lightbulb, TrendingUp, Users, BarChart3,
  DollarSign, Building2, Calendar, Settings, Sparkles,
} from "lucide-react";

export const NAV_ITEMS = [
  { href: "/dashboard/overview", icon: Home, label: "Overview" },
  { href: "/dashboard/recommendations", icon: Lightbulb, label: "Recommendations" },
  { href: "/dashboard/trends", icon: TrendingUp, label: "Trends" },
  { href: "/dashboard/competitors", icon: Users, label: "Competitors" },
  { href: "/dashboard/audience", icon: BarChart3, label: "Audience" },
  { href: "/dashboard/revenue", icon: DollarSign, label: "Revenue" },
  { href: "/dashboard/sponsors", icon: Building2, label: "Sponsors" },
  { href: "/dashboard/calendar", icon: Calendar, label: "Calendar" },
  { href: "/dashboard/settings", icon: Settings, label: "Settings" },
] as const;

export const PLATFORMS = ["YouTube", "TikTok", "Instagram", "LinkedIn", "X"] as const;

export const CREATOR_TYPES = [
  "YouTuber",
  "TikToker",
  "Podcaster",
  "Streamer",
  "Blogger",
  "Newsletter Writer",
] as const;

export const GOALS = [
  "Increase Views",
  "Grow Revenue",
  "Get Sponsors",
  "Gain Subscribers",
  "Improve Engagement",
  "Save Time",
] as const;

export const TREND_CATEGORIES = [
  "All", "Tech", "AI", "Business", "Creative", "Education", "Lifestyle",
] as const;

export const COUNTRIES = [
  "All", "India", "United States", "United Kingdom", "Germany", "Canada", "Australia",
] as const;
