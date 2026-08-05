"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Check, ChevronRight, ChevronLeft } from "lucide-react";
import { CREATOR_TYPES, PLATFORMS, GOALS } from "@/lib/constants";
import { useAppStore } from "@/store/use-app-store";
import { completeOnboarding } from "@/services/auth.service";

const steps = [1, 2, 3, 4, 5] as const;

export function Wizard() {
  const router = useRouter();
  const { setOnboardingComplete } = useAppStore();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({
    creatorType: "",
    platforms: [] as string[],
    goals: [] as string[],
    niche: "",
    theme: "dark" as string,
  });

  const toggleItem = (key: "platforms" | "goals", value: string) => {
    setData((prev) => ({
      ...prev,
      [key]: prev[key].includes(value)
        ? prev[key].filter((v) => v !== value)
        : [...prev[key], value],
    }));
  };

  const canNext = () => {
    if (step === 1) return data.creatorType !== "";
    if (step === 2) return data.platforms.length > 0;
    if (step === 3) return data.goals.length > 0;
    if (step === 4) return data.niche.length > 0;
    return true;
  };

  const handleFinish = async () => {
    setLoading(true);
    try {
      await completeOnboarding(data);
    } catch {
      // proceed even if API call fails
    }
    setOnboardingComplete(true);
    router.push("/dashboard/overview");
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-6">
      <div className="w-full max-w-lg">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold font-[family-name:var(--font-heading)]">Set up your workspace</h1>
          <p className="text-sm text-[var(--color-secondary)] mt-1">Step {step} of 5</p>
        </div>

        <div className="flex gap-2 mb-8">
          {steps.map((s) => (
            <div key={s} className={`flex-1 h-1 rounded-full ${s <= step ? "bg-[var(--color-primary)]" : "bg-white/10"}`} />
          ))}
        </div>

        <Card>
          <CardContent className="pt-6">
            {step === 1 && (
              <div>
                <h2 className="font-semibold mb-1 font-[family-name:var(--font-heading)]">What type of creator are you?</h2>
                <p className="text-sm text-[var(--color-secondary)] mb-4">Select the one that best describes you.</p>
                <div className="grid grid-cols-2 gap-3">
                  {CREATOR_TYPES.map((type) => (
                    <button
                      key={type}
                      onClick={() => setData((p) => ({ ...p, creatorType: type }))}
                      className={`p-4 rounded-[var(--radius-sm)] text-left text-sm font-medium transition-all ${
                        data.creatorType === type
                          ? "bg-[var(--color-primary)]/10 border border-[var(--color-primary)]/30 text-[var(--color-primary)]"
                          : "bg-white/5 border border-[var(--color-border)] hover:border-[var(--color-border-hover)]"
                      }`}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {step === 2 && (
              <div>
                <h2 className="font-semibold mb-1 font-[family-name:var(--font-heading)]">Which platforms do you use?</h2>
                <p className="text-sm text-[var(--color-secondary)] mb-4">Select all that apply.</p>
                <div className="grid grid-cols-2 gap-3">
                  {PLATFORMS.map((platform) => (
                    <button
                      key={platform}
                      onClick={() => toggleItem("platforms", platform)}
                      className={`p-4 rounded-[var(--radius-sm)] text-left text-sm font-medium transition-all flex items-center justify-between ${
                        data.platforms.includes(platform)
                          ? "bg-[var(--color-primary)]/10 border border-[var(--color-primary)]/30 text-[var(--color-primary)]"
                          : "bg-white/5 border border-[var(--color-border)] hover:border-[var(--color-border-hover)]"
                      }`}
                    >
                      {platform}
                      {data.platforms.includes(platform) && <Check size={16} />}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {step === 3 && (
              <div>
                <h2 className="font-semibold mb-1 font-[family-name:var(--font-heading)]">What are your goals?</h2>
                <p className="text-sm text-[var(--color-secondary)] mb-4">Select all that apply.</p>
                <div className="grid grid-cols-2 gap-3">
                  {GOALS.map((goal) => (
                    <button
                      key={goal}
                      onClick={() => toggleItem("goals", goal)}
                      className={`p-4 rounded-[var(--radius-sm)] text-left text-sm font-medium transition-all flex items-center justify-between ${
                        data.goals.includes(goal)
                          ? "bg-[var(--color-primary)]/10 border border-[var(--color-primary)]/30 text-[var(--color-primary)]"
                          : "bg-white/5 border border-[var(--color-border)] hover:border-[var(--color-border-hover)]"
                      }`}
                    >
                      {goal}
                      {data.goals.includes(goal) && <Check size={16} />}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {step === 4 && (
              <div>
                <h2 className="font-semibold mb-1 font-[family-name:var(--font-heading)]">What's your niche?</h2>
                <p className="text-sm text-[var(--color-secondary)] mb-4">This helps us find relevant trends and competitors.</p>
                <input
                  value={data.niche}
                  onChange={(e) => setData((p) => ({ ...p, niche: e.target.value }))}
                  placeholder="e.g., Web Development, AI, Finance"
                  className="flex h-10 w-full rounded-[var(--radius-sm)] bg-white/5 border border-[var(--color-border)] px-3 py-2 text-sm text-[var(--color-foreground)] placeholder-[var(--color-muted)] focus:outline-none focus:border-[var(--color-primary)]/50"
                />
              </div>
            )}

            {step === 5 && (
              <div>
                <h2 className="font-semibold mb-1 font-[family-name:var(--font-heading)]">Choose your theme</h2>
                <p className="text-sm text-[var(--color-secondary)] mb-4">You can change this later in settings.</p>
                <div className="grid grid-cols-3 gap-3">
                  {["dark", "light", "system"].map((theme) => (
                    <button
                      key={theme}
                      onClick={() => setData((p) => ({ ...p, theme }))}
                      className={`p-4 rounded-[var(--radius-sm)] text-center text-sm font-medium capitalize transition-all ${
                        data.theme === theme
                          ? "bg-[var(--color-primary)]/10 border border-[var(--color-primary)]/30 text-[var(--color-primary)]"
                          : "bg-white/5 border border-[var(--color-border)] hover:border-[var(--color-border-hover)]"
                      }`}
                    >
                      {theme}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        <div className="flex items-center justify-between mt-6">
          <Button
            variant="ghost"
            onClick={() => setStep((s) => Math.max(1, s - 1))}
            disabled={step === 1}
          >
            <ChevronLeft size={16} className="mr-1" /> Back
          </Button>
          {step < 5 ? (
            <Button onClick={() => setStep((s) => s + 1)} disabled={!canNext()}>
              Next <ChevronRight size={16} className="ml-1" />
            </Button>
          ) : (
            <Button onClick={handleFinish} disabled={loading}>
              {loading ? "Setting up..." : "Get Started"} <ChevronRight size={16} className="ml-1" />
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
