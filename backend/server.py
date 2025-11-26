"""
AI Digital Twin Backend API

This module sets up a FastAPI application that serves as the backend for the
LLMOps Digital Twin project. It provides endpoints for:

1. Health checks
2. Basic root response
3. Chat interactions with an AI model

The API loads environment variables, configures CORS, and integrates with the
OpenAI client. Each chat request is processed independently without memory,
although a session ID is generated to maintain future extensibility.
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
from typing import Optional
import uuid


# ============================================================
# Environment Variables
# ============================================================

# Load environment variables from .env
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
        A simple welcome message.
    """
    return {"message": "AI Digital Twin API"}


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
    Handle chat interactions with the AI model.

    This endpoint constructs a system prompt using the stored personality,
    forwards the user message to the OpenAI API, and returns the generated
    response. No conversational memory is retained between requests.

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

        # Construct message list with system personality and user input
        messages = [
            {"role": "system", "content": PERSONALITY},
            {"role": "user", "content": request.message},
        ]

        # Call the OpenAI model to generate a chat completion
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # Return structured response
        return ChatResponse(
            response=response.choices[0].message.content,
            session_id=session_id
        )

    except Exception as e:
        # Raise FastAPI HTTP exception for any runtime error
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Local Development Server (Uvicorn)
# ============================================================

if __name__ == "__main__":
    # Run Uvicorn development server locally
    import uvicorn

    # Start server on port 8000, accessible from all interfaces
    uvicorn.run(app, host="0.0.0.0", port=8000)
