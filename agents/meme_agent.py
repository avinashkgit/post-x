from .base_agent import Agent

class MemeAgent(Agent):
    def generate_post(self):
        prompt = "Generate a funny, meme-style social media post or joke. Keep it short, engaging, and under 280 characters."
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()