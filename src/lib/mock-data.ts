import type {
  User, Recommendation, Trend, Competitor, AudienceData,
  RevenueData, Sponsor, CalendarSlot, Notification, PricingTier,
} from "@/types";

export const currentUser: User = {
  id: "1",
  name: "Harsh",
  email: "harsh@example.com",
  channel: "TechWithHarsh",
  subscribers: 284000,
};

export const recommendations: Recommendation[] = [
  {
    id: "1",
    topic: "AI Agents for Students",
    confidence: 81,
    evidence: [
      "Search interest increasing for 12 consecutive days",
      "Similar creators are not covering this specific angle yet",
      "Your audience engages well with educational AI content",
    ],
    expectedViews: { low: 180000, high: 240000 },
    expectedRevenue: { low: 1200, high: 1800 },
    risks: ["Competition may increase within 2 weeks as topic gains traction"],
    similarContent: { title: "AI Tools Every Student Needs", views: 220000 },
    publishTime: "Tuesday 7:30 PM EST",
    category: "Education",
    potential: "high",
  },
  {
    id: "2",
    topic: "Build a SaaS in 24 Hours",
    confidence: 76,
    evidence: [
      "SaaS content has 3x higher engagement than average on your channel",
      "Similar video by Fireship got 1.2M views last month",
      "Your tutorial format performs above channel average",
    ],
    expectedViews: { low: 150000, high: 300000 },
    expectedRevenue: { low: 1000, high: 2200 },
    risks: ["High competition from established creators in this space"],
    similarContent: { title: "I Built a Startup in a Weekend", views: 185000 },
    publishTime: "Thursday 8:00 PM EST",
    category: "Business",
    potential: "high",
  },
  {
    id: "3",
    topic: "Why Python Is Losing Developers",
    confidence: 72,
    evidence: [
      "Rust and Go search volume up 45% year-over-year",
      "Contrarian takes on your channel get 2x average comments",
      "No major creator has covered this angle in the last 30 days",
    ],
    expectedViews: { low: 120000, high: 200000 },
    expectedRevenue: { low: 800, high: 1500 },
    risks: ["May attract negative engagement from Python community"],
    similarContent: { title: "Is JavaScript Dying?", views: 340000 },
    publishTime: "Tuesday 12:00 PM EST",
    category: "Tech",
    potential: "medium",
  },
  {
    id: "4",
    topic: "MCP Protocol Explained",
    confidence: 85,
    evidence: [
      "MCP search volume up 520% in 30 days",
      "Only 3 creators have covered this in depth",
      "Your API/protocol content averages 1.8x your channel mean",
    ],
    expectedViews: { low: 200000, high: 350000 },
    expectedRevenue: { low: 1400, high: 2500 },
    risks: ["Topic may be too niche for broad audience"],
    similarContent: { title: "REST vs GraphQL vs tRPC", views: 290000 },
    publishTime: "Thursday 7:00 PM EST",
    category: "Tech",
    potential: "high",
  },
];

export const trends: Trend[] = [
  { id: "1", topic: "AI Agents", growthDays: 18, competition: "Medium", fit: 88, searchVolume: "+340%", category: "Tech", country: "Global", direction: "up" },
  { id: "2", topic: "MCP Protocol", growthDays: 12, competition: "Low", fit: 82, searchVolume: "+520%", category: "Tech", country: "United States", direction: "up" },
  { id: "3", topic: "Rust for Web Dev", growthDays: 24, competition: "Low", fit: 74, searchVolume: "+180%", category: "Tech", country: "Global", direction: "up" },
  { id: "4", topic: "AI Video Generation", growthDays: 15, competition: "High", fit: 79, searchVolume: "+290%", category: "Creative", country: "India", direction: "up" },
  { id: "5", topic: "No-Code SaaS", growthDays: 21, competition: "Medium", fit: 71, searchVolume: "+160%", category: "Business", country: "United States", direction: "stable" },
  { id: "6", topic: "Local LLM Setup", growthDays: 9, competition: "Low", fit: 85, searchVolume: "+410%", category: "Tech", country: "Germany", direction: "up" },
  { id: "7", topic: "GPT-5 Features", growthDays: 6, competition: "High", fit: 90, searchVolume: "+680%", category: "AI", country: "Global", direction: "up" },
  { id: "8", topic: "TypeScript 6.0", growthDays: 3, competition: "Low", fit: 86, searchVolume: "+220%", category: "Tech", country: "Global", direction: "up" },
  { id: "9", topic: "AI Coding Agents", growthDays: 14, competition: "Medium", fit: 92, searchVolume: "+390%", category: "Tech", country: "United States", direction: "up" },
  { id: "10", topic: "Web Performance", growthDays: 30, competition: "Medium", fit: 77, searchVolume: "+95%", category: "Tech", country: "United Kingdom", direction: "stable" },
  { id: "11", topic: "DevOps Automation", growthDays: 20, competition: "Low", fit: 68, searchVolume: "+130%", category: "Tech", country: "Canada", direction: "up" },
  { id: "12", topic: "React Server Components", growthDays: 16, competition: "Medium", fit: 84, searchVolume: "+210%", category: "Tech", country: "Global", direction: "up" },
];

