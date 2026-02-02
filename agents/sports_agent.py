from .base_agent import Agent

class SportsAgent(Agent):
    def generate_post(self):
        prompt = "Create an exciting post about sports news, game predictions, or athlete highlights. Make it dramatic and engaging, under 280 characters, to get fans talking. Use sports emojis and hashtags."
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()