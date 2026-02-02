import random
import google.generativeai as genai

class Agent:
    def __init__(self, model):
        self.model = model

    def generate_post(self):
        raise NotImplementedError

class NewsAgent(Agent):
    def generate_post(self):
        prompt = "Generate a clickbait engaging social media post about recent news events. Make it short, under 280 characters, and attention-grabbing."
        response = self.model.generate_content(prompt)
        return response.text.strip()

class MemeAgent(Agent):
    def generate_post(self):
        prompt = "Generate a funny, meme-style social media post or joke. Keep it short, engaging, and under 280 characters."
        response = self.model.generate_content(prompt)
        return response.text.strip()

class QuoteAgent(Agent):
    def generate_post(self):
        prompt = "Generate an inspirational quote or motivational post. Make it engaging and under 280 characters."
        response = self.model.generate_content(prompt)
        return response.text.strip()

class TechAgent(Agent):
    def generate_post(self):
        prompt = "Generate a clickbait post about technology trends or gadgets. Make it engaging and under 280 characters."
        response = self.model.generate_content(prompt)
        return response.text.strip()

class LifestyleAgent(Agent):
    def generate_post(self):
        prompt = "Generate an engaging social media post about lifestyle topics like health, fitness, relationships, or self-care. Make it clickbait, under 280 characters, and encourage engagement with questions or calls to action. Include emojis and hashtags."
        response = self.model.generate_content(prompt)
        return response.text.strip()

class EntertainmentAgent(Agent):
    def generate_post(self):
        prompt = "Create a buzzworthy post about movies, TV shows, celebrities, or pop culture. Make it controversial or exciting, under 280 characters, to spark discussions and shares. Use emojis and trending hashtags."
        response = self.model.generate_content(prompt)
        return response.text.strip()

class FoodAgent(Agent):
    def generate_post(self):
        prompt = "Generate a mouth-watering post about food, recipes, cooking tips, or dining experiences. Make it visually appealing in text form, under 280 characters, and ask followers to share their favorites. Include food emojis."
        response = self.model.generate_content(prompt)
        return response.text.strip()

class SportsAgent(Agent):
    def generate_post(self):
        prompt = "Create an exciting post about sports news, game predictions, or athlete highlights. Make it dramatic and engaging, under 280 characters, to get fans talking. Use sports emojis and hashtags."
        response = self.model.generate_content(prompt)
        return response.text.strip()

class OpinionAgent(Agent):
    def generate_post(self):
        prompt = "Generate a controversial opinion or hot take on current trends, politics, or culture. Make it provocative but not offensive, under 280 characters, designed to start debates. Encourage replies."
        response = self.model.generate_content(prompt)
        return response.text.strip()

class QuestionAgent(Agent):
    def generate_post(self):
        prompt = "Pose a thought-provoking question about life, trends, or opinions that will encourage replies and discussions. Make it relatable and engaging, under 280 characters. Include question emojis."
        response = self.model.generate_content(prompt)
        return response.text.strip()

class ListAgent(Agent):
    def generate_post(self):
        prompt = "Create a 'Top 5' or list-style post about interesting facts, tips, or rankings. Make it shareable and curiosity-piquing, under 280 characters. Use numbers and emojis."
        response = self.model.generate_content(prompt)
        return response.text.strip()

class GeneratePostAgent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.agents = [
            NewsAgent(self.model),
            MemeAgent(self.model),
            QuoteAgent(self.model),
            TechAgent(self.model),
            LifestyleAgent(self.model),
            EntertainmentAgent(self.model),
            FoodAgent(self.model),
            SportsAgent(self.model),
            OpinionAgent(self.model),
            QuestionAgent(self.model),
            ListAgent(self.model)
        ]

    def generate_post(self):
        agent = random.choice(self.agents)
        post = agent.generate_post()
        if len(post) > 280:
            post = post[:277] + "..."
        return post