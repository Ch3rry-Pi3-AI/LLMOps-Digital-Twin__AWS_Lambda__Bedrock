/**
 * Next.js Configuration File
 *
 * This configuration enables a static export build (`output: "export"`)
 * which is required when hosting the frontend using services that do not
 * support a Node.js runtime (e.g., GitHub Pages, S3 static hosting, etc.).
 *
 * It also disables Next.js' built-in image optimisation (`unoptimized: true`)
 * because static exports do not support the default image pipeline.
 *
 * This file ensures the Digital Twin frontend can be exported and deployed
 * reliably in lightweight or serverless environments.
 */

import type { NextConfig } from "next";

/**
 * Global Next.js configuration object.
 *
 * Properties:
 * - output: `"export"` enables static export instead of server rendering
 * - images.unoptimized: avoids Next.js attempting to optimise images
 *   (required because static export does not provide an optimisation server)
 */
const nextConfig: NextConfig = {
  output: "export",
  images: {
    unoptimized: true,
  },
};

export default nextConfig;