export const competitors: Competitor[] = [
  { id: "1", name: "Fireship", subscribers: 2800000, growthRate: 4.2, overlap: 72, engagement: 8.7, lastVideo: "AI Agents in 100 Seconds", lastVideoViews: 1800000, trending: true },
  { id: "2", name: "Web Dev Simplified", subscribers: 1500000, growthRate: 2.1, overlap: 68, engagement: 6.4, lastVideo: "Build a Full Stack App", lastVideoViews: 420000, trending: false },
  { id: "3", name: "Theo", subscribers: 920000, growthRate: 5.8, overlap: 78, engagement: 9.2, lastVideo: "React Is Dead?", lastVideoViews: 680000, trending: true },
  { id: "4", name: "Jack Herrington", subscribers: 480000, growthRate: 3.4, overlap: 81, engagement: 7.8, lastVideo: "TypeScript Tips You Need", lastVideoViews: 245000, trending: false },
  { id: "5", name: "ByteGrad", subscribers: 340000, growthRate: 6.1, overlap: 75, engagement: 8.9, lastVideo: "Next.js 15 Changes Everything", lastVideoViews: 310000, trending: true },
  { id: "6", name: "Josh Tried Coding", subscribers: 210000, growthRate: 7.3, overlap: 69, engagement: 9.5, lastVideo: "I Learned Rust in 30 Days", lastVideoViews: 180000, trending: true },
];

export const audienceData: AudienceData = {
  age: [
    { range: "13-17", percent: 8 },
    { range: "18-24", percent: 42 },
    { range: "25-34", percent: 35 },
    { range: "35-44", percent: 11 },
    { range: "45+", percent: 4 },
  ],
  countries: [
    { name: "India", percent: 38 },
    { name: "United States", percent: 22 },
    { name: "United Kingdom", percent: 12 },
    { name: "Germany", percent: 8 },
    { name: "Canada", percent: 6 },
    { name: "Others", percent: 14 },
  ],
  devices: [
    { name: "Mobile", percent: 58 },
    { name: "Desktop", percent: 38 },
    { name: "Tablet", percent: 4 },
  ],
  returningViewers: 67,
  avgWatchTime: "6.4 min",
  peakHours: ["7 PM", "9 PM", "12 PM"],
  insight: "Your 18-24 audience grows 3x faster than other age groups. Educational AI content performs best with this segment.",
};

export const revenueData: RevenueData = {
  current: 3240,
  breakdown: { ads: 1944, sponsorships: 972, affiliate: 194, membership: 130 },
  monthly: [
    { month: "Jan", revenue: 2800, ads: 1680, sponsors: 840 },
    { month: "Feb", revenue: 2950, ads: 1770, sponsors: 885 },
    { month: "Mar", revenue: 3100, ads: 1860, sponsors: 930 },
    { month: "Apr", revenue: 3240, ads: 1944, sponsors: 972 },
  ],
};

