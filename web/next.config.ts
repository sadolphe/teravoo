import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  output: "standalone",
  typescript: {
    // !! WARN !!
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    ignoreBuildErrors: true,
  },
  async rewrites() {
    return [
      {
        source: '/mobile',
        destination: '/mobile/index.html',
      },
      // Handle client-side routing inside the mobile app if needed
      // (Though hash routing is default for Flutter Web, so this might be redundant but safe)
    ];
  },
};

export default nextConfig;
