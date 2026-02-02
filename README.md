# X Post Bot

This Python application uses AI agents to generate various types of highly engaging posts (news, memes, quotes, tech, lifestyle, entertainment, food, sports, opinions, questions, lists) using Google's Gemini AI and posts them on X (formerly Twitter) every 2 hours using GitHub Actions.

## Setup

1. **Clone or download this repository.**

2. **Set up API Keys:**

   - **Gemini API Key:** Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **X (Twitter) API Keys:** Get from [Twitter Developer Portal](https://developer.twitter.com/)
     - You need: Bearer Token, Consumer Key, Consumer Secret, Access Token, Access Token Secret
     - Ensure your app has write permissions.

3. **GitHub Secrets:** In your GitHub repository settings, add the following secrets:
   - `GEMINI_API_KEY`
   - `TWITTER_BEARER_TOKEN`
   - `TWITTER_CONSUMER_KEY`
   - `TWITTER_CONSUMER_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET`

4. **Push to GitHub:** The workflow will run automatically every 2 hours, or you can trigger it manually.

## Local Testing

To test locally:

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables with your API keys.
3. Run: `python main.py`

## Notes

- Posts are generated to be under 280 characters.
- The bot randomly selects from different agent types: News (current events), Memes (funny content), Quotes (inspirational), Tech (technology trends), Lifestyle (health/fitness), Entertainment (movies/TV), Food (recipes/tips), Sports (news/predictions), Opinions (controversial takes), Questions (discussion starters), and Lists (top rankings).