"""
Text utility functions for cleaning and formatting LLM responses
"""
import re
import logging

logger = logging.getLogger(__name__)

def clean_markdown_formatting(text: str) -> str:
    """
    Remove markdown formatting from text to make it more human-readable.
    This removes **bold**, *italic*, and other markdown syntax.
    """
    if not text:
        return text
    
    try:
        # Remove bold formatting (**text** or __text__)
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'__(.*?)__', r'\1', text)
        
        # Remove italic formatting (*text* or _text_)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        text = re.sub(r'_(.*?)_', r'\1', text)
        
        # Remove code blocks (```text```)
        text = re.sub(r'```(.*?)```', r'\1', text, flags=re.DOTALL)
        
        # Remove inline code (`text`)
        text = re.sub(r'`(.*?)`', r'\1', text)
        
        # Remove headers (# ## ### etc.)
        text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
        
        # Remove horizontal rules (--- or ***)
        text = re.sub(r'^[-*]{3,}\s*$', '', text, flags=re.MULTILINE)
        
        # Remove extra whitespace and clean up
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Replace multiple newlines with double
        text = text.strip()
        
        return text
        
    except Exception as e:
        logger.warning(f"Error cleaning markdown formatting: {e}")
        return text

def format_for_display(text: str, max_length: int = None) -> str:
    """
    Format text for user-friendly display.
    """
    if not text:
        return text
    
    # Clean markdown first
    text = clean_markdown_formatting(text)
    
    # Ensure proper sentence spacing
    text = re.sub(r'\.([A-Z])', r'. \1', text)
    
    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length].rsplit(' ', 1)[0] + "..."
    
    return text

def extract_key_points(text: str, max_points: int = 5) -> list:
    """
    Extract key points from text for better readability.
    """
    if not text:
        return []
    
    # Clean the text first
    text = clean_markdown_formatting(text)
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Return first few sentences as key points
    return sentences[:max_points]

def humanize_response(text: str) -> str:
    """
    Make LLM response more human-friendly by cleaning formatting
    and improving readability.
    """
    if not text:
        return text
    
    # Clean markdown formatting
    text = clean_markdown_formatting(text)
    
    # Improve readability
    text = format_for_display(text)
    
    # Add friendly touches
    if text and not text.endswith(('.', '!', '?')):
        text += '.'
    
    return text
