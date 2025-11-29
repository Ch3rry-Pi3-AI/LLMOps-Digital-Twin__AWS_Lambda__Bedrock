# 🎨 Build and Deploy Frontend

This branch covers wiring your Digital Twin UI to the API Gateway endpoint, exporting the Next.js app as static files, and deploying the frontend to your S3 static site bucket.

## Step 1: Update Frontend API URL

Update `frontend/components/twin.tsx` – find the `fetch` call and change it from the local backend to your API Gateway URL:

```typescript
// Replace this line:
const response = await fetch('http://localhost:8000/chat', {

// With your API Gateway URL:
const response = await fetch('https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/chat', {
```

Make sure you keep the `/chat` path at the end of the URL.

## Step 2: Configure for Static Export

Update `frontend/next.config.ts` to enable static export:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'export',
  images: {
    unoptimized: true
  }
};

export default nextConfig;
```

This tells Next.js to generate a static export suitable for hosting on S3.

## Step 3: Build Static Export

From the `frontend` folder, run:

```bash
cd frontend
npm run build
```

This will create an `out` directory containing your static site.

**Note:** With Next.js 15.5 and the App Router, you must set `output: 'export'` in `next.config.ts` for the `out` directory to be generated.

## Step 4: Upload to S3

Use the AWS CLI to sync the static export to your frontend S3 bucket:

```bash
cd frontend
aws s3 sync out/ s3://YOUR-FRONTEND-BUCKET-NAME/ --delete
```

The `--delete` flag ensures old files that are no longer part of the latest build are removed from the bucket.

## Step 5: Test Your Static Site

1. In the AWS Console, go to your S3 **frontend bucket**
2. Open the **Properties** tab → **Static website hosting**
3. Click the **Bucket website endpoint** URL

Your Digital Twin should now load from S3 and call your Lambda-backed API Gateway endpoint.

<img src="img/demo/twin_demo.gif" width="100%">