export const sponsors: Sponsor[] = [
  { id: "1", name: "Notion", category: "Productivity", fit: 94, estimatedPrice: "$2,500", responseProb: 78, status: "proposal" },
  { id: "2", name: "Vercel", category: "Developer Tools", fit: 91, estimatedPrice: "$3,200", responseProb: 82, status: "contacted" },
  { id: "3", name: "Linear", category: "Project Management", fit: 87, estimatedPrice: "$1,800", responseProb: 71, status: "lead" },
  { id: "4", name: "Supabase", category: "Backend", fit: 89, estimatedPrice: "$2,800", responseProb: 75, status: "contract" },
  { id: "5", name: "Raycast", category: "Productivity", fit: 86, estimatedPrice: "$1,500", responseProb: 73, status: "paid" },
];

export const calendarSlots: CalendarSlot[] = [
  { id: "1", day: "Monday", time: "12:00 PM", score: 72, reason: "Lunch break audience peak", type: "good" },
  { id: "2", day: "Tuesday", time: "7:30 PM", score: 94, reason: "Highest engagement window for your audience", type: "recommended" },
  { id: "3", day: "Tuesday", time: "12:00 PM", score: 68, reason: "Secondary peak", type: "okay" },
  { id: "4", day: "Wednesday", time: "9:00 PM", score: 81, reason: "Evening scroll traffic", type: "good" },
  { id: "5", day: "Thursday", time: "8:00 PM", score: 88, reason: "Pre-weekend content consumption peak", type: "recommended" },
  { id: "6", day: "Friday", time: "12:00 PM", score: 65, reason: "Lower engagement, but less competition", type: "okay" },
  { id: "7", day: "Saturday", time: "10:00 AM", score: 70, reason: "Weekend morning browse", type: "good" },
  { id: "8", day: "Sunday", time: "7:00 PM", score: 76, reason: "Sunday evening prep for the week", type: "good" },
];

export const notifications: Notification[] = [
  { id: "1", title: "Trend detected", message: "AI Agents trending with +340% search volume", type: "info", time: "2 min ago", read: false },
  { id: "2", title: "Competitor alert", message: "Theo published a new video with 680K views", type: "info", time: "15 min ago", read: false },
  { id: "3", title: "Revenue milestone", message: "You've earned $3,240 this month", type: "success", time: "1 hour ago", read: true },
  { id: "4", title: "Sponsor response", message: "Notion responded to your pitch", type: "success", time: "3 hours ago", read: true },
];

export const DASHBOARD_STATS = {
  totalViews: "1.2M",
  revenue: "$3,240",
  engagementRate: "7.8%",
  subscribers: "284K",
};

export const REVENUE_CHART_DATA = [
  { month: "May", revenue: 2100 },
  { month: "Jun", revenue: 2400 },
  { month: "Jul", revenue: 2200 },
  { month: "Aug", revenue: 2800 },
  { month: "Sep", revenue: 2600 },
  { month: "Oct", revenue: 2950 },
  { month: "Nov", revenue: 3100 },
  { month: "Dec", revenue: 3000 },
  { month: "Jan", revenue: 2800 },
  { month: "Feb", revenue: 2950 },
  { month: "Mar", revenue: 3100 },
  { month: "Apr", revenue: 3240 },
];

export const pricingTiers: PricingTier[] = [
  {
    name: "Starter",
    price: "Free",
    period: "",
    description: "For creators getting started",
    features: ["1 channel", "5 recommendations/month", "Basic trend data", "Community support"],
    cta: "Get Started",
  },
  {
    name: "Pro",
    price: "$29",
    period: "/month",
    description: "For growing creators",
    features: ["3 channels", "Unlimited recommendations", "Advanced analytics", "Competitor tracking", "Revenue predictions", "Priority support"],
    cta: "Start Pro Trial",
    highlighted: true,
  },
  {
    name: "Business",
    price: "$79",
    period: "/month",
    description: "For teams and agencies",
    features: ["10 channels", "Everything in Pro", "Team collaboration", "Custom reports", "API access", "Dedicated support"],
    cta: "Start Business Trial",
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    description: "For large organizations",
    features: ["Unlimited channels", "Everything in Business", "Custom integrations", "SLA", "Account manager", "On-premise option"],
    cta: "Contact Sales",
  },
];
