"""
AWS Lambda Handler for the Digital Twin Backend

This module adapts the FastAPI application for serverless deployment using AWS
Lambda and API Gateway. It uses the Mangum adapter, which allows ASGI
applications (such as FastAPI) to run seamlessly in Lambda environments.

When deployed, API Gateway forwards incoming HTTP requests to this Lambda
function, which passes them into the FastAPI `app` object. Responses generated
by FastAPI are then returned through API Gateway back to the client.

This file should be deployed alongside `server.py` in the backend directory.
"""

# ============================================================
# Imports
# ============================================================

from mangum import Mangum
from server import app


# ============================================================
# Lambda Handler Creation
# ============================================================

# Wrap the FastAPI app with Mangum so it can run inside AWS Lambda
handler = Mangum(app)
