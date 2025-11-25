"""
Web search functionality using Google Grounding Search via Gemini API
"""
from google import genai
from google.genai import types
from .config import GEMINI_API_KEY, GEMINI_TEXT_MODEL, TEMPERATURE


class WebSearcher:
    """Handle web search operations using Google Grounding Search"""
    
    def __init__(self):
        """Initialize the Gemini client"""
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = GEMINI_TEXT_MODEL
    
    def search_and_generate(self, query, stream=True):
        """
        Search the web and generate content based on the query
        
        Args:
            query (str): The search query and content generation prompt
            stream (bool): Whether to stream the response
            
        Returns:
            str: Generated content based on search results
        """
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=query),
                ],
            ),
        ]
        
        tools = [
            types.Tool(google_search=types.GoogleSearch()),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            tools=tools,
            temperature=TEMPERATURE,
        )
        
        if stream:
            return self._stream_response(contents, generate_content_config)
        else:
            return self._get_response(contents, generate_content_config)
    
    def _stream_response(self, contents, config):
        """Stream the response from Gemini"""
        full_response = ""
        
        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=config,
        ):
            if chunk.text:
                full_response += chunk.text
        
        return full_response
    
    def _get_response(self, contents, config):
        """Get the complete response from Gemini"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )
        return response.text
    
    def search_tech_news(self):
        """
        Search for latest tech, AI, gadgets and breaking news
        
        Returns:
            str: Generated article based on latest tech news
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
        
        return self.search_and_generate(query, stream=False)


def search_latest_tech_news():
    """
    Convenience function to search for latest tech news
    
    Returns:
        str: Generated article about latest tech news
    """
    searcher = WebSearcher()
    return searcher.search_tech_news()
