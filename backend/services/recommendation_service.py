import os
import logging
from typing import List, Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import hashlib
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.text_utils import humanize_response, clean_markdown_formatting

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        self.llm = None
        # Shorter cache for recommendations to feel more dynamic
        self._cache = {}
        self._cache_timeout = 1800  # 30 minutes cache timeout for fresher recommendations
        
    async def initialize(self):
        """Initialize recommendation service"""
        try:
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("GOOGLE_API_KEY not found")
            
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                google_api_key=google_api_key,
                temperature=0.3
            )
            
            logger.info("Recommendation service initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize recommendation service: {e}")
            raise
    
    async def get_recommendations(
        self,
        user_preferences: Dict[str, Any],
        current_location: Optional[str] = None,
        time_context: Optional[str] = None,
        limit: int = 5,
        session_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get personalized recommendations based on user preferences"""
        try:
            # Create cache key from parameters (include session for user-specific caching)
            cache_key = self._create_cache_key(
                user_preferences, current_location, time_context, limit, session_id
            )
            
            # Check cache first (shorter cache time for more dynamic recommendations)
            cached_result = self._get_from_cache(cache_key)
            if cached_result:
                logger.info("Returning cached recommendations")
                return cached_result
            
            # Build recommendation prompt
            prompt = self._build_recommendation_prompt(
                user_preferences, current_location, time_context, limit
            )
            
            # Get recommendations from Gemini
            response = await self.llm.ainvoke(prompt)
            
            # Parse recommendations
            recommendations = self._parse_recommendations(response.content)
            
            # Clean markdown formatting from all text fields
            for rec in recommendations:
                if 'description' in rec:
                    rec['description'] = clean_markdown_formatting(rec['description'])
                if 'reasons' in rec:
                    rec['reasons'] = [clean_markdown_formatting(reason) for reason in rec['reasons']]
            
            # Store in cache
            self._store_in_cache(cache_key, recommendations)
            
            return recommendations[:limit]
            
        except Exception as e:
            logger.error(f"Recommendation error: {e}")
            # Return fallback recommendations on error to avoid quota waste
            return self._create_fallback_recommendations("")[:limit]
    
    def _build_recommendation_prompt(
        self,
        user_preferences: Dict[str, Any],
        current_location: Optional[str],
        time_context: Optional[str],
        limit: int
    ) -> str:
        """Build prompt for personalized recommendations"""
        
        # Extract user preferences
        interests = user_preferences.get("interests", [])
        budget = user_preferences.get("budget", "medium")
        food_preferences = user_preferences.get("food_preferences", [])
        activity_level = user_preferences.get("activity_level", "moderate")
        group_type = user_preferences.get("group_type", "solo")
        
        # Build context
        location_context = f"Current location: {current_location}" if current_location else "Location: Hong Kong"
        time_context_info = f"Time context: {time_context}" if time_context else ""
        
        return f"""
        You are a local Hong Kong expert providing personalized recommendations.
        
        User Profile:
        - Interests: {', '.join(interests) if interests else 'general sightseeing'}
        - Budget preference: {budget}
        - Food preferences: {', '.join(food_preferences) if food_preferences else 'open to local cuisine'}
        - Activity level: {activity_level}
        - Group type: {group_type}
        
        Context:
        - {location_context}
        - {time_context_info}
        
        Hong Kong Knowledge:
        
        ATTRACTIONS:
        - Victoria Peak (iconic views, Peak Tram, Sky Terrace 428)
        - Star Ferry (historic harbor crossing, cheap, great views)
        - Temple Street Night Market (street food, fortune telling, shopping)
        - Tsim Sha Tsui Promenade (waterfront walk, Symphony of Lights)
        - Man Mo Temple (traditional temple, incense coils)
        - Wong Tai Sin Temple (fortune telling, colorful)
        - Dragon's Back (hiking trail, stunning views)
        - Big Buddha & Po Lin Monastery (Lantau Island, cable car)
        - Avenue of Stars (harbor views, Bruce Lee statue)
        - Ladies' Market (bargain shopping, street food)
        
        FOOD EXPERIENCES:
        - Dim sum at traditional tea houses (har gow, siu mai, cha siu bao)
        - Roast goose and char siu (Kam's Roast Goose, Joy Hing)
        - Street food (curry fish balls, egg waffles, stinky tofu)
        - Hong Kong-style milk tea and pineapple buns
        - Michelin street food (Tim Ho Wan, Hawker Chan)
        - Traditional cha chaan teng (tea restaurants)
        
        NEIGHBORHOODS:
        - Central: Business district, upscale shopping, IFC Mall
        - Tsim Sha Tsui: Tourist hub, museums, harbor views
        - Causeway Bay: Shopping paradise, Times Square, food courts
        - Mong Kok: Local life, night markets, electronics
        - Wan Chai: Mix of old and new, wet markets, bars
        - Sheung Wan: Trendy area, art galleries, dried seafood streets
        
        Please provide {limit} personalized recommendations in this exact format:
        
        RECOMMENDATION 1:
        Name: [Specific place/activity name]
        Category: [attraction/food/shopping/culture/nature]
        Location: [Specific location with MTR station]
        Description: [2-3 sentences about what makes this special]
        Why recommended: [Specific reasons based on user preferences]
        Best time: [When to visit]
        Estimated time: [How long to spend]
        Cost range: [Budget estimate in HKD]
        Tips: [Practical advice]
        
        [Continue for all recommendations]
        
        Focus on authentic Hong Kong experiences that match the user's preferences and current context.
        """
    
    def _parse_recommendations(self, response: str) -> List[Dict[str, Any]]:
        """Parse LLM response into structured recommendations"""
        try:
            recommendations = []
            
            # Split by recommendation blocks
            blocks = response.split('RECOMMENDATION ')
            
            for block in blocks[1:]:  # Skip first empty split
                try:
                    recommendation = self._parse_single_recommendation(block)
                    if recommendation:
                        recommendations.append(recommendation)
                except Exception as e:
                    logger.warning(f"Failed to parse recommendation block: {e}")
                    continue
            
            # If parsing failed, create fallback recommendations
            if not recommendations:
                recommendations = self._create_fallback_recommendations(response)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to parse recommendations: {e}")
            return self._create_fallback_recommendations(response)
    
    def _parse_single_recommendation(self, block: str) -> Optional[Dict[str, Any]]:
        """Parse a single recommendation block"""
        try:
            lines = block.strip().split('\n')
            recommendation = {
                "name": "",
                "category": "",
                "location": "",
                "description": "",
                "rating": 4.5,  # Default rating
                "estimated_time": "",
                "cost_range": "",
                "reasons": []
            }
            
            current_field = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check for field headers
                if line.startswith('Name:'):
                    recommendation["name"] = line.replace('Name:', '').strip()
                elif line.startswith('Category:'):
                    recommendation["category"] = line.replace('Category:', '').strip()
                elif line.startswith('Location:'):
                    recommendation["location"] = line.replace('Location:', '').strip()
                elif line.startswith('Description:'):
                    recommendation["description"] = line.replace('Description:', '').strip()
                    current_field = "description"
                elif line.startswith('Why recommended:'):
                    reason_text = line.replace('Why recommended:', '').strip()
                    if reason_text:
                        recommendation["reasons"].append(reason_text)
                    current_field = "reasons"
                elif line.startswith('Best time:'):
                    pass  # We can ignore this for now
                elif line.startswith('Estimated time:'):
                    recommendation["estimated_time"] = line.replace('Estimated time:', '').strip()
                elif line.startswith('Cost range:'):
                    recommendation["cost_range"] = line.replace('Cost range:', '').strip()
                elif line.startswith('Tips:'):
                    # Add tips to reasons
                    tip = line.replace('Tips:', '').strip()
                    if tip:
                        recommendation["reasons"].append(f"Tip: {tip}")
                elif current_field == "description" and not any(line.startswith(field) for field in ['Why recommended:', 'Best time:', 'Estimated time:', 'Cost range:', 'Tips:']):
                    # Continue description
                    recommendation["description"] += " " + line
                elif current_field == "reasons" and not any(line.startswith(field) for field in ['Best time:', 'Estimated time:', 'Cost range:', 'Tips:']):
                    # Continue reasons
                    recommendation["reasons"].append(line)
            
            # Validate recommendation has minimum required fields
            if recommendation["name"] and recommendation["description"]:
                return recommendation
            
            return None
            
        except Exception as e:
            logger.error(f"Error parsing single recommendation: {e}")
            return None
    
    def _create_fallback_recommendations(self, response: str) -> List[Dict[str, Any]]:
        """Create fallback recommendations if parsing fails"""
        # Default Hong Kong recommendations
        fallback_recommendations = [
            {
                "name": "Victoria Peak",
                "description": "Hong Kong's most famous attraction offering panoramic views of the city skyline and Victoria Harbour.",
                "category": "attraction",
                "location": "Central MTR Station, then Peak Tram",
                "rating": 4.6,
                "estimated_time": "2-3 hours",
                "cost_range": "HK$65 (Peak Tram) + HK$30 (Sky Terrace)",
                "reasons": ["Iconic Hong Kong experience", "Best city views", "Historic Peak Tram"]
            },
            {
                "name": "Star Ferry",
                "description": "Historic ferry service crossing Victoria Harbour since 1888, offering beautiful harbor views.",
                "category": "attraction",
                "location": "Central Pier or Tsim Sha Tsui Pier",
                "rating": 4.4,
                "estimated_time": "30 minutes",
                "cost_range": "HK$3-4",
                "reasons": ["Authentic Hong Kong experience", "Very affordable", "Great for photos"]
            },
            {
                "name": "Tim Ho Wan",
                "description": "World's cheapest Michelin-starred restaurant famous for BBQ pork buns and dim sum.",
                "category": "food",
                "location": "Multiple locations (Mong Kok, Central, etc.)",
                "rating": 4.3,
                "estimated_time": "1 hour",
                "cost_range": "HK$50-100 per person",
                "reasons": ["Michelin-starred food", "Affordable luxury", "Must-try dim sum"]
            },
            {
                "name": "Temple Street Night Market",
                "description": "Vibrant night market with street food, fortune telling, and local atmosphere.",
                "category": "culture",
                "location": "Yau Ma Tei MTR Station",
                "rating": 4.2,
                "estimated_time": "2 hours",
                "cost_range": "HK$50-200",
                "reasons": ["Authentic local experience", "Great street food", "Cultural immersion"]
            },
            {
                "name": "Dragon's Back",
                "description": "Award-winning hiking trail offering stunning views of Hong Kong's coastline and islands.",
                "category": "nature",
                "location": "Shek O MTR then bus/taxi",
                "rating": 4.7,
                "estimated_time": "3-4 hours",
                "cost_range": "HK$20 (transport only)",
                "reasons": ["Best hiking in Hong Kong", "Amazing coastal views", "Great exercise"]
            }
        ]
        
        return fallback_recommendations

    def _create_cache_key(
        self,
        user_preferences: Dict[str, Any],
        current_location: Optional[str],
        time_context: Optional[str],
        limit: int,
        session_id: Optional[str] = None
    ) -> str:
        """Create a cache key from request parameters"""
        # Create a string representation of the parameters
        cache_data = {
            "preferences": user_preferences,
            "location": current_location,
            "time": time_context,
            "limit": limit,
            "session": session_id  # Include session for user-specific caching
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[List[Dict[str, Any]]]:
        """Get recommendations from cache if not expired"""
        if cache_key in self._cache:
            cache_entry = self._cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self._cache_timeout:
                return cache_entry["data"]
            else:
                # Remove expired entry
                del self._cache[cache_key]
        return None
    
    def _store_in_cache(self, cache_key: str, recommendations: List[Dict[str, Any]]):
        """Store recommendations in cache"""
        self._cache[cache_key] = {
            "data": recommendations,
            "timestamp": time.time()
        }
        
        # Simple cache size management
        if len(self._cache) > 100:  # Keep only 100 entries
            # Remove oldest entries
            oldest_keys = sorted(
                self._cache.keys(),
                key=lambda k: self._cache[k]["timestamp"]
            )[:50]
            for key in oldest_keys:
                del self._cache[key]
    
    def _is_basic_request(self, user_preferences: Dict[str, Any]) -> bool:
        """Check if this is a basic request that can use fallback data"""
        # Never use fallback - always make LLM call for personalized recommendations
        # This ensures users get fresh, AI-generated recommendations each time
        return False
