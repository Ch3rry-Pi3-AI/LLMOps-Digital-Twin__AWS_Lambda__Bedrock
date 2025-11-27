# 🧠 **Adding Memory to Your Digital Twin — Branch Overview**

This branch upgrades the **llmops-digital-twin** backend to support **persistent conversational memory**. Your Digital Twin can now recall previous messages within a session, enabling natural, context-aware dialogue. Memory is stored as JSON files in the `/memory` directory, allowing each session to maintain its own conversation history.

## part 1: update the backend with memory support

### Step 1: Replace `server.py` with the memory-enabled version

In this branch, the backend is enhanced to include:

* a per-session memory system
* JSON storage under `../memory/`
* automatic session creation
* loading previous messages before each new request
* storing updated conversations after each assistant reply
* a `/sessions` endpoint for inspecting all active sessions

Replace your existing `backend/server.py` with the new memory-enabled version provided for this branch.

This update allows your Digital Twin to remember user-provided details (such as their name, preferences, or project details) across multiple messages within the same session.

## part 2: restart the backend server

After replacing `server.py`, restart the backend:

```bash
cd backend
uv run uvicorn server:app --reload
```

You should see the usual FastAPI startup logs indicating that the server is running on:

```
http://127.0.0.1:8000
```

The backend is now ready to support full memory-based conversations.

## part 3: test memory persistence in your Digital Twin

### Step 1: Open the app

Visit:

```
http://localhost:3000
```

### Step 2: Have a memory test conversation

Try the following messages:

1. **you:** “Hi! My name is Fred and I love Python.”
2. **twin:** responds with greeting and acknowledges your preferences
3. **you:** “What’s my name and what do I love?”
4. **twin:** correctly remembers:

   * your name is Fred
   * you love Python

Your interface should look similar to:

<img src="img/testing/chat_remember.png" width="100%" />

### Step 3: Inspect the memory files

Open a terminal and check the memory directory:

```bash
ls ../memory/
```

You will see files such as:

```
c12a55d8-8f23-41af-a81f-fbb3b6f6ed3e.json
```

Each file represents one session and contains the full conversation history:

```json
[
  {
    "role": "user",
    "content": "Hi! My name is Fred and I love Python"
  },
  {
    "role": "assistant",
    "content": "Hi, Fred! It's great to meet you..."
  },
  {
    "role": "user",
    "content": "What's my name and what do I love?"
  },
  {
    "role": "assistant",
    "content": "You mentioned that your name is Fred and you love Python..."
  }
]
```

This JSON file-based memory system now enables your Digital Twin to maintain session context and support natural multi-turn conversations.

Your backend now fully supports memory, completing a major milestone in developing your Digital Twin.
