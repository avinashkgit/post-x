from .base_agent import Agent

class TechAgent(Agent):
    def generate_post(self):
        prompt = "Generate a clickbait post about technology trends or gadgets. Make it engaging and under 280 characters."
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()