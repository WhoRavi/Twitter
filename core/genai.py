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
        """Build tweet generation prompt with dynamic engagement styles"""
        previous_context = ""
        if previous_posts and len(previous_posts) > 0:
            recent_posts = previous_posts[-5:] if len(previous_posts) > 5 else previous_posts
            previous_context = f"\n\nPREVIOUS POSTS TO AVOID REPEATING:\n{recent_posts}"
        
        # Random engagement styles for variety
        styles = [
            "Share a mind-blowing recent breakthrough or development",
            "Post a controversial but thought-provoking take or prediction",
            "Highlight a fascinating real-world application or use case",
            "Share a surprising statistic or research finding",
            "Explain a complex concept in simple, relatable terms",
            "Point out an unexpected connection or implication",
            "Share a counterintuitive insight or common misconception debunked",
            "Highlight what's happening right NOW in the field",
            "Compare where we are vs where we're heading (past vs future)",
            "Share an exciting emerging trend or capability",
        ]
        
        selected_style = random.choice(styles)
        
        return f"""You are a tech influencer creating viral content about AI. Generate ONE tweet about {topic}.

STYLE FOR THIS TWEET: {selected_style}

GUIDELINES:
✓ Under {MAX_TWEET_LENGTH} characters
✓ Hook readers in the first line
✓ Use conversational, authentic voice (not corporate)
✓ Include specific details, numbers, or examples when relevant
✓ Make it shareable - give people something interesting to discuss
✓ Add 1-2 relevant hashtags naturally
✓ Vary your approach - questions, statements, hot takes, insights
✓ NO clichés like "asking for a friend" or "let that sink in"
✓ NO generic platitudes - be specific and interesting
✓ Focus on LATEST developments and current trends{previous_context}

Return ONLY the tweet text. No quotes, no labels, no explanations."""
    
    def _clean_and_truncate(self, text, source_url=None):
        """Clean and truncate text to Twitter limits, optionally adding source URL"""
        text = text.strip().strip('"').strip("'")
        
        # If we have a source URL, append it
        if source_url:
            # Reserve space for URL (Twitter shortens to ~23 chars) + newline
            max_text_length = MAX_TWEET_LENGTH - 25
            if len(text) > max_text_length:
                text = text[:max_text_length-3] + "..."
            text = f"{text}\n\n{source_url}"
        else:
            if len(text) > MAX_TWEET_LENGTH:
                text = text[:MAX_TWEET_LENGTH-3] + "..."
        
        return text
    
    def _extract_grounding_sources(self, response):
        """Extract source URLs from grounding metadata"""
        try:
            # Check if response has grounding metadata
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                    # Get grounding chunks (search results)
                    if hasattr(candidate.grounding_metadata, 'grounding_chunks'):
                        chunks = candidate.grounding_metadata.grounding_chunks
                        if chunks and len(chunks) > 0:
                            # Get the first (most relevant) source
                            chunk = chunks[0]
                            if hasattr(chunk, 'web') and chunk.web:
                                return chunk.web.uri
        except Exception as e:
            print(f"⚠️ Could not extract grounding source: {e}")
        
        return None
    
    def generate_tweet_with_search(self, topic=None, previous_posts=None, include_source=True):
        """
        Generate a tweet using web search for latest information
        
        Args:
            topic (str, optional): Specific topic to generate about. If None, random topic is selected.
            previous_posts (list, optional): List of previous posts to avoid duplicates
            include_source (bool, optional): Whether to include source URL in tweet. Default True.
            
        Returns:
            tuple: (topic, tweet_text, source_url)
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
        
        # Extract source URL from grounding metadata
        source_url = self._extract_grounding_sources(response) if include_source else None
        
        # Clean tweet text and optionally add source
        tweet_text = self._clean_and_truncate(response.text, source_url)
        
        return topic, tweet_text, source_url
    
    def generate_tweet_simple(self, topic=None, previous_posts=None):
        """
        Generate a tweet without web search (faster, but less current)
        
        Args:
            topic (str, optional): Specific topic to generate about. If None, random topic is selected.
            previous_posts (list, optional): List of previous posts to avoid duplicates
            
        Returns:
            tuple: (topic, tweet_text, source_url)
        """
        topic = topic or random.choice(TOPICS)
        prompt = self._build_tweet_prompt(topic, previous_posts)
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=TEMPERATURE)
        )
        
        return topic, self._clean_and_truncate(response.text), None
    
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
        - AI Research and Developments
        
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


def generate_tweet(use_web_search=True, topic=None, previous_posts=None, include_source=True):
    """
    Convenience function to generate a tweet
    
    Args:
        use_web_search (bool): Whether to use web search for latest information
        topic (str, optional): Specific topic to generate about
        previous_posts (list, optional): List of previous posts to avoid duplicates
        include_source (bool, optional): Whether to include source URL in tweet (only with web search)
        
    Returns:
        tuple: (topic, tweet_text, source_url)
    """
    generator = ContentGenerator()
    
    if use_web_search:
        return generator.generate_tweet_with_search(topic, previous_posts, include_source)
    else:
        return generator.generate_tweet_simple(topic, previous_posts)
