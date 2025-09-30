import os
import logging
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime, timedelta
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.text_utils import humanize_response, clean_markdown_formatting

logger = logging.getLogger(__name__)

class ItineraryService:
    def __init__(self):
        self.llm = None
        
    async def initialize(self):
        """Initialize itinerary service"""
        try:
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if not google_api_key:
                raise ValueError("GOOGLE_API_KEY not found")
            
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                google_api_key=google_api_key,
                temperature=0.4
            )
            
            logger.info("Itinerary service initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize itinerary service: {e}")
            raise
    
    async def generate_itinerary(
        self,
        duration: int,
        interests: List[str],
        budget: str,
        accommodation: str = None,
        travel_style: str = "moderate",
        group_size: int = 1,
        special_requirements: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Generate a personalized Hong Kong itinerary"""
        try:
            # Build comprehensive prompt
            prompt = self._build_itinerary_prompt(
                duration, interests, budget, accommodation, 
                travel_style, group_size, special_requirements
            )
            
            # Generate itinerary
            response = await self.llm.ainvoke(prompt)
            
            # Debug: Log the raw response
            logger.info(f"Raw LLM response: {response.content[:500]}...")
            
            # Parse and structure the response
            itinerary = self._parse_itinerary_response(response.content, duration)
            
            return itinerary
            
        except Exception as e:
            logger.error(f"Itinerary generation error: {e}")
            raise
    
    def _build_itinerary_prompt(
        self,
        duration: int,
        interests: List[str],
        budget: str,
        accommodation: str,
        travel_style: str,
        group_size: int,
        special_requirements: List[str]
    ) -> str:
        """Build detailed prompt for itinerary generation"""
        
        budget_guidance = {
            "low": "Budget-friendly options (HK$200-500 per day), street food, free attractions, public transport",
            "medium": "Moderate spending (HK$500-1000 per day), mix of experiences, some dining out",
            "high": "Premium experiences (HK$1000+ per day), fine dining, private transport, luxury activities"
        }
        
        travel_style_guidance = {
            "slow": "Relaxed pace, 2-3 activities per day, plenty of rest time",
            "moderate": "Balanced pace, 3-4 activities per day, some flexibility",
            "fast": "Packed schedule, 4-5 activities per day, maximize experiences"
        }
        
        interests_context = ", ".join(interests) if interests else "general sightseeing"
        budget_info = budget_guidance.get(budget, budget_guidance["medium"])
        style_info = travel_style_guidance.get(travel_style, travel_style_guidance["moderate"])
        
        accommodation_info = f"Starting point: {accommodation}" if accommodation else "Central Hong Kong area"
        requirements_info = f"Special requirements: {', '.join(special_requirements)}" if special_requirements else ""
        
        return f"""
        You are an expert Hong Kong travel planner. Create a detailed {duration}-day itinerary for Hong Kong.
        
        Traveler Profile:
        - Group size: {group_size} person(s)
        - Interests: {interests_context}
        - Budget: {budget} ({budget_info})
        - Travel style: {travel_style} ({style_info})
        - {accommodation_info}
        {requirements_info}
        
        Hong Kong Knowledge Base:
        - Must-visit: Victoria Peak, Star Ferry, Temple Street Night Market, Tsim Sha Tsui Promenade
        - Food: Dim sum, roast goose, egg waffles, milk tea, street food markets
        - Culture: Man Mo Temple, Wong Tai Sin Temple, Heritage Museum, Space Museum
        - Nature: Dragon's Back hike, Repulse Bay, Lantau Island, Big Buddha
        - Shopping: Central, Causeway Bay, Mong Kok, Ladies' Market
        - Transport: MTR (very efficient), Star Ferry, Peak Tram, taxis, Airport Express
        - Practical: Octopus Card essential, most signs in English/Chinese, very safe city
        
        Please create a detailed itinerary with the following structure for each day:
        
        Day X:
        Morning (9:00-12:00):
        - Activity: [Specific attraction/activity]
        - Duration: [Time needed]
        - Cost: [Estimated cost in HKD]
        - Transport: [How to get there]
        - Tips: [Practical advice]
        
        Afternoon (12:00-18:00):
        - [Same structure]
        
        Evening (18:00-22:00):
        - [Same structure]
        
        Daily Total Cost: [HKD amount]
        Daily Transport Tips: [MTR lines, walking distances, etc.]
        
        Important Requirements:
        1. Include specific MTR stations and transport directions
        2. Suggest actual restaurant names where possible
        3. Include estimated costs in HKD
        4. Consider Hong Kong's geography (Hong Kong Island vs Kowloon vs New Territories)
        5. Account for travel time between locations
        6. Include both tourist attractions and local experiences
        7. Suggest backup indoor activities for each day (in case of rain)
        8. Include cultural etiquette tips relevant to planned activities
        
        Format the response as a structured daily plan that can be easily parsed.
        """
    
    def _parse_itinerary_response(self, response: str, duration: int) -> List[Dict[str, Any]]:
        """Parse the LLM response into structured itinerary"""
        try:
            # Clean markdown formatting
            response = clean_markdown_formatting(response)
            
            # Simple approach: create days with basic parsing
            days = []
            
            # Split into sections by looking for day patterns
            import re
            day_sections = re.split(r'(?i)(?:\*\*)?day\s+(\d+)(?:\*\*)?[:\-]', response)
            
            # Process each day section
            for i in range(1, len(day_sections), 2):
                if i + 1 < len(day_sections):
                    day_num = int(day_sections[i])
                    day_content = day_sections[i + 1]
                    
                    activities = self._extract_activities_simple(day_content)
                    
                    days.append({
                        "day": day_num,
                        "activities": activities,
                        "estimated_cost": sum(act.get("cost", 0) for act in activities),
                        "transportation_info": self._extract_transport_info_simple(day_content)
                    })
            
            # If no days parsed, create fallback
            if not days:
                days = self._create_fallback_itinerary(response, duration)
            
            # Ensure we have the right number of days
            while len(days) < duration:
                days.append({
                    "day": len(days) + 1,
                    "activities": [],
                    "estimated_cost": 0,
                    "transportation_info": ""
                })
            
            return days[:duration]  # Limit to requested duration
            
        except Exception as e:
            logger.error(f"Error parsing itinerary: {e}")
            return self._create_fallback_itinerary(response, duration)
    
    def _extract_activities_simple(self, day_content: str) -> List[Dict[str, Any]]:
        """Extract activities from day content"""
        activities = []
        lines = day_content.split('\n')
        
        current_activity = None
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and time headers
            if not line or any(time_word in line.lower() for time_word in ['morning', 'afternoon', 'evening']):
                continue
            
            # Look for activity lines
            if line.startswith('- Activity:') or 'Activity:' in line:
                if current_activity:
                    activities.append(current_activity)
                
                activity_name = line.split('Activity:', 1)[1].strip() if 'Activity:' in line else line[2:].strip()
                current_activity = {
                    "name": activity_name,
                    "time": "",
                    "duration": "",
                    "cost": 0,
                    "description": activity_name,
                    "transport": "",
                    "tips": ""
                }
            
            elif current_activity and line.startswith('-'):
                # Parse additional details
                if 'Duration:' in line:
                    current_activity["duration"] = line.split('Duration:', 1)[1].strip()
                elif 'Cost:' in line:
                    current_activity["cost"] = self._extract_cost_number(line.split('Cost:', 1)[1].strip())
                elif 'Transport:' in line:
                    current_activity["transport"] = line.split('Transport:', 1)[1].strip()
                elif 'Tips:' in line:
                    current_activity["tips"] = line.split('Tips:', 1)[1].strip()
        
        # Add the last activity
        if current_activity:
            activities.append(current_activity)
        
        return activities
    
    def _extract_transport_info_simple(self, content: str) -> str:
        """Extract transport info from content"""
        transport_keywords = ['MTR', 'station', 'train', 'bus', 'taxi', 'ferry', 'tram']
        transport_lines = []
        
        for line in content.split('\n'):
            if any(keyword.lower() in line.lower() for keyword in transport_keywords):
                transport_lines.append(line.strip())
        
        return '; '.join(transport_lines[:3])  # Limit to 3 lines
    
    def _parse_activity_block(self, lines: List[str], start_index: int) -> Dict[str, Any]:
        """Parse a single activity block"""
        try:
            activity = {
                "name": "",
                "time": "",
                "duration": "",
                "cost": 0,
                "description": "",
                "transport": "",
                "tips": ""
            }
            
            for i in range(start_index, min(start_index + 10, len(lines))):
                if i >= len(lines):
                    break
                    
                line = lines[i].strip()
                
                if line.startswith('- Activity:') or line.startswith('Activity:'):
                    activity["name"] = line.split(':', 1)[1].strip()
                elif line.startswith('- Duration:') or line.startswith('Duration:'):
                    activity["duration"] = line.split(':', 1)[1].strip()
                elif line.startswith('- Cost:') or line.startswith('Cost:'):
                    cost_text = line.split(':', 1)[1].strip()
                    activity["cost"] = self._extract_cost_number(cost_text)
                elif line.startswith('- Transport:') or line.startswith('Transport:'):
                    activity["transport"] = line.split(':', 1)[1].strip()
                elif line.startswith('- Tips:') or line.startswith('Tips:'):
                    activity["tips"] = line.split(':', 1)[1].strip()
                elif line.startswith('- ') and activity["name"]:
                    # Additional description
                    activity["description"] += line[2:] + " "
            
            return activity if activity["name"] else None
            
        except Exception as e:
            logger.error(f"Failed to parse activity block: {e}")
            return None
    
    def _extract_cost_number(self, cost_text: str) -> float:
        """Extract numeric cost from text"""
        try:
            # Remove currency symbols and extract numbers
            import re
            numbers = re.findall(r'\d+(?:\.\d+)?', cost_text.replace(',', ''))
            if numbers:
                return float(numbers[0])
            return 0.0
        except:
            return 0.0
    
    def _extract_daily_cost(self, activities: List[Dict[str, Any]]) -> float:
        """Calculate total daily cost from activities"""
        try:
            return sum(activity.get("cost", 0) for activity in activities)
        except:
            return 0.0
    
    def _extract_transport_info(self, activities: List[Dict[str, Any]]) -> str:
        """Extract transportation information from activities"""
        try:
            transport_info = []
            for activity in activities:
                if activity.get("transport"):
                    transport_info.append(activity["transport"])
            return "; ".join(set(transport_info))
        except:
            return ""
    
    def _create_fallback_itinerary(self, response: str, duration: int) -> List[Dict[str, Any]]:
        """Create a simple fallback itinerary structure"""
        days = []
        
        # Split response into roughly equal parts for each day
        response_parts = response.split('\n\n')
        part_size = max(1, len(response_parts) // duration)
        
        for day in range(1, duration + 1):
            start_idx = (day - 1) * part_size
            end_idx = day * part_size
            day_content = '\n'.join(response_parts[start_idx:end_idx])
            
            days.append({
                "day": day,
                "activities": [{
                    "name": f"Day {day} Activities",
                    "time": "Full Day",
                    "duration": "8 hours",
                    "cost": 500,  # Default estimate
                    "description": day_content[:500] + "..." if len(day_content) > 500 else day_content,
                    "transport": "MTR and walking",
                    "tips": "Check specific attraction opening hours"
                }],
                "estimated_cost": 500,
                "transportation_info": "Use MTR system with Octopus Card"
            })
        
        return days
