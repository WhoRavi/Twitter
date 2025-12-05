"""
Twitter Bot - Main Application
Generates and posts AI-related content to Twitter/X using Gemini API
"""
from core.config import validate_credentials
from core.genai import generate_tweet
from core.posting import post_tweet, load_post_history, save_post


def main():
    """Main application entry point"""
    print("🚀 Starting Twitter Bot...")
    print("=" * 70)
    
    # Validate credentials
    try:
        validate_credentials()
        print("✅ All credentials validated successfully!")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return
    
    print("=" * 70)
    
    # Load previous posts to avoid duplicates
    previous_posts = load_post_history()
    print(f"📚 Loaded {len(previous_posts)} previous posts from history")
    
    print("=" * 70)
    
    # Generate tweet content using web search
    print("🔍 Generating tweet with latest information...")
    try:
        topic, tweet_text, source_url = generate_tweet(
            use_web_search=True,
            previous_posts=previous_posts,
            include_source=True  # Include source URL in tweet
        )
        
        print(f"\n📝 Topic: {topic}")
        print(f"📄 Generated tweet:\n{tweet_text}")
        if source_url:
            print(f"🔗 Source: {source_url}")
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"❌ Error generating tweet: {e}")
        return
    
    # Check if already posted
    if tweet_text in previous_posts:
        print("⚠️ This tweet was already posted before!")
        return
    
    # Post the tweet
    print("📤 Posting tweet to X...")
    result = post_tweet(tweet_text)
    
    if result:
        save_post(topic, tweet_text)
        print(f"💾 Saved to post_history.csv")
        print("=" * 70)
        print("✅ Tweet posted successfully!")
        print(f"🔗 Tweet ID: {result['id']}")
    else:
        print("=" * 70)
        print("❌ Failed to post tweet")
    
    print("=" * 70)
    print("🏁 Bot execution completed!")


if __name__ == "__main__":
    main()
