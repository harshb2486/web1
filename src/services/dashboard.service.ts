import { apiRequest } from "./api";
import type {
  Recommendation,
  Trend,
  Competitor,
  AudienceData,
  RevenueData,
  Sponsor,
  CalendarSlot,
  Notification,
} from "@/types";

interface DashboardStats {
  totalViews: string;
  revenue: string;
  engagementRate: string;
  subscribers: string;
}

export async function getDashboardStats(): Promise<DashboardStats> {
  return apiRequest<DashboardStats>("/dashboard");
}

export async function getRecommendations(): Promise<Recommendation[]> {
  return apiRequest<Recommendation[]>("/recommendations");
}

export async function getTrends(): Promise<Trend[]> {
  return apiRequest<Trend[]>("/trends");
}

export async function getCompetitors(): Promise<Competitor[]> {
  return apiRequest<Competitor[]>("/competitors");
}

export async function getAudience(): Promise<AudienceData> {
  return apiRequest<AudienceData>("/audience");
}

export async function getRevenue(): Promise<RevenueData & { chartData: { month: string; revenue: number }[] }> {
  return apiRequest("/revenue");
}

export async function getSponsors(): Promise<Sponsor[]> {
  return apiRequest<Sponsor[]>("/sponsors");
}

export async function getCalendarSlots(): Promise<CalendarSlot[]> {
  return apiRequest<CalendarSlot[]>("/calendar");
}

export async function getNotifications(): Promise<Notification[]> {
  return apiRequest<Notification[]>("/notifications");
}
