from google import genai

class Agent:
    def __init__(self, client):
        self.client = client

    def generate_post(self):
        raise NotImplementedError