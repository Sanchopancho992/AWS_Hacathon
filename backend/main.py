"""
Hong Kong Tourism AI - Main API Server

This is the main FastAPI server that powers the Hong Kong Tourism AI assistant.
It provides endpoints for:
- Chat with AI assistant (RAG-powered Q&A)
- Smart itinerary planning  
- Real-time translation (text and images)
- Personalized recommendations
- User session management

The server uses Google Gemini AI and Pinecone vector database to provide
intelligent, context-aware responses about Hong Kong tourism.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv
from typing import Optional, List
import logging
from datetime import datetime
from mangum import Mangum

# Import our data models for API requests and responses
from models.schemas import (
    ChatRequest, ChatResponse, 
    ItineraryRequest, ItineraryResponse,
    TranslationRequest, TranslationResponse,
    RecommendationRequest, RecommendationResponse,
    SessionRequest, SessionResponse, SessionStatsResponse
)

# Import our AI-powered services
from services.rag_service import RAGService  # AI chat with Hong Kong knowledge
from services.translation_service import TranslationService  # Text and image translation
from services.itinerary_service import ItineraryService  # Smart trip planning
from services.recommendation_service import RecommendationService  # Personalized suggestions
from services.user_service import UserService  # Session and user management

# Load environment variables from .env file (API keys, etc.)
load_dotenv()

# Set up logging so we can see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize all our AI services
rag_service = RAGService()
translation_service = TranslationService()
itinerary_service = ItineraryService()
recommendation_service = RecommendationService()
user_service = UserService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown.
    This ensures all AI services are properly initialized when the server starts.
    """
    # Startup: Initialize all services
    try:
        await user_service.initialize()
        logger.info("✅ User service ready - can track sessions and preferences")
        
        await rag_service.initialize()
        logger.info("✅ RAG service ready - AI chat with Hong Kong knowledge loaded")
        
        await translation_service.initialize()
        logger.info("✅ Translation service ready - can translate text and images")
        
        await itinerary_service.initialize()
        logger.info("Itinerary service initialized successfully")
        
        await recommendation_service.initialize()
        logger.info("Recommendation service initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
    
    yield
    
    # Shutdown (cleanup if needed)
    logger.info("Shutting down...")

app = FastAPI(
    title="HK Tourism AI API",
    description="Smart Tourism AI for Hong Kong with RAG-powered Q&A, itinerary planning, and translation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "HK Tourism AI API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "services": {
            "rag": rag_service is not None,
            "user": user_service is not None,
            "recommendation": recommendation_service is not None,
            "itinerary": itinerary_service is not None,
            "translation": translation_service is not None
        }
    }

@app.post("/api/session", response_model=SessionResponse)
async def create_session(request: SessionRequest = None):
    """Create a new user session"""
    try:
        user_context = request.user_context.dict() if request and request.user_context else None
        session_id = user_service.create_session(user_context)
        session = user_service.get_session_stats(session_id)
        
        return SessionResponse(
            session_id=session_id,
            created_at=session["created_at"],
            message="Session created successfully"
        )
    except Exception as e:
        logger.error(f"Session creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/session/{session_id}/stats", response_model=SessionStatsResponse)
async def get_session_stats(session_id: str):
    """Get session statistics"""
    try:
        stats = user_service.get_session_stats(session_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Session not found or expired")
        
        return SessionStatsResponse(**stats)
    except Exception as e:
        logger.error(f"Session stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/session/cleanup")
async def cleanup_expired_sessions():
    """Clean up expired sessions (admin endpoint)"""
    try:
        cleaned_count = user_service.cleanup_expired_sessions()
        return {"message": f"Cleaned up {cleaned_count} expired sessions"}
    except Exception as e:
        logger.error(f"Session cleanup error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """RAG-powered chat endpoint for Hong Kong tourism questions"""
    try:
        # Get or create session
        session_id = user_service.get_or_create_session(
            request.session_id, 
            request.user_context.dict() if request.user_context else None
        )
        
        # Add user message to conversation history
        user_service.add_conversation_message(session_id, "user", request.message)
        
        # Get conversation history from session if not provided
        conversation_history = request.conversation_history
        if not conversation_history:
            history = user_service.get_conversation_history(session_id, limit=10)
            conversation_history = [
                {"role": msg["role"], "content": msg["content"], "timestamp": msg["timestamp"]}
                for msg in history
            ]
        
        response = await rag_service.chat(
            query=request.message,
            conversation_history=conversation_history,
            user_context=request.user_context.dict() if request.user_context else user_service.get_user_context(session_id)
        )
        
        # Add assistant response to conversation history
        user_service.add_conversation_message(session_id, "assistant", response["answer"])
        
        return ChatResponse(
            message=response["answer"],
            sources=response.get("sources", []),
            conversation_id=request.conversation_id,
            session_id=session_id
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/itinerary", response_model=ItineraryResponse)
async def generate_itinerary(request: ItineraryRequest):
    """Generate personalized Hong Kong itinerary"""
    try:
        # Get or create session
        session_id = user_service.get_or_create_session(request.session_id)
        
        # Save user preferences for future use
        preferences = {
            "interests": request.interests,
            "budget": request.budget,
            "travel_style": request.travel_style,
            "group_size": request.group_size
        }
        user_service.save_user_preferences(session_id, preferences)
        
        itinerary = await itinerary_service.generate_itinerary(
            duration=request.duration,
            interests=request.interests,
            budget=request.budget,
            accommodation=request.accommodation,
            travel_style=request.travel_style,
            group_size=request.group_size,
            special_requirements=request.special_requirements
        )
        return ItineraryResponse(itinerary=itinerary, session_id=session_id)
    except Exception as e:
        logger.error(f"Itinerary generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """Translate text with cultural context"""
    try:
        # Get or create session
        session_id = user_service.get_or_create_session(request.session_id)
        
        result = await translation_service.translate_with_context(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language,
            context_type=request.context_type
        )
        return TranslationResponse(
            translated_text=result["translation"],
            cultural_context=result.get("context", ""),
            confidence=result.get("confidence", 0.0),
            session_id=session_id
        )
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/translate-image", response_model=TranslationResponse)
async def translate_image(file: UploadFile = File(...)):
    """Extract text from image and translate"""
    try:
        # Read image content
        content = await file.read()
        
        result = await translation_service.translate_image(
            image_content=content,
            target_language="en"
        )
        
        return TranslationResponse(
            translated_text=result["translation"],
            original_text=result.get("original_text", ""),
            cultural_context=result.get("context", ""),
            confidence=result.get("confidence", 0.0)
        )
    except Exception as e:
        logger.error(f"Image translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recommendations", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get personalized recommendations"""
    try:
        # Get or create session
        session_id = user_service.get_or_create_session(request.session_id)
        
        # Merge with saved preferences if available
        saved_preferences = user_service.get_user_preferences(session_id)
        merged_preferences = {**saved_preferences, **request.user_preferences}
        
        recommendations = await recommendation_service.get_recommendations(
            user_preferences=merged_preferences,
            current_location=request.current_location,
            time_context=request.time_context,
            limit=request.limit,
            session_id=session_id
        )
        return RecommendationResponse(recommendations=recommendations, session_id=session_id)
    except Exception as e:
        logger.error(f"Recommendation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="127.0.0.1", 
        port=8000, 
        reload=True
    )

# Vercel serverless handler
handler = Mangum(app)
