# 🌐 Set Up API Gateway

## Step 1: Create HTTP API with Integration

1. In AWS Console, search for **API Gateway**
2. Click **Create API**
3. Choose **HTTP API** → **Build**
4. **Step 1 – Create and configure integrations:**

   * Click **Add integration**
   * Integration type: **Lambda**
   * Lambda function: select `twin-api`
   * API name: `twin-api-gateway`
   * Click **Next**

## Step 2: Configure Routes

1. **Step 2 – Configure routes**
2. A default route already exists. Update it and add the rest:

**Existing Route (update this one):**

* Method: `ANY`
* Resource path: `/{proxy+}`
* Integration target: `twin-api`

**Add the following additional routes:**
Route 1:

* Method: `GET`
* Resource path: `/`
* Integration target: `twin-api`

Route 2:

* Method: `GET`
* Resource path: `/health`
* Integration target: `twin-api`

Route 3:

* Method: `POST`
* Resource path: `/chat`
* Integration target: `twin-api`

Route 4 (CORS preflight):

* Method: `OPTIONS`
* Resource path: `/{proxy+}`
* Integration target: `twin-api`

<img src="img/aws_lambda/route_config.png" width="100%">

3. Click **Next**

## Step 3: Configure Stages

1. **Step 3 – Configure stages:**

   * Stage name: `$default`
   * Auto-deploy: enabled
2. Click **Next**

## Step 4: Review and Create

1. **Step 4 – Review and create:**

   * Review your Lambda integration and all routes
2. Click **Create**

## Step 5: Configure CORS

1. In the left menu, click **CORS**
2. Click **Configure**
3. Enter the following:

* Access-Control-Allow-Origin: type `*` → **click Add**
* Access-Control-Allow-Headers: type `*` → **click Add**
* Access-Control-Allow-Methods: type `*` → **click Add**
* Access-Control-Max-Age: `300`

<img src="img/aws_lambda/cors_config.png" width="100%">

4. Click **Save**

**Important:** For every CORS field, you must **type**, then **click Add**, or your values will not be saved.

## Step 6: Test Your API

1. Go to **API details** or **Stages → $default**

<img src="img/aws_lambda/default_endpoint.png" width="100%">

2. Copy your **Invoke URL**
3. Test your health check endpoint:

Visit:

```
https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/health
```

You should see:

```
{"status": "healthy", "use_s3": true}
```

**Note:**
If you see **Missing Authentication Token**, make sure you are calling the full path:

```
/health
```