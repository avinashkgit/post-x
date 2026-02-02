from .base_agent import Agent

class LifestyleAgent(Agent):
    def generate_post(self):
        prompt = "Generate an engaging social media post about lifestyle topics like health, fitness, relationships, or self-care. Make it clickbait, under 280 characters, and encourage engagement with questions or calls to action. Include emojis and hashtags."
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()