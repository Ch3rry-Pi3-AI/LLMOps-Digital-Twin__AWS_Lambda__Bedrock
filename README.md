# 🪣 Create S3 Buckets

## Step 1: Create Memory Bucket

1. In AWS Console, search for **S3**
2. Click **Create bucket**
3. Configuration:

   * Bucket name: `twin-memory-[random-suffix]` (must be globally unique)
   * Region: same as your Lambda (e.g., `us-east-1`)
   * Leave all other settings as default
4. Click **Create bucket**
5. Copy the exact bucket name

## Step 2: Update Lambda Environment

1. Go back to **Lambda** → **Configuration** → **Environment variables**
2. Update `S3_BUCKET` with your bucket name
3. Click **Save**

## Step 3: Add S3 Permissions to Lambda

1. In **Lambda** → **Configuration** → **Permissions**
2. Click the execution role name
3. Click **Add permissions** → **Attach policies**
4. Search for and select **AmazonS3FullAccess**
5. Click **Attach policies**

## Step 4: Create Frontend Bucket

1. In S3, click **Create bucket**
2. Configuration:

   * Bucket name: `twin-frontend-[random-suffix]`
   * Region: same as Lambda
   * **Uncheck** “Block all public access”
   * Check the acknowledgment box
3. Click **Create bucket**

## Step 5: Enable Static Website Hosting

1. Click your frontend bucket
2. Go to the **Properties** tab
3. Scroll to **Static website hosting** → **Edit**
4. Enable static website hosting:

   * Hosting type: **Host a static website**
   * Index document: `index.html`
   * Error document: `404.html`
5. Click **Save changes**

<img src="img/aws_lambda/static_hosting.png" width="100%">

6. Copy the **Bucket website endpoint** shown at the top of that section

## Step 6: Configure Bucket Policy

1. Go to the **Permissions** tab
2. Under **Bucket policy**, click **Edit**
3. Add this policy (replace `YOUR-BUCKET-NAME`):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
        }
    ]
}
```

4. Click **Save changes**