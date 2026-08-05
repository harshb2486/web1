export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  channel: string;
  subscribers: number;
}

export interface Recommendation {
  id: string;
  topic: string;
  confidence: number;
  evidence: string[];
  expectedViews: { low: number; high: number };
  expectedRevenue: { low: number; high: number };
  risks: string[];
  similarContent: { title: string; views: number };
  publishTime: string;
  category: string;
  potential: "high" | "medium" | "low";
}

export interface Trend {
  id: string;
  topic: string;
  growthDays: number;
  competition: "Low" | "Medium" | "High";
  fit: number;
  searchVolume: string;
  category: string;
  country: string;
  direction: "up" | "down" | "stable";
}

export interface Competitor {
  id: string;
  name: string;
  subscribers: number;
  growthRate: number;
  overlap: number;
  engagement: number;
  lastVideo: string;
  lastVideoViews: number;
  trending: boolean;
}

export interface AudienceData {
  age: { range: string; percent: number }[];
  countries: { name: string; percent: number }[];
  devices: { name: string; percent: number }[];
  returningViewers: number;
  avgWatchTime: string;
  peakHours: string[];
  insight: string;
}

export interface RevenueData {
  current: number;
  breakdown: { ads: number; sponsorships: number; affiliate: number; membership: number };
  monthly: { month: string; revenue: number; ads: number; sponsors: number }[];
}

export interface Sponsor {
  id: string;
  name: string;
  category: string;
  fit: number;
  estimatedPrice: string;
  responseProb: number;
  status: "lead" | "contacted" | "proposal" | "contract" | "invoice" | "paid";
}

export interface CalendarSlot {
  id: string;
  day: string;
  time: string;
  score: number;
  reason: string;
  type: "recommended" | "good" | "okay";
}

export interface Notification {
  id: string;
  title: string;
  message: string;
  type: "info" | "success" | "warning";
  time: string;
  read: boolean;
}

export interface PricingTier {
  name: string;
  price: string;
  period: string;
  description: string;
  features: string[];
  cta: string;
  highlighted?: boolean;
}

export type OnboardingStep = 1 | 2 | 3 | 4 | 5;

export interface OnboardingData {
  creatorType: string;
  platforms: string[];
  goals: string[];
  niche: string;
  theme: "dark" | "light" | "system";
}
