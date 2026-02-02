from .base_agent import Agent

class FoodAgent(Agent):
    def generate_post(self):
        prompt = "Generate a mouth-watering post about food, recipes, cooking tips, or dining experiences. Make it visually appealing in text form, under 280 characters, and ask followers to share their favorites. Include food emojis."
        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()