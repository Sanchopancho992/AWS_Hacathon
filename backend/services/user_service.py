import os
import logging
import uuid
from typing import Dict, Optional, List, Any
from datetime import datetime, timedelta
import json
from collections import defaultdict

logger = logging.getLogger(__name__)

class UserService:
    """
    Simple in-memory user session tracking service.
    In production, this would be replaced with a database solution.
    """
    
    def __init__(self):
        # In-memory storage (would be database in production)
        self.user_sessions: Dict[str, Dict] = {}
        self.conversation_history: Dict[str, List] = defaultdict(list)
        self.user_preferences: Dict[str, Dict] = {}
        self.session_timeout = timedelta(hours=24)  # 24 hour session timeout
        
    async def initialize(self):
        """Initialize user service"""
        try:
            logger.info("User service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize user service: {e}")
            raise
    
    def create_session(self, user_context: Optional[Dict] = None) -> str:
        """Create a new user session and return session ID"""
        session_id = str(uuid.uuid4())
        
        self.user_sessions[session_id] = {
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "user_context": user_context or {},
            "interaction_count": 0
        }
        
        logger.info(f"Created new session: {session_id}")
        return session_id
    
    def get_or_create_session(self, session_id: Optional[str] = None, user_context: Optional[Dict] = None) -> str:
        """Get existing session or create new one"""
        if session_id and self.is_session_valid(session_id):
            # Update last activity
            self.user_sessions[session_id]["last_activity"] = datetime.now()
            self.user_sessions[session_id]["interaction_count"] += 1
            return session_id
        else:
            # Create new session
            return self.create_session(user_context)
    
    def is_session_valid(self, session_id: str) -> bool:
        """Check if session exists and hasn't expired"""
        if session_id not in self.user_sessions:
            return False
        
        session = self.user_sessions[session_id]
        time_since_activity = datetime.now() - session["last_activity"]
        
        return time_since_activity < self.session_timeout
    
    def get_user_context(self, session_id: str) -> Optional[Dict]:
        """Get user context for a session"""
        if not self.is_session_valid(session_id):
            return None
        
        return self.user_sessions[session_id].get("user_context", {})
    
    def update_user_context(self, session_id: str, user_context: Dict) -> bool:
        """Update user context for a session"""
        if not self.is_session_valid(session_id):
            return False
        
        self.user_sessions[session_id]["user_context"].update(user_context)
        self.user_sessions[session_id]["last_activity"] = datetime.now()
        return True
    
    def add_conversation_message(self, session_id: str, role: str, content: str) -> bool:
        """Add a message to conversation history"""
        if not self.is_session_valid(session_id):
            return False
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.conversation_history[session_id].append(message)
        
        # Keep only last 50 messages to prevent memory issues
        if len(self.conversation_history[session_id]) > 50:
            self.conversation_history[session_id] = self.conversation_history[session_id][-50:]
        
        return True
    
    def get_conversation_history(self, session_id: str, limit: int = 20) -> List[Dict]:
        """Get conversation history for a session"""
        if not self.is_session_valid(session_id):
            return []
        
        history = self.conversation_history.get(session_id, [])
        return history[-limit:] if limit else history
    
    def save_user_preferences(self, session_id: str, preferences: Dict) -> bool:
        """Save user preferences"""
        if not self.is_session_valid(session_id):
            return False
        
        self.user_preferences[session_id] = preferences
        self.user_sessions[session_id]["last_activity"] = datetime.now()
        return True
    
    def get_user_preferences(self, session_id: str) -> Dict:
        """Get user preferences"""
        if not self.is_session_valid(session_id):
            return {}
        
        return self.user_preferences.get(session_id, {})
    
    def get_session_stats(self, session_id: str) -> Optional[Dict]:
        """Get session statistics"""
        if not self.is_session_valid(session_id):
            return None
        
        session = self.user_sessions[session_id]
        conversation_count = len(self.conversation_history.get(session_id, []))
        
        return {
            "session_id": session_id,
            "created_at": session["created_at"].isoformat(),
            "last_activity": session["last_activity"].isoformat(),
            "interaction_count": session["interaction_count"],
            "conversation_messages": conversation_count,
            "has_preferences": session_id in self.user_preferences
        }
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions (should be called periodically)"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.user_sessions.items():
            time_since_activity = current_time - session["last_activity"]
            if time_since_activity > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.user_sessions[session_id]
            if session_id in self.conversation_history:
                del self.conversation_history[session_id]
            if session_id in self.user_preferences:
                del self.user_preferences[session_id]
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        
        return len(expired_sessions)
    
    def get_all_sessions_stats(self) -> Dict:
        """Get statistics for all sessions"""
        total_sessions = len(self.user_sessions)
        active_sessions = sum(1 for s in self.user_sessions.values() 
                            if datetime.now() - s["last_activity"] < timedelta(hours=1))
        
        return {
            "total_sessions": total_sessions,
            "active_sessions": active_sessions,
            "total_conversations": len(self.conversation_history),
            "total_user_preferences": len(self.user_preferences)
        }
