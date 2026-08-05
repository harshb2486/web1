"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Settings, User, Bell, Shield, CreditCard, LogOut } from "lucide-react";
import { useState } from "react";

const tabs = [
  { id: "profile", label: "Profile", icon: User },
  { id: "notifications", label: "Notifications", icon: Bell },
  { id: "security", label: "Security", icon: Shield },
  { id: "billing", label: "Billing", icon: CreditCard },
] as const;

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState("profile");

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)] flex items-center gap-2">
          <Settings size={20} className="text-[var(--color-primary)]" /> Settings
        </h1>
        <p className="text-sm text-[var(--color-secondary)] mt-0.5">Manage your account preferences.</p>
      </div>

      <div className="flex gap-6">
        <div className="w-48 shrink-0">
          <div className="space-y-1">
            {tabs.map((t) => (
              <button
                key={t.id}
                onClick={() => setActiveTab(t.id)}
                className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-[var(--radius-sm)] text-sm font-medium transition-colors ${
                  activeTab === t.id
                    ? "bg-[var(--color-primary)]/10 text-[var(--color-primary)]"
                    : "text-[var(--color-muted)] hover:text-[var(--color-secondary)] hover:bg-white/5"
                }`}
              >
                <t.icon size={16} /> {t.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex-1 rounded-[var(--radius)] bg-[var(--color-card)] border border-[var(--color-border)] p-6">
          {activeTab === "profile" && (
            <div className="space-y-5">
              <h2 className="text-lg font-semibold font-[family-name:var(--font-heading)]">Profile</h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Full Name</Label>
                  <Input defaultValue="Harsh" />
                </div>
                <div className="space-y-2">
                  <Label>Channel Name</Label>
                  <Input defaultValue="TechWithHarsh" />
                </div>
              </div>
              <div className="space-y-2">
                <Label>Email</Label>
                <Input defaultValue="harsh@example.com" type="email" />
              </div>
              <div className="space-y-2">
                <Label>Niche</Label>
                <Input defaultValue="Web Development & AI" />
              </div>
              <Button variant="primary">Save Changes</Button>
            </div>
          )}

          {activeTab === "notifications" && (
            <div className="space-y-5">
              <h2 className="text-lg font-semibold font-[family-name:var(--font-heading)]">Notifications</h2>
              {[
                { label: "Trend alerts", desc: "Get notified when new trends match your niche" },
                { label: "Competitor updates", desc: "When competitors publish new content" },
                { label: "Revenue reports", desc: "Weekly revenue summary emails" },
                { label: "AI recommendations", desc: "New content suggestions" },
              ].map((n) => (
                <div key={n.label} className="flex items-center justify-between py-3 border-b border-[var(--color-border)] last:border-0">
                  <div>
                    <p className="text-sm font-medium">{n.label}</p>
                    <p className="text-xs text-[var(--color-secondary)]">{n.desc}</p>
                  </div>
                  <button className="w-10 h-5 rounded-full bg-[var(--color-primary)] relative transition-colors">
                    <span className="absolute top-0.5 right-0.5 w-4 h-4 rounded-full bg-white transition-transform" />
                  </button>
                </div>
              ))}
            </div>
          )}

          {activeTab === "security" && (
            <div className="space-y-5">
              <h2 className="text-lg font-semibold font-[family-name:var(--font-heading)]">Security</h2>
              <div className="space-y-2">
                <Label>Current Password</Label>
                <Input type="password" placeholder="Enter current password" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>New Password</Label>
                  <Input type="password" placeholder="Enter new password" />
                </div>
                <div className="space-y-2">
                  <Label>Confirm Password</Label>
                  <Input type="password" placeholder="Confirm new password" />
                </div>
              </div>
              <Button variant="primary">Update Password</Button>
            </div>
          )}

          {activeTab === "billing" && (
            <div className="space-y-5">
              <h2 className="text-lg font-semibold font-[family-name:var(--font-heading)]">Billing</h2>
              <div className="p-4 rounded-[var(--radius-sm)] bg-white/[0.03] border border-[var(--color-border)]">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium">Pro Plan</p>
                    <p className="text-sm text-[var(--color-secondary)]">$29/month • Renews May 15, 2026</p>
                  </div>
                  <Badge variant="primary">Active</Badge>
                </div>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm">Change Plan</Button>
                <Button variant="ghost" size="sm" className="text-[var(--color-danger)]">Cancel Subscription</Button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
