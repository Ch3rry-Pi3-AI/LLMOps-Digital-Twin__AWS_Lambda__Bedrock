"""
AI Digital Twin Backend API with Configurable Memory Storage

This module defines the FastAPI backend for the llmops-digital-twin project.
It provides endpoints for:

1. Health checks
2. Basic root response (with memory/storage status)
3. Chat interactions with an AI model (with conversation memory)
4. Retrieving full conversation history for a given session

Key features:
- CORS configuration for frontend–backend communication
- Integration with the OpenAI Chat Completions API
- Pluggable memory storage:
    * Local JSON files under MEMORY_DIR
    * Optional S3-based storage, controlled by environment variables
- Rich system prompt construction using `context.prompt()`, which pulls in
  structured facts, summary, style, and LinkedIn/CV content.

Each conversation is keyed by a session_id, enabling the Digital Twin to recall
past exchanges and maintain coherent, context-aware dialogue.
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
from typing import Optional, List, Dict, Any
import json
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from context import prompt


# ============================================================
# Environment Variables
# ============================================================

# Load environment variables from .env (e.g. OPENAI_API_KEY, CORS_ORIGINS, USE_S3)
load_dotenv(override=True)


# ============================================================
# FastAPI Application
# ============================================================

# Create FastAPI instance
app = FastAPI()


# ============================================================
# CORS Configuration
# ============================================================

# Read allowed origins from environment (defaults to local Next.js dev)
origins: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Add CORS middleware to allow cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ============================================================
# OpenAI Client Initialisation
# ============================================================

# Initialise OpenAI client using explicit API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================================================
# Memory Storage Configuration
# ============================================================

# Toggle between local file-based storage and S3-based storage
USE_S3: bool = os.getenv("USE_S3", "false").lower() == "true"

# S3 bucket name used when USE_S3 is enabled
S3_BUCKET: str = os.getenv("S3_BUCKET", "")

# Local directory used when storing memory on disk
MEMORY_DIR: str = os.getenv("MEMORY_DIR", "../memory")

# Initialise S3 client if required
if USE_S3:
    s3_client = boto3.client("s3")


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


class Message(BaseModel):
    """
    Model representing a single message in the conversation history.

    Attributes
    ----------
    role : str
        The role of the speaker ('user' or 'assistant').
    content : str
        The textual content of the message.
    timestamp : str
        ISO 8601 timestamp indicating when the message was created.
    """
    role: str
    content: str
    timestamp: str


# ============================================================
# Memory Management Helpers
# ============================================================

def get_memory_path(session_id: str) -> str:
    """
    Construct the storage key / file name for a given session.

    Parameters
    ----------
    session_id : str
        Unique identifier for the conversation session.

    Returns
    -------
    str
        The relative key or path for storing this session's memory.
    """
    return f"{session_id}.json"


def load_conversation(session_id: str) -> List[Dict[str, Any]]:
    """
    Load conversation history for a given session from storage.

    If S3 is enabled, the conversation is read from the configured S3 bucket.
    Otherwise, it is loaded from the local filesystem under MEMORY_DIR.

    Parameters
    ----------
    session_id : str
        Unique identifier for the conversation session.

    Returns
    -------
    List[Dict[str, Any]]
        A list of message dictionaries representing the conversation history.
        Each message dictionary contains 'role', 'content', and 'timestamp'.
    """
    if USE_S3:
        try:
            # Retrieve the object from S3
            response = s3_client.get_object(
                Bucket=S3_BUCKET,
                Key=get_memory_path(session_id),
            )
            return json.loads(response["Body"].read().decode("utf-8"))
        except ClientError as e:
            # If the object is not found, return an empty history
            if e.response["Error"]["Code"] == "NoSuchKey":
                return []
            # Propagate other S3-related errors
            raise
    else:
        # Local file storage
        file_path = os.path.join(MEMORY_DIR, get_memory_path(session_id))
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


def save_conversation(session_id: str, messages: List[Dict[str, Any]]) -> None:
    """
    Persist the conversation history for a given session to storage.

    If S3 is enabled, the conversation is written to the configured S3 bucket.
    Otherwise, it is saved as a JSON file in the local MEMORY_DIR.

    Parameters
    ----------
    session_id : str
        Unique identifier for the conversation session.
    messages : List[Dict[str, Any]]
        The full list of messages to write to storage.
    """
    if USE_S3:
        # Store JSON-serialised conversation in S3
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=get_memory_path(session_id),
            Body=json.dumps(messages, indent=2),
            ContentType="application/json",
        )
    else:
        # Local file storage
        os.makedirs(MEMORY_DIR, exist_ok=True)
        file_path = os.path.join(MEMORY_DIR, get_memory_path(session_id))
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2)


# ============================================================
# API Routes
# ============================================================

@app.get("/")
async def root() -> Dict[str, Any]:
    """
    Root endpoint used to verify the API is running and memory configuration.

    Returns
    -------
    dict
        A dictionary containing a welcome message and storage configuration.
    """
    return {
        "message": "AI Digital Twin API",
        "memory_enabled": True,
        "storage": "S3" if USE_S3 else "local",
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for monitoring and readiness probes.

    Returns
    -------
    dict
        A simple dictionary indicating service health and S3 usage.
    """
    return {"status": "healthy", "use_s3": USE_S3}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Handle chat interactions with the AI model, including session-based memory.

    This endpoint:
    - Generates or reuses a session_id
    - Loads previous conversation history for that session
    - Builds a messages list including:
        * a system message constructed from `context.prompt()`
        * prior user and assistant messages (last 10 for context)
        * the current user message
    - Sends the combined context to the OpenAI Chat Completions API
    - Updates and saves the conversation history

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
        # Generate a new session ID if not provided by the client
        session_id: str = request.session_id or str(uuid.uuid4())

        # Load existing conversation history for this session
        conversation: List[Dict[str, Any]] = load_conversation(session_id)

        # Build the message list starting with the system prompt
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": prompt()}
        ]

        # Append the last 10 messages from the conversation history for context
        for msg in conversation[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})

        # Add the current user message
        messages.append({"role": "user", "content": request.message})

        # Call the OpenAI Chat Completions API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        # Extract the assistant's reply
        assistant_response: str = response.choices[0].message.content

        # Append the new user message to the conversation history
        conversation.append(
            {
                "role": "user",
                "content": request.message,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Append the assistant's reply to the conversation history
        conversation.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Persist the updated conversation history
        save_conversation(session_id, conversation)

        # Return the structured response
        return ChatResponse(response=assistant_response, session_id=session_id)

    except Exception as e:
        # Log the error and surface a generic HTTP 500 to the client
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversation/{session_id}")
async def get_conversation(session_id: str) -> Dict[str, Any]:
    """
    Retrieve the full conversation history for a given session.

    Parameters
    ----------
    session_id : str
        Unique identifier for the conversation session.

    Returns
    -------
    dict
        A dictionary containing the session_id and its associated messages.

    Raises
    ------
    HTTPException
        If an error occurs while loading the conversation history.
    """
    try:
        conversation: List[Dict[str, Any]] = load_conversation(session_id)
        return {"session_id": session_id, "messages": conversation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Local Development Server (Uvicorn)
# ============================================================

if __name__ == "__main__":
    # Run Uvicorn development server locally
    import uvicorn

    # Start server on port 8000, accessible from all interfaces
    uvicorn.run(app, host="0.0.0.0", port=8000)
