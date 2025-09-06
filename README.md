# 🤖 Twitter Bot - Complete Guide

A comprehensive Twitter bot built with Python that can post tweets, read timelines, reply to tweets, and perform automated interactions using Twitter API v2.

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Twitter API Setup](#-twitter-api-setup)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Bot Functions](#-bot-functions)
- [Security Best Practices](#-security-best-practices)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

## ✨ Features

### Core Functionality
- ✅ **Post Tweets** - Create and publish tweets with automatic length validation
- ✅ **Read Timeline** - Fetch and display tweets from your home timeline
- ✅ **Reply to Tweets** - Respond to specific tweets by ID
- ✅ **Search Tweets** - Find tweets using keywords, hashtags, or advanced queries
- ✅ **Like & Retweet** - Engage with other users' content
- ✅ **Get Own Tweets** - Retrieve your recent posts with metrics

### Advanced Features
- 🔄 **Automated Workflows** - Smart bot behavior with customizable actions
- 📊 **State Management** - Prevents duplicate actions and tracks activity
- ⏱️ **Rate Limiting** - Respects Twitter API limits automatically
- 📅 **Daily Post Limits** - Configurable daily posting limits to prevent spam
- 📝 **Comprehensive Logging** - Monitor all bot activities
- 🛡️ **Error Handling** - Robust exception handling throughout

## 🔧 Prerequisites

- Python 3.7 or higher
- Jupyter Notebook or JupyterLab
- Twitter Developer Account
- Twitter App with API keys

## 📦 Installation

1. **Clone or download this repository:**
   ```bash
   git clone <repository-url>
   cd twitter-bot
   ```

2. **Install required Python packages:**
   ```bash
   pip install tweepy python-dotenv requests
   ```

3. **Start Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

4. **Open `twitter.ipynb`** in Jupyter Notebook

## 🐦 Twitter API Setup

### Step 1: Create a Twitter Developer Account

1. Visit [developer.twitter.com](https://developer.twitter.com/)
2. Apply for a developer account
3. Wait for approval (usually takes 1-3 days)

### Step 2: Create a Twitter App

1. Go to the [Twitter Developer Portal](https://developer.twitter.com/portal)
2. Click "Create App"
3. Fill in the required information:
   - **App Name**: Choose a unique name
   - **Description**: Describe your bot's purpose
   - **Website**: Your website or GitHub repo URL
   - **Use Case**: Select appropriate use case

### Step 3: Generate API Keys

After creating your app, generate the following credentials:

- **API Key** (Consumer Key)
- **API Key Secret** (Consumer Secret) 
- **Bearer Token**
- **Access Token**
- **Access Token Secret**
- **Client ID** (for OAuth 2.0)
- **Client Secret** (for OAuth 2.0)

### Step 4: Set App Permissions

Ensure your app has the following permissions:
- ✅ **Read** - To read tweets and timelines
- ✅ **Write** - To post tweets and replies
- ✅ **Direct Messages** (optional) - If you plan to handle DMs

## 🚀 Quick Start

### 1. Configure Credentials

Open `twitter.ipynb` and update the credentials in cell 3:

```python
# Twitter API Credentials
API_KEY = "your_api_key_here"
API_KEY_SECRET = "your_api_key_secret_here" 
BEARER_TOKEN = "your_bearer_token_here"
ACCESS_TOKEN = "your_access_token_here"
ACCESS_TOKEN_SECRET = "your_access_token_secret_here"
CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"
```

### 2. Run Initial Setup

Execute the first 4 cells in order:
1. **Cell 1**: Install dependencies
2. **Cell 2**: Import libraries
3. **Cell 3**: Set credentials
4. **Cell 4**: Initialize bot and verify authentication

### 3. Test Basic Functions

Try these basic operations:

```python
# Post a tweet
post_tweet("Hello Twitter! 🤖 My bot is now active!")

# Read your timeline
tweets = read_home_timeline(5)

# Search for tweets
results = search_tweets("#Python", 3)

# Reply to a tweet
reply_to_tweet(tweet_id, "Thanks for sharing this!")
```

## 📖 Usage Guide

### Running the Notebook

1. **Execute cells sequentially** - Start from the top and run each cell
2. **Wait for completion** - Some cells may take time due to API calls
3. **Check outputs** - Each cell will show results or confirmations
4. **Monitor logs** - Watch for success/error messages

### Basic Workflow

```python
# 1. Initialize bot (run setup cells first)
bot = TwitterBot()

# 2. Verify authentication
bot.verify_credentials()

# 3. Use bot functions
tweet_id = post_tweet("My first automated tweet!")
timeline = read_home_timeline(10)
search_results = search_tweets("#AI", 5)
```

### Advanced Usage

```python
# Automated workflow
automated_bot_workflow()

# State management
bot_state = BotState()
if not bot_state.is_tweet_processed(tweet_id):
    like_tweet(tweet_id)
    bot_state.mark_tweet_processed(tweet_id)

# Safe posting with limits
safe_post_tweet("Daily update!", max_daily_posts=5)
```

## 🔧 Bot Functions

### Core Functions

| Function | Description | Example |
|----------|-------------|---------|
| `post_tweet(text)` | Post a new tweet | `post_tweet("Hello World!")` |
| `read_home_timeline(count)` | Read tweets from timeline | `read_home_timeline(10)` |
| `search_tweets(query, count)` | Search for tweets | `search_tweets("#Python", 5)` |
| `reply_to_tweet(tweet_id, text)` | Reply to a tweet | `reply_to_tweet("123", "Great post!")` |
| `like_tweet(tweet_id)` | Like a tweet | `like_tweet("123456789")` |
| `retweet(tweet_id)` | Retweet a tweet | `retweet("123456789")` |
| `get_my_tweets(count)` | Get your recent tweets | `get_my_tweets(5)` |

### Advanced Functions

| Function | Description | Example |
|----------|-------------|---------|
| `safe_post_tweet(text, max_daily)` | Post with daily limits | `safe_post_tweet("Update", 10)` |
| `automated_bot_workflow()` | Run automated actions | `automated_bot_workflow()` |
| `bot_state.is_tweet_processed(id)` | Check if tweet was processed | `bot_state.is_tweet_processed("123")` |
| `bot_state.mark_tweet_processed(id)` | Mark tweet as processed | `bot_state.mark_tweet_processed("123")` |

### Search Query Examples

```python
# Basic hashtag search
search_tweets("#Python", 10)

# Exclude retweets
search_tweets("#MachineLearning -is:retweet", 5)

# Search with multiple terms
search_tweets("python OR javascript", 10)

# Search from specific user
search_tweets("from:username", 5)

# Search with engagement filters
search_tweets("#AI min_faves:10", 5)
```

## 🔒 Security Best Practices

### 1. Environment Variables (Recommended)

Create a `.env` file:
```bash
# .env file
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_SECRET=your_access_secret_here
TWITTER_CLIENT_ID=your_client_id_here
TWITTER_CLIENT_SECRET=your_client_secret_here
```

Update your notebook to use environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('TWITTER_API_KEY')
API_KEY_SECRET = os.getenv('TWITTER_API_SECRET')
# ... etc
```

### 2. Git Security

Add to `.gitignore`:
```
.env
bot_state.json
*.log
__pycache__/
.ipynb_checkpoints/
```

### 3. Rate Limiting

- Bot automatically handles rate limits
- Daily post limits prevent spam (default: 10 posts/day)
- Respectful delays between API calls

### 4. Monitoring

- All actions are logged
- Bot state is saved to track activity
- Regular monitoring recommended

## ⚙️ Configuration

### Bot State Configuration

The bot saves its state in `bot_state.json`:
```json
{
  "processed_tweets": ["123456789", "987654321"],
  "last_timeline_check": "2025-09-06T10:30:00",
  "daily_post_count": 3,
  "last_post_date": "2025-09-06"
}
```

### Customizable Settings

```python
# Daily posting limits
MAX_DAILY_POSTS = 10

# Search result limits
DEFAULT_SEARCH_COUNT = 10

# Timeline fetch count
DEFAULT_TIMELINE_COUNT = 20

# Automated workflow settings
WORKFLOW_QUERIES = [
    "#Python programming -is:retweet",
    "#MachineLearning -is:retweet",
    "#DataScience -is:retweet"
]
```

## 🐛 Troubleshooting

### Common Issues

#### Authentication Errors
```
Error: 401 Unauthorized
```
**Solution**: Check your API credentials and app permissions

#### Rate Limit Exceeded
```
Error: 429 Too Many Requests
```
**Solution**: Wait for rate limit reset (automatically handled by tweepy)

#### Tweet Too Long
```
Error: Tweet text is too long
```
**Solution**: Bot automatically truncates tweets over 280 characters

#### Duplicate Tweet
```
Error: Status is a duplicate
```
**Solution**: Use unique content or add timestamp

### Debug Mode

Enable detailed logging:
```python
import logging
logging.getLogger("tweepy").setLevel(logging.DEBUG)
```

### API Status Check

Check Twitter API status: [api.twitterstat.us](https://api.twitterstat.us/)

## 📊 Monitoring Your Bot

### View Bot Activity
```python
# Check daily statistics
print(f"Posts today: {bot_state.state['daily_post_count']}")
print(f"Processed tweets: {len(bot_state.state['processed_tweets'])}")

# View recent activity
get_my_tweets(10)
```

### Log Analysis
Check log files for:
- Successful operations
- Error patterns
- Rate limit hits
- Authentication issues

## 🔄 Automated Workflows

### Example Workflow

```python
def custom_workflow():
    # Search for relevant content
    tweets = search_tweets("#YourTopic -is:retweet", 5)
    
    for tweet in tweets:
        if not bot_state.is_tweet_processed(tweet['id']):
            # Like the tweet
            like_tweet(tweet['id'])
            
            # Maybe reply (30% chance)
            if random.random() < 0.3:
                reply_to_tweet(tweet['id'], "Interesting! 👍")
            
            # Mark as processed
            bot_state.mark_tweet_processed(tweet['id'])
            
            # Respectful delay
            time.sleep(60)  # 1 minute between actions
```

### Scheduling

For automated scheduling, consider:
- **Cron jobs** (Linux/Mac)
- **Task Scheduler** (Windows)
- **Cloud functions** (AWS Lambda, Google Cloud Functions)
- **GitHub Actions** (for simple automation)

## 📈 Best Practices

### Content Guidelines
- ✅ Post valuable, relevant content
- ✅ Engage authentically with users
- ✅ Respect Twitter's terms of service
- ❌ Don't spam or post repetitive content
- ❌ Don't engage in harassment or abuse

### Technical Guidelines
- ✅ Monitor bot activity regularly
- ✅ Implement proper error handling
- ✅ Use rate limiting and delays
- ✅ Keep credentials secure
- ❌ Don't ignore API rate limits
- ❌ Don't hardcode sensitive data

### Engagement Guidelines
- ✅ Reply thoughtfully to mentions
- ✅ Share interesting content from others
- ✅ Use relevant hashtags appropriately
- ❌ Don't auto-reply to everything
- ❌ Don't follow/unfollow aggressively

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review Twitter API documentation
3. Check Twitter API status
4. Create an issue on GitHub

## 🔗 Useful Links

- [Twitter Developer Documentation](https://developer.twitter.com/en/docs)
- [Tweepy Documentation](https://docs.tweepy.org/)
- [Twitter API v2 Reference](https://developer.twitter.com/en/docs/api-reference-index)
- [Twitter Developer Community](https://twittercommunity.com/)

---

**Happy Tweeting! 🐦🤖**

*Remember to use your bot responsibly and follow Twitter's terms of service and automation rules.*
