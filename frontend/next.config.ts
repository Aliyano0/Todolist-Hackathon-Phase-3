import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  /* config options here */
  typedRoutes: true,
  reactStrictMode: true,
  poweredByHeader: false, // Remove X-Powered-By header for security

  // Security headers for production
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
    ];
  },
};

export default nextConfig;