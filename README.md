# Twitter AI Bot 🤖

An automated Twitter/X bot that generates and posts engaging AI and tech-related content using Google's Gemini API with integrated web search capabilities.

## 📋 Overview

This bot automatically:
1. Generates engaging tweets about AI, ML, and tech topics
2. Uses Google's Grounding Search to find latest information
3. Avoids posting duplicate content
4. Posts to Twitter/X automatically
5. Tracks all posted content in CSV format

## 🏗️ Architecture

```
Twitter/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── run_main.bat           # Windows batch script for automation
├── core/
│   ├── config.py          # Configuration and credentials
│   ├── genai.py           # Content generation using Gemini
│   ├── posting.py         # Twitter/X posting functionality
│   └── web_search.py      # Web search utilities
└── data/
    └── post_history.csv   # Track posted tweets
```

## 🔄 How It Works

### 1. **Initialization & Validation** (`main.py`)
- Validates all required API credentials (Twitter & Gemini)
- Loads post history from CSV to avoid duplicates

### 2. **Content Generation** (`core/genai.py`)
The `ContentGenerator` class offers two modes:

#### **Web Search Mode (Recommended)**
```python
generate_tweet_with_search(topic=None, previous_posts=None)
```
- Uses Google's Grounding Search to find latest information
- Generates tweets based on current trends and news
- More relevant and timely content

#### **Simple Mode (Faster)**
```python
generate_tweet_simple(topic=None, previous_posts=None)
```
- Generates content without web search
- Faster but may be less current
- Uses Gemini's knowledge cutoff

**Tweet Generation Process:**
1. Selects a random topic from predefined list (or uses specified topic)
2. Builds a prompt with requirements:
   - Max 280 characters
   - Engaging question, code snippet, or interesting fact
   - 1-2 relevant hashtags
   - Educational but entertaining
3. Uses Gemini API to generate content
4. Cleans and truncates to Twitter limits

### 3. **Duplicate Prevention**
- Checks generated tweet against `previous_posts` list
- Prevents posting identical content
- Maintains post history in CSV file

### 4. **Posting to Twitter** (`core/posting.py`)
```python
post_tweet(text)
```
- Uses Tweepy library with Twitter API v2
- Authenticates using OAuth 1.0a
- Posts tweet and returns tweet ID
- Handles errors gracefully

### 5. **History Tracking**
- Saves each post to `data/post_history.csv`
- Records: timestamp, topic, and tweet text
- Used for duplicate detection in future runs

## 🔑 Configuration

### Required Environment Variables (`.env`)

```env
# Twitter API Credentials
BEARER_TOKEN=your_bearer_token
API_KEY=your_api_key
API_SECRET=your_api_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret

# Gemini API
GEMINI_API_KEY=your_gemini_api_key
```

### Configurable Settings (`core/config.py`)

```python
# Topics for tweet generation
TOPICS = [
    'Artificial Intelligence',
    'Generative AI',
    'Machine Learning',
    'Python Programming',
    'Data Science',
    'Deep Learning',
    'Natural Language Processing',
    'Computer Vision',
    'Neural Networks',
    'Large Language Models',
    # ... more topics
]

# Model configurations
GEMINI_TEXT_MODEL = "gemini-2.5-flash"
TEMPERATURE = 0.7
MAX_TWEET_LENGTH = 280
```

## 🚀 Installation

### 1. Clone the repository
```bash
cd c:\Users\ravid\Desktop\Codes\Projects\Twitter
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory with your API credentials:
```env
BEARER_TOKEN=...
API_KEY=...
API_SECRET=...
ACCESS_TOKEN=...
ACCESS_TOKEN_SECRET=...
GEMINI_API_KEY=...
```

### 4. Create data directory
```bash
mkdir data
```

## 💻 Usage

### Manual Execution
```bash
python main.py
```

### Automated Execution (Windows)
```bash
run_main.bat
```

This batch file can be scheduled using Windows Task Scheduler for automatic posting.

### Example Output
```
🚀 Starting Twitter Bot...
======================================================================
✅ All credentials validated successfully!
======================================================================
📚 Loaded 42 previous posts from history
======================================================================
🔍 Generating tweet with latest information...

