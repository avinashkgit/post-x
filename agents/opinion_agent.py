from .base_agent import Agent

class OpinionAgent(Agent):
    def generate_post(self):
        prompt = "Generate a controversial opinion or hot take on current trends, politics, or culture. Make it provocative but not offensive, under 280 characters, designed to start debates. Encourage replies."
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()