"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Hero } from "@/components/landing/hero";
import { SocialProof } from "@/components/landing/social-proof";
import { Problem } from "@/components/landing/problem";
import { Solution } from "@/components/landing/solution";
import { Features } from "@/components/landing/features";
import { Pricing } from "@/components/landing/pricing";

export default function MarketingPage() {
  return (
    <>
      <Hero />
      <SocialProof />
      <Problem />
      <Solution />
      <Features />
      <Pricing />
    </>
  );
}
