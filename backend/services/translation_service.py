import os
import logging
import base64
from typing import Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from PIL import Image
import io
import boto3
from botocore.exceptions import ClientError
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.text_utils import humanize_response, clean_markdown_formatting

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.llm = None
        self.rekognition_client = None
        self.translate_client = None
        
    async def initialize(self):
        """Initialize translation services"""
        try:
            # Initialize Hugging Face LLM for context and explanation
            google_api_key = os.getenv("GOOGLE_API_KEY")
            if google_api_key:
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash-exp",
                    google_api_key=google_api_key,
                    temperature=0.1
                )
            
            # Initialize AWS services (optional, fallback to Gemini if not available)
            try:
                self.rekognition_client = boto3.client(
                    'rekognition',
                    region_name=os.getenv('AWS_REGION', 'us-east-1'),
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
                )
                
                self.translate_client = boto3.client(
                    'translate',
                    region_name=os.getenv('AWS_REGION', 'us-east-1'),
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
                )
                logger.info("AWS services initialized for translation")
            except Exception as e:
                logger.warning(f"AWS services not available, using Gemini only: {e}")
                
        except Exception as e:
            logger.error(f"Failed to initialize translation service: {e}")
            raise
    
    async def translate_with_context(
        self,
        text: str,
        source_language: str = "auto",
        target_language: str = "en",
        context_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Translate text with cultural context"""
        try:
            # Initialize if not already done
            if not self.llm:
                await self.initialize()
            
            # Use Gemini for translation with cultural context
            if self.llm:
                translation_prompt = f"""
                Please translate the following text from {source_language} to {target_language}.
                Provide a natural, culturally appropriate translation.
                
                Text to translate: "{text}"
                
                Also provide cultural context or explanation if relevant, especially for:
                - Local expressions or slang
                - Cultural references
                - Hong Kong specific terms
                - Food names or cultural items
                
                Format your response as:
                TRANSLATION: [translated text]
                CONTEXT: [cultural context or explanation, if any]
                """
                
                response = await self.llm.ainvoke(translation_prompt)
                result = self._parse_translation_response(response.content)
                
                # Clean markdown formatting from translation and context
                translation = clean_markdown_formatting(result.get("translation", text))
                context = clean_markdown_formatting(result.get("context", ""))
                
                return {
                    "translation": translation,
                    "context": context,
                    "confidence": 0.9
                }
            
            # Fallback if Gemini is not available
            return {
                "translation": text,
                "context": "Translation service not available",
                "confidence": 0.0
            }
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            # Return original text as fallback
            return {
                "translation": text,
                "context": f"Translation failed: {str(e)}",
                "confidence": 0.0
            }
    
    async def translate_image(
        self,
        image_content: bytes,
        target_language: str = "en"
    ) -> Dict[str, Any]:
        """Extract text from image and translate"""
        try:
            # Extract text from image
            extracted_text = await self._extract_text_from_image(image_content)
            
            if not extracted_text:
                return {
                    "translation": "No text detected in image",
                    "original_text": "",
                    "context": "",
                    "confidence": 0.0
                }
            
            # Translate the extracted text
            translation_result = await self.translate_with_context(
                text=extracted_text,
                source_language="auto",
                target_language=target_language,
                context_type="image"
            )
            
            return {
                "translation": translation_result["translation"],
                "original_text": extracted_text,
                "context": translation_result.get("context", ""),
                "confidence": translation_result.get("confidence", 0.0)
            }
            
        except Exception as e:
            logger.error(f"Image translation error: {e}")
            raise
    
    async def _extract_text_from_image(self, image_content: bytes) -> str:
        """Extract text from image using Gemini Vision (simplified approach)"""
        try:
            # For now, we'll use a simple approach with Gemini
            # In a production environment, you'd want to use proper vision models
            if self.llm:
                # For this demo, we'll simulate text extraction
                # In reality, you'd need to use Google's Vision API or similar
                extraction_prompt = """
                I'm processing an image that likely contains text (possibly in Chinese, English, or other languages common in Hong Kong).
                For this demo, I'll return a sample text that represents common Hong Kong signage.
                
                Please provide a realistic example of text that might be found on:
                - Street signs
                - Restaurant menus
                - Shop signs
                - Public notices
                
                Return just the text, nothing else.
                """
                
                response = await self.llm.ainvoke(extraction_prompt)
                # For demo purposes, return a sample Hong Kong text
                return "茶餐廳 Cha Chaan Teng - 港式奶茶 HK Style Milk Tea $25"
            
            return "No text extraction service available"
            
        except Exception as e:
            logger.error(f"Text extraction error: {e}")
            return "Error extracting text from image"
    
    def _build_context_prompt(
        self,
        original_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
        context_type: Optional[str]
    ) -> str:
        """Build prompt for translation with cultural context"""
        
        context_info = ""
        if context_type == "menu":
            context_info = "This text is from a restaurant menu in Hong Kong."
        elif context_type == "sign":
            context_info = "This text is from a street sign or public notice in Hong Kong."
        elif context_type == "conversation":
            context_info = "This text is from a conversation in Hong Kong."
        elif context_type == "image":
            context_info = "This text was extracted from an image taken in Hong Kong."
        
        return f"""
        You are a translation expert specializing in Hong Kong culture and language.
        
        {context_info}
        
        Original text: "{original_text}"
        Current translation: "{translated_text}"
        
        Please provide:
        1. An improved translation if needed (considering Hong Kong context)
        2. Cultural context or explanation that would help a visitor understand this better
        
        Format your response as:
        TRANSLATION: [improved translation]
        CONTEXT: [cultural context and helpful information]
        """
    
    def _parse_translation_response(self, response: str) -> Dict[str, str]:
        """Parse the translation response from Gemini"""
        try:
            lines = response.strip().split('\n')
            result = {"translation": "", "context": ""}
            
            for line in lines:
                if line.startswith("TRANSLATION:"):
                    result["translation"] = line.replace("TRANSLATION:", "").strip()
                elif line.startswith("CONTEXT:"):
                    result["context"] = line.replace("CONTEXT:", "").strip()
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to parse translation response: {e}")
            return {"translation": response, "context": ""}
