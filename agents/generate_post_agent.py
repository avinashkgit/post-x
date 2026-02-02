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
                "Write a post like a real person reacting to a surprising or unsettling news moment. "
                "Sound curious, concerned, or slightly shocked — not like a headline. "
                "Keep it casual, under 280 characters. End with a natural question. "
                "No hashtags, emojis, or formal news tone."
            ),
            # Memes
            (
                "Write something funny and relatable that feels like a random thought someone posted. "
                "Dry humor, self-awareness, or mild sarcasm is good. "
                "Short, imperfect, under 280 characters. "
                "No hashtags, emojis, or explaining the joke."
            ),
            # Quotes
            (
                "Write a short thought about life or growth that sounds like something someone realized late at night. "
                "Not poetic. Not inspirational. Just honest. "
                "Under 280 characters. No hashtags or emojis."
            ),
            # Tech
            (
                "Write a casual thought about tech, AI, or gadgets like someone thinking out loud. "
                "Curious, slightly unsure, maybe impressed or skeptical. "
                "Under 280 characters. End with a natural question. "
                "No buzzwords, hashtags, or emojis."
            ),
            # Lifestyle
            (
                "Write a relatable post about habits, health, relationships, or mental state. "
                "Sound human, a bit vulnerable or self-aware. "
                "Under 280 characters. End with a question that feels genuine. "
                "No hashtags or emojis."
            ),
            # Entertainment
            (
                "Write a casual opinion about a movie, show, celebrity, or pop culture moment. "
                "It should sound like a real take, not a review. "
                "Under 280 characters. End with a question. "
                "No hashtags or emojis."
            ),
            # Food
            (
                "Write about food like someone who’s either craving it or slightly disappointed by it. "
                "Casual, sensory, imperfect. "
                "Under 280 characters. End with a natural question. "
                "No hashtags or emojis."
            ),
            # Sports
            (
                "Write a sports take that sounds emotional or impulsive. "
                "A little bias is fine. Overconfidence is fine. "
                "Under 280 characters. End with a question that invites debate. "
                "No hashtags or emojis."
            ),
            # Opinions
            (
                "Write an opinion that sounds like a thought someone hesitated before posting. "
                "Respectful, but honest. Not trying to go viral. "
                "Under 280 characters. End with a question. "
                "No hashtags or emojis."
            ),
            # Questions
            (
                "Ask a question that feels personal and real, not philosophical or motivational. "
                "Something people might actually answer. "
                "Under 280 characters. No hashtags or emojis."
            ),
            # Lists
            (
                "Write a short list like someone casually sharing thoughts, not teaching. "
                "Loose structure is fine. Slightly messy is good. "
                "Under 280 characters. End with a question. "
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
