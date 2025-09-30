"""
AWS Bedrock service for LLM interactions.
Replaces Google Gemini with AWS Bedrock models available in Hong Kong.
"""
import os
import logging
import boto3
from typing import Dict, Any, Optional
from langchain_aws import ChatBedrock
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class BedrockService:
    """
    AWS Bedrock service for LLM interactions.
    Uses Claude 3.5 Sonnet which is available in Hong Kong region.
    """
    
    def __init__(self):
        self.bedrock_client = None
        self.chat_model = None
        self.region = "ap-southeast-1"  # Singapore region (closest to Hong Kong)
        
    async def initialize(self):
        """Initialize AWS Bedrock service"""
        try:
            # Initialize Bedrock client
            self.bedrock_client = boto3.client(
                'bedrock-runtime',
                region_name=self.region,
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
            )
            
            # Initialize Claude 3.5 Sonnet chat model
            self.chat_model = ChatBedrock(
                client=self.bedrock_client,
                model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
                model_kwargs={
                    "max_tokens": 2000,
                    "temperature": 0.3,
                    "top_p": 0.9
                }
            )
            
            # Test the connection
            await self._test_connection()
            
            logger.info(f"✅ AWS Bedrock initialized successfully with Claude 3.5 Sonnet in {self.region}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize AWS Bedrock: {e}")
            # Fall back to a basic response system
            self.chat_model = None
            logger.warning("🔄 Will use fallback responses due to Bedrock initialization failure")
    
    async def _test_connection(self):
        """Test AWS Bedrock connection"""
        try:
            test_response = await self.chat_model.ainvoke("Hello")
            logger.info("🔍 Bedrock connection test successful")
        except Exception as e:
            logger.warning(f"⚠️ Bedrock test failed: {e}")
            raise
    
    async def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a chat message to Claude and get response
        """
        try:
            if not self.chat_model:
                return self._get_fallback_response(message)
            
            # Prepare the full prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {message}\n\nAssistant:"
            else:
                full_prompt = message
            
            # Get response from Claude
            response = await self.chat_model.ainvoke(full_prompt)
            
            # Clean the response content
            if hasattr(response, 'content'):
                return response.content.strip()
            else:
                return str(response).strip()
                
        except ClientError as e:
            logger.error(f"AWS Bedrock API error: {e}")
            return self._get_fallback_response(message)
        except Exception as e:
            logger.error(f"Bedrock chat error: {e}")
            return self._get_fallback_response(message)
    
    def _get_fallback_response(self, message: str) -> str:
        """
        Provide fallback responses when Bedrock is not available
        """
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['food', 'eat', 'restaurant', 'dim sum']):
            return """Hong Kong offers incredible dining experiences! Here are some must-try options:

• Dim Sum: Try traditional tea houses like Lin Heung or modern spots like Tim Ho Wan (Michelin-starred)
• Street Food: Explore Temple Street Night Market for curry fish balls and egg waffles  
• Roast Meats: Visit Kam's Roast Goose or Joy Hing for authentic Cantonese roast duck and char siu
• Cha Chaan Teng: Experience local tea restaurants for Hong Kong-style milk tea and pineapple buns

Each district has its own food specialties. What type of cuisine interests you most?"""

        elif any(word in message_lower for word in ['attraction', 'see', 'visit', 'sightseeing']):
            return """Hong Kong has amazing attractions for every interest:

• Victoria Peak: Take the historic Peak Tram for stunning harbor views
• Star Ferry: Enjoy this century-old ferry ride across Victoria Harbour  
• Temple Street Night Market: Experience the vibrant night market culture
• Man Mo Temple: Visit this beautiful traditional temple with hanging incense coils
• Dragon's Back: Hike this award-winning trail for coastal views
• Big Buddha: Take the cable car to Lantau Island's giant bronze Buddha

What type of experiences are you most interested in - cultural sites, nature, shopping, or nightlife?"""

        elif any(word in message_lower for word in ['transport', 'mtr', 'taxi', 'travel']):
            return """Getting around Hong Kong is easy and efficient:

• MTR (Subway): Fast, clean, and connects all major areas. Get an Octopus Card for easy payment
• Star Ferry: Historic and scenic way to cross the harbor between Central and Tsim Sha Tsui
• Trams: Slow but charming way to see Hong Kong Island 
• Taxis: Red taxis for urban areas, green for New Territories
• Airport Express: Quick 24-minute ride from airport to Central

The MTR is usually your best option. Download the MTR Mobile app for real-time updates and route planning."""

        else:
            return """Welcome to Hong Kong! I'm here to help you explore this amazing city.

I can assist you with:
• Restaurant and food recommendations
• Tourist attractions and sightseeing  
• Transportation and getting around
• Cultural experiences and local tips
• Shopping and entertainment

What would you like to know about Hong Kong? Feel free to ask me anything about attractions, food, culture, or practical travel tips!"""

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        if self.chat_model:
            return {
                "provider": "AWS Bedrock",
                "model": "Claude 3.5 Sonnet",
                "region": self.region,
                "status": "connected"
            }
        else:
            return {
                "provider": "Fallback System",
                "model": "Rule-based responses",
                "region": "local",
                "status": "fallback_mode"
            }

# Global instance
bedrock_service = BedrockService()
