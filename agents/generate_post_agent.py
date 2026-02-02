import random
from google import genai

from .unified_agent import UnifiedContentAgent

class GeneratePostAgent:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.agent = UnifiedContentAgent(self.client)

    def generate_post(self):
        post = self.agent.generate_post()
        if len(post) > 280:
            post = post[:277] + "..."
        return post
