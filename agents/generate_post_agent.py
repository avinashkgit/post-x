import random
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+
from google import genai
from .base_agent import Agent


class GeneratePostAgent(Agent):
    def __init__(self, api_key: str, debug: bool = False):
        self.client = genai.Client(api_key=api_key)
        super().__init__(self.client)

        self.debug = debug

        # Vibes grouped loosely by time-of-day (IST)
        self.vibe_library = {
            "chaotic": [
                "brain glitch moment",
                "late-night thought",
                "unhinged but harmless thought",
                "this-shouldnt-make-sense-but-does",
                "thought that feels illegal to post",
                "absurd internet thought",
                "random joke that barely makes sense",
            ],
            "thoughtful": [
                "quiet realization",
                "unexpected insight",
                "soft philosophical wondering",
                "question that isnt really a question",
                "meta thought about thinking",
                "curious thought",
                "thinking out loud",
            ],
            "snarky": [
                "mildly sarcastic realization",
                "light hot take",
                "confident but casual opinion",
                "opinion stated without defending it",
                "observation about online behavior",
                "something everyone online does but nobody admits",
            ],
            "chill": [
                "calm appreciation",
                "small thing that made today better",
                "noticing something nice for no reason",
                "playful confusion",
                "quietly enjoying something",
                "funny observation",
            ],
        }

    def _get_current_vibe_category(self):
        """Determine vibe category based on India time (Asia/Kolkata)."""
        local_hour = datetime.now(ZoneInfo("Asia/Kolkata")).hour

        if 0 <= local_hour < 6:
            category = "chaotic"
        elif 6 <= local_hour < 12:
            category = "chill"
        elif 12 <= local_hour < 18:
            category = "snarky"
        else:
            category = "thoughtful"

        return category, local_hour

    def _get_system_instruction(self) -> str:
        return (
            "You are a real Twitter/X user.\n"
            "You post spontaneous thoughts about anything: science, tech, jokes, philosophy, culture, or random ideas.\n"
            "Nothing is planned. Nothing is explained.\n\n"
            "RULES:\n"
            "- NO emojis. NO hashtags.\n"
            "- Do NOT teach or define things.\n"
            "- Avoid structure, lists, or conclusions.\n"
            "- Use casual language.\n"
            "- Sound human, impulsive, and a little unpredictable.\n"
            "- lowercase preferred, but small inconsistencies are okay."
        )

    def generate_post(self) -> str:
        category, local_hour = self._get_current_vibe_category()
        vibe = random.choice(self.vibe_library[category])

        if self.debug:
            print("\n--- DEBUG ---")
            print(f"India Hour : {local_hour}")
            print(f"Category   : {category}")
            print(f"Vibe       : {vibe}")
            print("------------\n")

        prompt = (
            "Think of a completely random topic and write a short, spontaneous X post.\n"
            f"VIBE: {vibe}\n"
            "Do not explain context. Let it feel impulsive and real."
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                "system_instruction": self._get_system_instruction(),
                "temperature": 1.2,  # high randomness
                "max_output_tokens": 50,  # short, tweet-like
            },
            contents=prompt,
        )

        return self._format(response.text.strip())

    def _format(self, text: str) -> str:
        text = text.replace("**", "").replace('"', "").strip()

        # Mostly lowercase, but not always (more human)
        if random.random() < 0.85:
            text = text.lower()

        # Sometimes trail off
        if random.random() < 0.3:
            text = text.rstrip(".!?")

        # Add uneven spacing
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        output = ""

        for line in lines:
            output += line + ("\n\n" if random.random() > 0.6 else "\n")

        return output.strip()
