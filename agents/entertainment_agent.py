from .base_agent import Agent

class EntertainmentAgent(Agent):
    def generate_post(self):
        prompt = "Create a buzzworthy post about movies, TV shows, celebrities, or pop culture. Make it controversial or exciting, under 280 characters, to spark discussions and shares. Use emojis and trending hashtags."
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()