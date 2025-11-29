# 📁 **`/backend`**

The `backend` directory contains all API logic and supporting resources for the **llmops-digital-twin** project.
This backend powers the Digital Twin’s intelligence, memory, personality shaping, and optional cloud-ready deployment.

It includes:

* The FastAPI application
* Local or S3-based conversation memory
* Personality and style resources
* Context-generation logic
* AWS Bedrock model integration
* AWS Lambda compatibility
* Personal data files (stored in `/backend/data`)

## Files Inside This Folder

### **1. `requirements.txt`**

Defines all Python dependencies required for the backend, including:

* FastAPI  
* Uvicorn  
* boto3 (for Bedrock + optional S3 memory storage)  
* python-dotenv  
* mangum (for AWS Lambda support)

Installing from this file ensures consistent backend behaviour across all environments.

### **2. `.env`**

Stores environment-specific configuration such as:

* `DEFAULT_AWS_REGION`  
* `BEDROCK_MODEL_ID`  
* `CORS_ORIGINS`  
* `USE_S3=true/false`  
* `S3_BUCKET`  
* `MEMORY_DIR`

This file should never be committed. It is automatically loaded when the backend starts.

### **3. `server.py` (FastAPI + Bedrock + Memory Engine)**

The main FastAPI application.

It now supports:

* Integration with **AWS Bedrock Runtime**  
* Full conversation memory (user + assistant messages)  
* Local filesystem or S3-based memory storage  
* Clean, policy-friendly CORS configuration  
* Strong request/response Pydantic models  
* Robust Bedrock error handling  
* System-prompt injection via `context.py`  
* Session retrieval endpoint for restoring prior conversations  

This file forms the **core intelligence, memory, and model-orchestration engine** of the Digital Twin.

### **4. `lambda_handler.py`**

A lightweight adapter using **Mangum**, enabling the FastAPI backend to run seamlessly on:

* AWS Lambda  
* API Gateway  

This provides a fully serverless deployment option for the Digital Twin.

### **5. `context.py`**

Builds the full system prompt that governs how the Digital Twin behaves.

It:

* Loads data from `facts.json`, `summary.txt`, `style.txt`, and `linkedin.pdf`  
* Constructs a structured and unified behavioural prompt  
* Encodes tone, identity, guardrails, and conversational style  
* Ensures the Digital Twin reflects your professional identity accurately  

This is the backbone of the Digital Twin’s personality and consistency.

### **6. `resources.py`**

Handles loading and preprocessing all personal data, including:

* Extracted text from `LinkedIn.pdf`  
* Professional summaries  
* Style and tone instructions  
* Structured JSON-based facts  

It centralises all personal information used to generate the Digital Twin’s internal context.

### **7. `data/` Folder**

Contains the personal and contextual information used to construct your Digital Twin’s knowledge base.

Included files:

* `facts.json` → structured data: name, skills, education, roles  
* `summary.txt` → a professional overview  
* `style.txt` → your communication style  
* `LinkedIn.pdf` → CV-derived content used to refine the system prompt  

These files collectively ensure the AI mirrors your background and communication style.

### **8. `deploy.py` (Lambda Deployment Packager)**

Automates building the **AWS Lambda deployment package** for the backend.

It:

* Cleans previous build artefacts (`lambda-package/`, `lambda-deployment.zip`)  
* Uses the **AWS Lambda Python 3.12 Docker image** to install dependencies into `lambda-package/`  
* Copies core backend files (`server.py`, `lambda_handler.py`, `context.py`, `resources.py`)  
* Includes the `data/` folder so the Digital Twin’s persona resources are available in Lambda  
* Creates a production-ready `lambda-deployment.zip` that can be:
  * Uploaded directly to Lambda, or  
  * Used as the source for `aws lambda update-function-code`  

This script ensures your deployment artefact is binary-compatible with the Lambda runtime and keeps the packaging process repeatable and reliable.
