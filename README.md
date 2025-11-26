# 🧠 **Backend API — Branch Overview**

This branch introduces the backend layer for the **llmops-digital-twin** project. The focus is on creating the initial FastAPI service, defining configuration files, setting up the Digital Twin personality file, and preparing a clean API endpoint that the frontend will communicate with. Memory is not implemented at this stage and will be added in a later branch.

## Part 1: Create the Backend Files

### Step 1: Create the Requirements File

Create `backend/requirements.txt`:

```
fastapi
uvicorn
openai
python-dotenv
python-multipart
```

These dependencies allow the backend to run a FastAPI server, load environment variables, interact with OpenAI models, and handle incoming requests from the frontend.

### Step 2: Add Environment Configuration

Create `backend/.env`:

```
OPENAI_API_KEY=your_openai_api_key_here
CORS_ORIGINS=http://localhost:3000
```

Replace `your_openai_api_key_here` with your real API key.

This file stores sensitive configuration values and should not be committed to Git. To protect it, ensure the project root contains a `.gitignore` file with:

```
.env
```

This keeps your secrets safe while working across branches.

### Step 3: Add the Digital Twin Personality File

Create `backend/me.txt` with a description of who your Digital Twin represents.

This file acts as the system prompt. Its contents shape how the model responds on your behalf. Every chat request loads this personality text and uses it to generate replies that reflect your tone, background, and expertise.

Example structure:

```
You are a chatbot acting as a "Digital Twin", representing Roger J. Campbell...

(your personality content here)
```

The final version is customised to your educational background, AI/ML consulting work, interests, and tone.

### Step 4: Build the FastAPI Server

Create `backend/server.py` containing the backend API logic.

This file:

* Loads environment variables
* Configures CORS for safe communication with the frontend
* Loads the Digital Twin personality from `me.txt`
* Defines request and response models
* Provides `/`, `/health`, and `/chat` endpoints
* Sends user messages to OpenAI and returns the model’s response

The `/chat` endpoint currently **does not include memory**. Each request is processed independently. A session ID is generated so that memory can be added seamlessly in a later branch.

## Part 2: Backend Structure After This Branch

Your backend now looks like:

```
llmops-digital-twin/
├── backend/
│   ├── .env
│   ├── me.txt
│   ├── requirements.txt
│   └── server.py
```

This backend is now prepared to receive messages from the frontend and respond as your Digital Twin. Memory, retrieval, history tracking, and advanced features will be built in upcoming branches.
