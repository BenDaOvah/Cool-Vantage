import type { NextConfig } from "next";

// Cool Vantage static site: map clean directory URLs to their index.html files.
// The extracted site lives in /public and keeps its original root-relative links.
const staticPages = [
  "home",
  "about",
  "contact",
  "privacy",
  "services",
  "services/ac-repair",
  "services/ac-installation",
  "services/ac-maintenance",
  "services/commercial-refrigeration",
  "service-area/apopka-fl",
];

const rewrites = staticPages.map((page) => ({
  source: `/${page}`,
  destination: `/${page}/index.html`,
}));

const nextConfig: NextConfig = {
  output: "standalone",
  /* config options here */
  typescript: {
    ignoreBuildErrors: true,
  },
  reactStrictMode: false,
  allowedDevOrigins: ["**.space-z.ai"],
  async rewrites() {
    return {
      beforeFiles: rewrites,
      afterFiles: [],
      fallback: [],
    };
  },
};

export default nextConfig;
