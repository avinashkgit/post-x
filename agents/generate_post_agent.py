import random
from google import genai

from .news_agent import NewsAgent
from .meme_agent import MemeAgent
from .quote_agent import QuoteAgent
from .tech_agent import TechAgent
from .lifestyle_agent import LifestyleAgent
from .entertainment_agent import EntertainmentAgent
from .food_agent import FoodAgent
from .sports_agent import SportsAgent
from .opinion_agent import OpinionAgent
from .question_agent import QuestionAgent
from .list_agent import ListAgent

class GeneratePostAgent:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.agents = [
            NewsAgent(self.client),
            MemeAgent(self.client),
            QuoteAgent(self.client),
            TechAgent(self.client),
            LifestyleAgent(self.client),
            EntertainmentAgent(self.client),
            FoodAgent(self.client),
            SportsAgent(self.client),
            OpinionAgent(self.client),
            QuestionAgent(self.client),
            ListAgent(self.client),
        ]

    def generate_post(self):
        agent = random.choice(self.agents)
        post = agent.generate_post()
        if len(post) > 280:
            post = post[:277] + "..."
        return post
