"""
AI Digital Twin Backend API with Memory

This module sets up a FastAPI application that serves as the backend for the
llmops-digital-twin project. It provides endpoints for:

1. Health checks
2. Basic root response
3. Chat interactions with an AI model (with file-based conversation memory)
4. Listing active conversation sessions

The API loads environment variables, configures CORS, integrates with the
OpenAI client, and persists per-session conversation history in JSON files
under the ../memory directory. Each session is identified by a session_id,
which allows the Digital Twin to recall previous messages within that session.
"""

# ============================================================
# Imports
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict
import json
import uuid
from datetime import datetime  # Currently unused, kept for potential future extension
from pathlib import Path


# ============================================================
# Environment Variables
# ============================================================

# Load environment variables from .env (e.g. OPENAI_API_KEY, CORS_ORIGINS)
load_dotenv(override=True)


# ============================================================
# FastAPI Application
# ============================================================

# Create FastAPI instance
app = FastAPI()


# ============================================================
# CORS Configuration
# ============================================================

# Read allowed origins from environment (defaults to local React/Next.js dev)
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Add CORS middleware to allow secure cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # Allow all HTTP methods
    allow_headers=["*"],   # Allow all HTTP headers
)


# ============================================================
# OpenAI Client Initialisation
# ============================================================

# Create OpenAI client using API key loaded via environment variables
client = OpenAI()


# ============================================================
# Memory Directory Configuration
# ============================================================

# Define the directory used to store per-session conversation history
MEMORY_DIR = Path("../memory")

# Ensure the memory directory exists
MEMORY_DIR.mkdir(exist_ok=True)


# ============================================================
# Personality Loading
# ============================================================

def load_personality() -> str:
    """
    Load the personality text file used as a system message for the AI.

    Returns
    -------
    str
        The personality prompt content from the local file.
    """
    # Open the personality file and return its contents
    with open("me.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


# Load the personality at startup
PERSONALITY = load_personality()


# ============================================================
# Memory Handling Functions
# ============================================================

def load_conversation(session_id: str) -> List[Dict]:
    """
    Load conversation history for a given session from disk.

    Parameters
    ----------
    session_id : str
        Unique identifier for the conversation session.

    Returns
    -------
    List[Dict]
        A list of message dictionaries representing the conversation history.
        Each message dictionary contains 'role' and 'content' fields.
    """
    # Construct the file path for this session
    file_path = MEMORY_DIR / f"{session_id}.json"

    # If the file exists, load and return its contents
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # No existing conversation found, return an empty list
    return []


def save_conversation(session_id: str, messages: List[Dict]) -> None:
    """
    Persist the conversation history for a given session to disk.

    Parameters
    ----------
    session_id : str
        Unique identifier for the conversation session.
    messages : List[Dict]
        The full list of messages to write to the session file.
    """
    # Construct the file path for this session
    file_path = MEMORY_DIR / f"{session_id}.json"

    # Write the messages list to disk as formatted JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)


# ============================================================
# Request and Response Models
# ============================================================

class ChatRequest(BaseModel):
    """
    Request model for chat messages sent to the API.

    Attributes
    ----------
    message : str
        The text message from the user.
    session_id : Optional[str]
        Unique identifier for the conversation session.
        Generated automatically if not provided.
    """
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """
    Response model returned by the API after processing chat input.

    Attributes
    ----------
    response : str
        The AI-generated reply.
    session_id : str
        The session identifier associated with the request.
    """
    response: str
    session_id: str


# ============================================================
# API Routes
# ============================================================

@app.get("/")
async def root():
    """
    Root endpoint used to verify the API is running.

    Returns
    -------
    dict
        A simple welcome message indicating memory support.
    """
    return {"message": "AI Digital Twin API with Memory"}


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and readiness probes.

    Returns
    -------
    dict
        A simple dictionary indicating service health.
    """
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle chat interactions with the AI model, including session-based memory.

    This endpoint:
    - Generates or reuses a session_id
    - Loads previous conversation history for that session
    - Constructs a message list including:
        * system personality
        * prior user and assistant messages
        * the current user message
    - Sends the combined context to the OpenAI API
    - Stores the updated conversation history back to disk

    Parameters
    ----------
    request : ChatRequest
        The user input containing the message and optional session ID.

    Returns
    -------
    ChatResponse
        The AI's reply and the associated session identifier.

    Raises
    ------
    HTTPException
        If an error occurs when generating the AI response.
    """
    try:
        # Generate session ID if not provided by the client
        session_id = request.session_id or str(uuid.uuid4())

        # Load existing conversation history for this session
        conversation = load_conversation(session_id)

        # Start the message list with the system personality
        messages = [{"role": "system", "content": PERSONALITY}]

        # Append prior conversation history to the messages list
        for msg in conversation:
            messages.append(msg)

        # Add the current user message as the latest entry
        messages.append({"role": "user", "content": request.message})

        # Call the OpenAI model to generate a chat completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # Extract the assistant's reply content
        assistant_response = response.choices[0].message.content

        # Update conversation history with the new user and assistant messages
        conversation.append({"role": "user", "content": request.message})
        conversation.append({"role": "assistant", "content": assistant_response})

        # Persist the updated conversation history for this session
        save_conversation(session_id, conversation)

        # Return the AI response and session ID to the client
        return ChatResponse(
            response=assistant_response,
            session_id=session_id
        )

    except Exception as e:
        # Raise FastAPI HTTP exception for any runtime error
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions")
async def list_sessions():
    """
    List all conversation sessions that have been stored in the memory directory.

    Returns
    -------
    dict
        A dictionary containing a list of sessions, where each session entry
        includes:
        - session_id : str
            The unique session identifier
        - message_count : int
            Number of messages stored in the conversation
        - last_message : Optional[str]
            The content of the final message in the conversation, if any
    """
    sessions = []

    # Iterate over all JSON files in the memory directory
    for file_path in MEMORY_DIR.glob("*.json"):
        session_id = file_path.stem

        # Load the conversation history for this session
        with open(file_path, "r", encoding="utf-8") as f:
            conversation = json.load(f)

        # Build a summary entry for this session
        sessions.append({
            "session_id": session_id,
            "message_count": len(conversation),
            "last_message": conversation[-1]["content"] if conversation else None
        })

    # Return the list of sessions
    return {"sessions": sessions}


# ============================================================
# Local Development Server (Uvicorn)
# ============================================================

if __name__ == "__main__":
    # Run Uvicorn development server locally
    import uvicorn

    # Start server on port 8000, accessible from all interfaces
    uvicorn.run(app, host="0.0.0.0", port=8000)