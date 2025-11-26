# 📁 **`/backend`**

The `backend` directory contains the core API components for the **llmops-digital-twin** project. This folder handles configuration, personality loading, and the FastAPI application that communicates with the OpenAI API.

## Files Inside This Folder

### **1. `requirements.txt`**

Lists all Python dependencies needed for the backend. These include FastAPI, Uvicorn, the OpenAI SDK, and utilities for loading environment variables and handling incoming requests. Installing from this file ensures the backend runs consistently across machines.

### **2. `.env`**

Holds environment-specific configuration such as the OpenAI API key and allowed CORS origins. This file is kept out of version control for security reasons and is automatically loaded when the backend starts.

### **3. `me.txt`**

Contains the Digital Twin’s personality description. Its contents are injected into each chat request as the system message, shaping how the AI responds on your behalf. This file provides grounding for tone, identity, and professional background.

### **4. `server.py` (without memory)**

The main FastAPI application. It sets up CORS policies, loads the personality from `me.txt`, defines request and response models, and exposes the `/`, `/health`, and `/chat` endpoints. The current version does not include memory; each request is processed independently. Future branches will extend this file to incorporate conversational memory and state handling.

This backend folder forms the foundation of the Digital Twin’s intelligence layer, enabling the frontend to send messages and receive personality-aligned responses.