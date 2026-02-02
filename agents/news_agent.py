from .base_agent import Agent

class NewsAgent(Agent):
    def generate_post(self):
        prompt = "Generate a clickbait engaging social media post about recent news events. Make it short, under 280 characters, and attention-grabbing."
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()