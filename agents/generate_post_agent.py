import random
from google import genai
from .base_agent import Agent


class GeneratePostAgent(Agent):
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        super().__init__(self.client)
        self.prompts = [
            # News
            (
                "Write a shocking, scroll-stopping news-style post inspired by recent real-world events. "
                "Use dramatic language, create urgency, and open with a bold claim or unexpected twist. "
                "Keep it under 280 characters. End with a compelling question that invites opinions. "
                "Do not include hashtags, emojis, sources, or disclaimers."
            ),
            # Memes
            (
                "Create a short, meme-style post that captures a painfully relatable everyday experience. "
                "Use humor, irony, or self-awareness. Make it punchy, conversational, and instantly shareable. "
                "Under 280 characters. No hashtags, emojis, or explanations."
            ),
            # Quotes
            (
                "Write an original, powerful quote about life, ambition, failure, or growth. "
                "It should feel timeless, emotionally resonant, and quotable. "
                "Under 280 characters. Avoid clichés. Do not include hashtags or emojis."
            ),
            # Tech
            (
                "Create an intriguing post about emerging technology, AI, gadgets, or digital trends. "
                "Spark curiosity by hinting at how it could change everyday life or challenge assumptions. "
                "Under 280 characters. End with a question inviting opinions. No hashtags or emojis."
            ),
            # Lifestyle
            (
                "Write a relatable lifestyle post about health, habits, relationships, or mental well-being. "
                "Offer a practical insight or hard truth that feels personal and real. "
                "Under 280 characters. End with a question encouraging people to share experiences. "
                "No hashtags or emojis."
            ),
            # Entertainment
            (
                "Generate a buzzworthy post about movies, TV shows, celebrities, or pop culture. "
                "Keep it spoiler-free but provocative or controversial enough to spark debate. "
                "Under 280 characters. End with a question. No hashtags or emojis."
            ),
            # Food
            (
                "Write a vivid, mouth-watering food post describing a dish, cooking hack, or dining experience. "
                "Use sensory language (taste, smell, texture). "
                "Under 280 characters. End with a question asking readers about their favorites. "
                "No hashtags or emojis."
            ),
            # Sports
            (
                "Create a high-energy sports post about a match, athlete, rivalry, or prediction. "
                "Be bold, emotional, and slightly opinionated to trigger debate. "
                "Under 280 characters. End with a challenge or question. No hashtags or emojis."
            ),
            # Opinions
            (
                "Share a bold, thought-provoking opinion about modern culture, trends, or society. "
                "Keep it respectful but polarizing enough to invite disagreement. "
                "Under 280 characters. End with a question encouraging civil discussion. "
                "No hashtags or emojis."
            ),
            # Questions
            (
                "Ask a deep, emotionally resonant question about life, relationships, success, or current events. "
                "Make it universal, reflective, and conversation-starting. "
                "Under 280 characters. Do not include hashtags or emojis."
            ),
            # Lists
            (
                "Create a compact 'Top 3' or 'Top 5' list of surprising facts, tips, or insights. "
                "Use curiosity-driven wording and an unexpected angle. "
                "Under 280 characters. End with a question inviting reactions. "
                "No hashtags or emojis."
            ),
        ]

    def generate_post(self):
        prompt = random.choice(self.prompts)
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
        post = response.text.strip()
        if len(post) > 280:
            post = post[:277] + "..."
        return post
