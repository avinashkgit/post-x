from .base_agent import Agent

class ListAgent(Agent):
    def generate_post(self):
        prompt = "Create a 'Top 5' or list-style post about interesting facts, tips, or rankings. Make it shareable and curiosity-piquing, under 280 characters. Use numbers and emojis."
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()