📝 Topic: Artificial Intelligence
📄 Generated tweet:
What if AI could explain its reasoning in plain language? 🤔

New research shows models with "chain-of-thought" prompting improve accuracy by 40%!

#AI #MachineLearning

======================================================================
📤 Posting tweet to X...
✅ Tweet posted! ID: 1234567890
💾 Saved to post_history.csv
======================================================================
✅ Tweet posted successfully!
🔗 Tweet ID: 1234567890
======================================================================
🏁 Bot execution completed!
```

## 📦 Dependencies

- **tweepy** (>=4.14.0) - Twitter API client
- **google-genai** (>=1.0.0) - Google Gemini API
- **python-dotenv** (>=1.0.0) - Environment variable management
- **pandas** (>=2.0.0) - Data processing for CSV

## 🔍 Key Features

### 1. **Smart Content Generation**
- Uses Google Grounding Search for latest information
- Generates diverse content types:
  - Thought-provoking questions
  - Code snippets and challenges
  - Interesting facts and recent developments
  - Educational content with entertainment value

### 2. **Duplicate Detection**
- Maintains history of all posted tweets
- Compares new content against previous posts
- Prevents accidental reposts

### 3. **Error Handling**
- Validates credentials before execution
- Graceful error handling for API failures
- Detailed logging for debugging

### 4. **Flexible Configuration**
- Easy topic customization
- Adjustable temperature for creativity
- Multiple model support (Gemini, OpenAI)

## 🛠️ Advanced Usage

### Custom Topic Generation
```python
from core.genai import generate_tweet

topic, tweet = generate_tweet(
    use_web_search=True,
    topic="Quantum Computing",
    previous_posts=[]
)
```

### Tech Article Generation
```python
from core.genai import ContentGenerator

generator = ContentGenerator()
article = generator.generate_tech_article()
```

### Web Search
```python
from core.web_search import WebSearcher

searcher = WebSearcher()
result = searcher.search_tech_news()
```

## 📊 Data Storage

Post history is stored in `data/post_history.csv`:

| timestamp | topic | text |
|-----------|-------|------|
| 2025-11-26T10:30:00 | Artificial Intelligence | What if AI could... |
| 2025-11-26T11:45:00 | Machine Learning | Here's a cool Python one-liner... |

## 🔐 Security Notes

- Never commit your `.env` file
- Keep API credentials secure
- Use environment variables for sensitive data
- Regularly rotate access tokens

## 🤝 Contributing

To add new topics:
1. Edit `TOPICS` list in `core/config.py`
2. Keep topics AI/tech-related for best results

To modify tweet style:
1. Edit prompt in `_build_tweet_prompt()` in `core/genai.py`
2. Adjust `TEMPERATURE` for creativity level

## 📝 License

This project is for personal use. Ensure compliance with Twitter's automation rules and API terms of service.

## ⚠️ Disclaimer

- Use responsibly and follow Twitter's automation rules
- Avoid excessive posting (rate limits)
- Ensure generated content aligns with Twitter's policies
- Monitor bot activity regularly

## 🐛 Troubleshooting

### "Configuration error" message
- Check `.env` file exists and has all required variables
- Verify API credentials are correct

### "Failed to post tweet"
- Check Twitter API rate limits
- Verify OAuth credentials are valid
- Ensure tweet length is under 280 characters

### "Error generating tweet"
- Verify Gemini API key is valid
- Check internet connection for web search
- Review API quota limits

## 📞 Support

For issues or questions, review the error messages in the console output. Most issues are related to:
- Missing or invalid API credentials
- Network connectivity
- API rate limits
- Duplicate content detection

---

**Built with ❤️ using Google Gemini and Tweepy**
