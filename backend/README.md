Here is a clean, fully updated **`/backend` folder README**, now reflecting:

* The new **memory system**
* The new **S3 optional integration**
* The new **data folder**
* The new **context.py**
* The new **resources.py**
* The new **lambda_handler.py**
* The updated **server.py**

All formatting matches your preferred style — clean, simple, consistent, and **no horizontal rules**.

---

# 📁 **`/backend`**

The `backend` directory contains all API logic and supporting resources for the **llmops-digital-twin** project.
This backend powers the Digital Twin’s intelligence, personality shaping, memory, and optional cloud-ready deployment.

It includes:

* The FastAPI application
* Local or S3-based conversation memory
* Personality and style resources
* Context-generation logic
* AWS Lambda compatibility
* Personal data files (stored in `/backend/data`)

## Files Inside This Folder

### **1. `requirements.txt`**

Defines all Python dependencies required for the backend, including:

* FastAPI
* Uvicorn
* OpenAI SDK
* boto3 (for optional S3 memory storage)
* dotenv
* mangum (for AWS Lambda support)

Installing from this file ensures consistent backend behaviour across machines or environments.

### **2. `.env`**

Stores environment-specific configuration such as:

* `OPENAI_API_KEY`
* `CORS_ORIGINS`
* `USE_S3=true/false`
* `S3_BUCKET`
* `MEMORY_DIR`

This file should never be committed to Git. It is loaded automatically when the backend starts.

### **3. `server.py` (with memory + S3 support)**

The main FastAPI application.

It now supports:

* Full conversation memory
* Local filesystem or S3-based storage
* Request/response models
* Context injection via the new `context.py`
* Session retrieval endpoint
* Clean CORS configuration
* Production-ready structure

This file forms the core intelligence + memory engine of the Digital Twin.

### **4. `lambda_handler.py`**

A lightweight adapter using **Mangum**, allowing the FastAPI app to run seamlessly inside:

* AWS Lambda
* API Gateway

This enables fully serverless backend hosting.

### **5. `context.py`**

Generates the full system prompt that informs how the Digital Twin behaves.

It:

* Loads data from `facts.json`, `summary.txt`, `style.txt`, and `linkedin.pdf`
* Constructs a detailed, structured prompt
* Defines behavioural rules, tone, and guardrails
* Represents your professional identity accurately

This ensures the AI behaves consistently and naturally as your Digital Twin.

### **6. `resources.py`**

Responsible for loading all personal data, including:

* Extracted text from `LinkedIn.pdf`
* Summary notes
* Communication style notes
* Structured facts from `facts.json`

It centralises all personal information the Digital Twin uses to represent you.

### **7. `data/` Folder**

Contains personal data used to construct your Digital Twin’s knowledge base.

Included files:

* `facts.json` → structured profile: name, roles, skills, education
* `summary.txt` → high-level professional summary
* `style.txt` → communication-style instructions
* `LinkedIn.pdf` → full CV-derived text used to enrich the model context

These files allow your Digital Twin to accurately reflect your background, skills, tone, and professional identity.

### **8. `me.txt`**

This older file remains for compatibility, though the new system uses the richer dataset inside `/data`.
`server.py` still supports it for basic system prompts, but advanced behaviour comes from `context.py`.
