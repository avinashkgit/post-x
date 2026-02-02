from .base_agent import Agent

class QuoteAgent(Agent):
    def generate_post(self):
        prompt = "Generate an inspirational quote or motivational post. Make it engaging and under 280 characters."
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()