"""
SignSpeak - Google Gemini Language Engine
Transforms raw gesture words into natural, context-aware sentences
"""

import google.generativeai as genai
import os
from typing import Optional

class GeminiLanguageEngine:
    """Contextual language processing using Google Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini language engine
        
        Args:
            api_key: Google AI Studio API key. If None, reads from GEMINI_API_KEY env var
        """
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError(
                "Gemini API key not provided. "
                "Set GEMINI_API_KEY environment variable or pass api_key parameter."
            )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Context prompt for natural sentence generation
        self.system_prompt = """You are a helpful assistant that converts sign language gesture words into natural, polite, and contextually appropriate spoken sentences.

Rules:
1. Convert single gesture words (like "WATER", "HELLO", "THANK_YOU") into natural spoken sentences
2. Make sentences polite and conversational
3. Keep sentences concise (1-2 sentences max)
4. If the gesture is a greeting, respond with a greeting
5. If the gesture is a request, phrase it as a polite request
6. If the gesture is a statement, make it a natural statement

Examples:
- "WATER" → "Could I please have some water?"
- "HELLO" → "Hello, how are you?"
- "THANK_YOU" → "Thank you very much!"
- "YES" → "Yes, that's correct."
- "NO" → "No, thank you."

Now convert this gesture word into a natural sentence:"""
    
    def generate_sentence(self, gesture_word: str) -> str:
        """
        Generate natural sentence from gesture word
        
        Args:
            gesture_word: Raw gesture label (e.g., "WATER", "HELLO")
            
        Returns:
            Natural spoken sentence (e.g., "Could I please have some water?")
        """
        try:
            prompt = f"{self.system_prompt}\n\nGesture: {gesture_word}"
            response = self.model.generate_content(prompt)
            
            # Extract the generated sentence
            sentence = response.text.strip()
            
            # Fallback if API fails
            if not sentence or len(sentence) > 200:
                return self._fallback_sentence(gesture_word)
            
            return sentence
            
        except Exception as e:
            print(f"⚠️ Gemini API error: {e}. Using fallback sentence.")
            return self._fallback_sentence(gesture_word)
    
    def _fallback_sentence(self, gesture_word: str) -> str:
        """
        Fallback sentence generation if API fails
        
        Args:
            gesture_word: Raw gesture label
            
        Returns:
            Simple fallback sentence
        """
        # Simple fallback mappings
        fallback_map = {
            "WATER": "Could I please have some water?",
            "HELLO": "Hello, how are you?",
            "THANK_YOU": "Thank you very much!",
            "YES": "Yes, that's correct.",
            "NO": "No, thank you.",
            "WE": "We are here.",
            "I": "I am here.",
        }
        
        # Return mapped sentence or default format
        if gesture_word.upper() in fallback_map:
            return fallback_map[gesture_word.upper()]
        
        # Default: convert to sentence
        return f"I would like {gesture_word.lower()}."

