import os
import json
import logging
from functools import lru_cache
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class OpenAIHelper:
    """Helper class for OpenAI API interactions with caching to minimize costs."""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = "gpt-3.5-turbo"
        self.cache = {}
        
    def is_configured(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.api_key)
    
    @lru_cache(maxsize=128)
    def generate_movie_summary(self, movie_title: str, overview: str, genres: str) -> Dict:
        """Generate AI-powered summary and recommendation explanation."""
        if not self.is_configured():
            logger.warning("OpenAI API not configured")
            return {
                'summary': overview,
                'why_recommended': 'This movie matches your interests based on content similarity.',
                'perfect_for': genres,
                'vibe': 'Unknown'
            }
        
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""You are a helpful movie recommendation assistant. For the movie "{movie_title}" with genres {genres} and overview: {overview[:200]}...

Please provide in JSON format:
{{
  "summary": "A 1-2 sentence engaging summary",
  "why_recommended": "Why someone would enjoy this based on themes",
  "perfect_for": "Who would love this movie",
  "vibe": "One-word vibe (e.g., Thrilling, Heartwarming, Mind-bending)"
}}

Respond ONLY with valid JSON, no markdown or extra text."""

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a movie recommendation expert. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=200,
                timeout=10
            )
            
            content = response['choices'][0]['message']['content'].strip()
            
            # Remove markdown code blocks if present
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            
            result = json.loads(content.strip())
            logger.info(f"Generated AI summary for {movie_title}")
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in AI response: {e}")
            return {
                'summary': overview[:150],
                'why_recommended': 'This movie matches your interests.',
                'perfect_for': genres,
                'vibe': 'Great'
            }
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return {
                'summary': overview[:150],
                'why_recommended': 'This movie matches your interests.',
                'perfect_for': genres,
                'vibe': 'Great'
            }
    
    def generate_comparison(self, movie1: str, movie2: str, overview1: str, overview2: str) -> Dict:
        """Generate AI-powered movie comparison."""
        if not self.is_configured():
            return {
                'comparison': f'{movie1} vs {movie2}: Two great movies with different styles.',
                'pick_if': f'Pick {movie1} for X, {movie2} for Y'
            }
        
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"""Compare these two movies in JSON format:
Movie 1: {movie1} - {overview1[:150]}
Movie 2: {movie2} - {overview2[:150]}

Provide JSON:
{{
  "comparison": "Brief comparison of themes and styles",
  "pick_if": "When to pick movie 1 vs movie 2"
}}

Respond ONLY with valid JSON."""

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=200,
                timeout=10
            )
            
            content = response['choices'][0]['message']['content'].strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            
            return json.loads(content.strip())
        except Exception as e:
            logger.error(f"Error in comparison: {e}")
            return {
                'comparison': 'Two great movies worth watching.',
                'pick_if': 'Both are excellent choices!'
            }

# Global instance
openai_helper = OpenAIHelper()
