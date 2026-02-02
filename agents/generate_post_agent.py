import random
from google import genai
from .base_agent import Agent


class GeneratePostAgent(Agent):
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        super().__init__(self.client)
        self.prompts = [
            # News
            "Create a shocking, clickbait news post about recent events that will make people stop scrolling. Make it dramatic, under 280 characters, and end with a question to spark comments. Do not include any hashtags.",
            # Memes
            "Generate a hilarious, relatable meme-style post or joke that captures a universal experience. Keep it short and punchy under 280 characters, perfect for viral sharing. Do not include any hashtags.",
            # Quotes
            "Craft an inspiring, shareable quote about life, success, or motivation that resonates deeply. Make it profound yet accessible, under 280 characters, encouraging followers to reflect and reply. Do not include any hashtags.",
            # Tech
            "Write an exciting post about cutting-edge technology, gadgets, or digital trends that will blow people's minds. Make it futuristic and intriguing, under 280 characters, asking readers what they think. Do not include any hashtags.",
            # Lifestyle
            "Create an engaging lifestyle post about health, fitness, relationships, or self-care with practical advice. Make it relatable and helpful, under 280 characters, ending with a question to encourage sharing personal experiences. Do not include any hashtags.",
            # Entertainment
            "Generate a buzzworthy post about movies, TV shows, celebrities, or pop culture that's spoiler-light but intriguing. Make it controversial or exciting, under 280 characters, designed to start discussions. Do not include any hashtags.",
            # Food
            "Write a mouth-watering food post about recipes, cooking hacks, or dining experiences that makes readers hungry. Make it descriptive and tempting, under 280 characters, asking followers to share their favorite dishes. Do not include any hashtags.",
            # Sports
            "Create an intense sports post about games, predictions, or athlete drama that gets fans fired up. Make it dramatic and opinionated, under 280 characters, challenging readers to debate. Do not include any hashtags.",
            # Opinions
            "Share a bold, controversial opinion on current trends, culture, or society that's thought-provoking but respectful. Make it provocative enough to generate replies, under 280 characters, encouraging civil debate. Do not include any hashtags.",
            # Questions
            "Pose a deep, thought-provoking question about life, relationships, or current events that will make people pause and respond. Make it relatable and engaging, under 280 characters, perfect for sparking meaningful conversations. Do not include any hashtags.",
            # Lists
            "Create a fascinating 'Top 5' or ranked list about interesting facts, tips, or surprising rankings that piques curiosity. Make it informative and shareable, under 280 characters, with a twist that encourages discussion. Do not include any hashtags.",
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
