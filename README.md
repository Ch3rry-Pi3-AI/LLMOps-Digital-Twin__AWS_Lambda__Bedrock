# 🛠️ **AWS Environment Setup — Branch Overview**

This branch prepares the **initial AWS environment** required for deploying the **llmops-digital-twin** backend and its future serverless components (Lambda, API Gateway, S3, CloudFront, DynamoDB).
The focus is on configuring AWS credentials, creating the correct IAM user/group structure, and ensuring your project root contains the environment variables needed for deployment.



## Part 1: Project Environment Configuration

### **Step 1: Create a `.env` File in the Project Root**

Inside the root of your project (`twin/.env`), create the following file:

```bash
# AWS Configuration
AWS_ACCOUNT_ID=your_aws_account_id
DEFAULT_AWS_REGION=us-east-1

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Project Configuration
PROJECT_NAME=twin
```

Replace:

* **your_aws_account_id** → your *12-digit* AWS account number
* **your_openai_api_key** → your actual OpenAI API key

This `.env` file will later be used by deployment scripts and AWS CLI for building Lambda packages and configuring infrastructure.



## Part 2: Configure AWS Console Access

### **Step 2: Sign In to the AWS Console**

1. Visit **aws.amazon.com**
2. Sign in as **root user**
   (This is only needed for initial setup—afterwards you will switch to IAM user-only access.)



## Part 3: Create IAM Group and Permissions

### **Step 3: Create the IAM User Group**

1. In the AWS Console, go to **IAM**
2. Navigate to **User groups**
3. Select **Create group**
4. Name it: **TwinAccess**
5. Attach the following AWS managed policies:

| Policy                          | Purpose                                             |
| ------------------------------- | --------------------------------------------------- |
| `AWSLambda_FullAccess`          | Deploy & manage Lambda functions                    |
| `AmazonS3FullAccess`            | S3 buckets + object storage for memory or artifacts |
| `AmazonAPIGatewayAdministrator` | Create & manage REST APIs for your Lambda           |
| `CloudFrontFullAccess`          | Prepare for optional frontend CDN deployment        |
| `IAMReadOnlyAccess`             | Allows viewing roles required by other services     |
| `AmazonDynamoDBFullAccess_v2`   | Required for Day 4 enhancements                     |

6. Click **Create group**

This group now contains all permissions the Digital Twin project will require across upcoming branches.


## Part 4: Add IAM User to the Group

### **Step 4: Add Your Existing IAM User**

1. In **IAM → Users**, select your Week 1 user: **`aiengineer`**
2. Click **Add to groups**
3. Select the `TwinAccess` group
4. Confirm by clicking **Add to groups**

Your IAM user now has all needed permissions for serverless deployment.



## Part 5: Switch to IAM-Only Sign-In

### **Step 5: Sign In as IAM User**

1. Log out of the root account
2. Sign in again, this time as:

* **Username:** `aiengineer`
* **Password:** (your IAM user password)

From this point forward, *all AWS project work should be done under the IAM user*, keeping your root credentials secure.
