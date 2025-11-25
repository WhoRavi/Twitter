"""
Content generation for X (Twitter) posts using Gemini API with integrated web search
"""
import random
from google import genai
from google.genai import types
from .config import (
    GEMINI_API_KEY, 
    GEMINI_TEXT_MODEL, 
    TOPICS, 
    TEMPERATURE,
    MAX_TWEET_LENGTH
)


class ContentGenerator:
    """Generate content for X posts using Gemini API with integrated web search"""
    
    def __init__(self):
        """Initialize the Gemini client"""
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = GEMINI_TEXT_MODEL
    
    def _build_tweet_prompt(self, topic, previous_posts):
        """Build tweet generation prompt"""
        previous_context = ""
        if previous_posts and len(previous_posts) > 0:
            recent_posts = previous_posts[-5:] if len(previous_posts) > 5 else previous_posts
            previous_context = f"\n- Don't repeat these previous posts: {recent_posts}"
        
        return f"""Generate a single engaging tweet about {topic}.

Requirements:
- Keep it under {MAX_TWEET_LENGTH} characters
- Ask a thought-provoking or fun question related to {topic}
- OR share a coding snippet/challenge (like "n % 2 ? 'Odd' : 'Even'", lambda functions, one-liners, etc.)
- OR share an interesting fact or recent development
- Add humor and wit when appropriate
- Use relevant hashtags (1-2 max)
- Make it educational but entertaining{previous_context}

Just return the tweet text, nothing else. No quotes, no explanations."""
    
    def _clean_and_truncate(self, text):
        """Clean and truncate text to Twitter limits"""
        text = text.strip().strip('"').strip("'")
        if len(text) > MAX_TWEET_LENGTH:
            text = text[:MAX_TWEET_LENGTH-3] + "..."
        return text
    
    def generate_tweet_with_search(self, topic=None, previous_posts=None):
        """
        Generate a tweet using web search for latest information
        
        Args:
            topic (str, optional): Specific topic to generate about. If None, random topic is selected.
            previous_posts (list, optional): List of previous posts to avoid duplicates
            
        Returns:
            tuple: (topic, tweet_text)
        """
        topic = topic or random.choice(TOPICS)
        prompt = f"Search for the latest information and trending topics about {topic}.\n\n" + \
                 self._build_tweet_prompt(topic, previous_posts)
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])],
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=TEMPERATURE,
            )
        )
        
        return topic, self._clean_and_truncate(response.text)
    
    def generate_tweet_simple(self, topic=None, previous_posts=None):
        """
        Generate a tweet without web search (faster, but less current)
        
        Args:
            topic (str, optional): Specific topic to generate about. If None, random topic is selected.
            previous_posts (list, optional): List of previous posts to avoid duplicates
            
        Returns:
            tuple: (topic, tweet_text)
        """
        topic = topic or random.choice(TOPICS)
        prompt = self._build_tweet_prompt(topic, previous_posts)
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=TEMPERATURE)
        )
        
        return topic, self._clean_and_truncate(response.text)
    
    def generate_tech_article(self):
        """
        Generate a tech article based on latest news using grounding search
        
        Returns:
            str: Generated article about latest tech news
        """
        query = """Search for the latest breaking news and trending topics in:
        - Technology
        - Artificial Intelligence
        - Gadgets and Consumer Electronics
        - Tech Industry News
        
        Based on the most recent and relevant information found, write an engaging article suitable for posting on X (Twitter). 
        The article should:
        - Be informative and attention-grabbing
        - Highlight the most important/interesting development
        - Be formatted for easy reading on social media
        - Include key facts and details
        - Be between 200-300 words
        - Have a compelling hook at the start
        """
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=[types.Content(role="user", parts=[types.Part.from_text(text=query)])],
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                temperature=TEMPERATURE,
            )
        )
        
        return response.text


def generate_tweet(use_web_search=True, topic=None, previous_posts=None):
    """
    Convenience function to generate a tweet
    
    Args:
        use_web_search (bool): Whether to use web search for latest information
        topic (str, optional): Specific topic to generate about
        previous_posts (list, optional): List of previous posts to avoid duplicates
        
    Returns:
        tuple: (topic, tweet_text)
    """
    generator = ContentGenerator()
    
    if use_web_search:
        return generator.generate_tweet_with_search(topic, previous_posts)
    else:
        return generator.generate_tweet_simple(topic, previous_posts)
