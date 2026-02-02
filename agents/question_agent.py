from .base_agent import Agent

class QuestionAgent(Agent):
    def generate_post(self):
        prompt = "Pose a thought-provoking question about life, trends, or opinions that will encourage replies and discussions. Make it relatable and engaging, under 280 characters. Include question emojis."
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()