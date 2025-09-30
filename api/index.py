# Vercel serverless function handler
from backend.main import app

# Export the FastAPI app for Vercel
def handler(request, context):
    return app(request, context)
