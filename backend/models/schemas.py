from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserContext(BaseModel):
    location: Optional[str] = None
    language_preference: str = "en"
    interests: List[str] = []
    budget_range: Optional[str] = None

class ConversationMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    session_id: Optional[str] = None
    conversation_history: List[ConversationMessage] = []
    user_context: Optional[UserContext] = None

class Source(BaseModel):
    title: str
    content: str
    url: Optional[str] = None
    relevance_score: float

class ChatResponse(BaseModel):
    message: str
    sources: List[Source] = []
    conversation_id: Optional[str] = None
    session_id: Optional[str] = None

class ItineraryRequest(BaseModel):
    duration: int  # days
    interests: List[str]
    budget: str  # "low", "medium", "high"
    accommodation: Optional[str] = None
    travel_style: str = "moderate"  # "slow", "moderate", "fast"
    group_size: int = 1
    special_requirements: Optional[List[str]] = None
    session_id: Optional[str] = None

class DayPlan(BaseModel):
    day: int
    date: Optional[str] = None
    activities: List[Dict[str, Any]]
    estimated_cost: Optional[float] = None
    transportation_info: Optional[str] = None

class ItineraryResponse(BaseModel):
    itinerary: List[DayPlan]
    total_estimated_cost: Optional[float] = None
    tips: List[str] = []
    session_id: Optional[str] = None

class TranslationRequest(BaseModel):
    text: str
    source_language: str = "auto"
    target_language: str = "en"
    context_type: Optional[str] = None  # "menu", "sign", "conversation"
    session_id: Optional[str] = None

class TranslationResponse(BaseModel):
    translated_text: str
    original_text: Optional[str] = None
    cultural_context: Optional[str] = None
    confidence: float = 0.0
    session_id: Optional[str] = None

class RecommendationRequest(BaseModel):
    user_preferences: Dict[str, Any]
    current_location: Optional[str] = None
    time_context: Optional[str] = None  # "morning", "afternoon", "evening"
    limit: int = 5
    session_id: Optional[str] = None

class Recommendation(BaseModel):
    name: str
    description: str
    category: str
    location: str
    rating: Optional[float] = None
    estimated_time: Optional[str] = None
    cost_range: Optional[str] = None
    reasons: List[str] = []

class RecommendationResponse(BaseModel):
    recommendations: List[Recommendation]
    session_id: Optional[str] = None

# New schemas for session management
class SessionRequest(BaseModel):
    user_context: Optional[UserContext] = None

class SessionResponse(BaseModel):
    session_id: str
    created_at: str
    message: str = "Session created successfully"

class SessionStatsResponse(BaseModel):
    session_id: str
    created_at: str
    last_activity: str
    interaction_count: int
    conversation_messages: int
    has_preferences: bool
