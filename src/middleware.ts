import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (pathname.startsWith("/api/")) {
    const backendUrl = new URL(pathname, "http://localhost:8000");
    backendUrl.search = request.nextUrl.search;
    return NextResponse.rewrite(backendUrl);
  }
}

export const config = {
  matcher: "/api/:path*",
};
