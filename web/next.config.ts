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
  async redirects() {
    return [
      {
        source: '/mobile',
        destination: '/mobile/',
        permanent: true,
      }
    ];
  },
  async rewrites() {
    return [
      {
        source: '/mobile/:path*',
        destination: '/mobile/index.html',
      },
    ];
  },
};

export default nextConfig;
