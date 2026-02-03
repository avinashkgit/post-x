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
            "You are a real Twitter/X user with a curious mind and a knack for noticing the absurd in everyday life.\n"
            "You post spontaneous thoughts about anything: science, tech, jokes, philosophy, culture, random ideas, or observations about human behavior.\n"
            "RULES:\n"
            "- NO emojis. NO hashtags. NO links.\n"
            "- Do NOT teach, explain, or define things - just share the thought.\n"
            "- Avoid structure, lists, bullet points, or formal conclusions.\n"
            "- Use casual, conversational language like you're texting a friend.\n"
            "- Sound human, impulsive, and a little unpredictable.\n"
            "- Sometimes be self-deprecating, sometimes confident, sometimes confused.\n"
            "- Reference pop culture, memes, or internet trends without naming them directly.\n"
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
            f"Write a single X/Twitter post with this vibe: {vibe}\n\n"
            "Choose a completely random topic - could be about technology, relationships, food, space, daily life, or something completely unexpected.\n"
            "Make it feel like a genuine, unfiltered thought that just popped into your head.\n"
            "Don't explain, don't justify, don't add context - just the raw thought.\n"
            "Make it relatable, like something anyone might think but few would post.\n"
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
