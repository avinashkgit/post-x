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
            "chaotic": {
                "description": "wild, erratic, late-night energy - impulsive and slightly unhinged",
                "examples": [
                    "brain glitch moment",
                    "late-night thought",
                    "unhinged but harmless thought",
                    "this-shouldnt-make-sense-but-does",
                    "thought that feels illegal to post",
                    "absurd internet thought",
                    "random joke that barely makes sense",
                ]
            },
            "thoughtful": {
                "description": "quiet, introspective, evening reflection - deep but casual pondering",
                "examples": [
                    "quiet realization",
                    "unexpected insight",
                    "soft philosophical wondering",
                    "question that isnt really a question",
                    "meta thought about thinking",
                    "curious thought",
                    "thinking out loud",
                ]
            },
            "snarky": {
                "description": "witty, sarcastic, afternoon edge - confident opinions with bite",
                "examples": [
                    "mildly sarcastic realization",
                    "light hot take",
                    "confident but casual opinion",
                    "opinion stated without defending it",
                    "observation about online behavior",
                    "something everyone online does but nobody admits",
                ]
            },
            "chill": {
                "description": "calm, appreciative, morning ease - relaxed and positive vibes",
                "examples": [
                    "calm appreciation",
                    "small thing that made today better",
                    "noticing something nice for no reason",
                    "playful confusion",
                    "quietly enjoying something",
                    "funny observation",
                ]
            },
        }

    def _get_current_vibe_category(self):
        """Determine vibe category and time of day based on India time (Asia/Kolkata)."""
        local_hour = datetime.now(ZoneInfo("Asia/Kolkata")).hour

        if 0 <= local_hour < 6:
            category = "chaotic"
            time_of_day = "late night"
        elif 6 <= local_hour < 12:
            category = "chill"
            time_of_day = "morning"
        elif 12 <= local_hour < 18:
            category = "snarky"
            time_of_day = "afternoon"
        else:
            category = "thoughtful"
            time_of_day = "evening"

        return category, local_hour, time_of_day

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
            "- Sometimes be self-deprecating, sometimes confident, sometimes confused, excited, or nostalgic.\n"
            "- Reference pop culture, memes, or internet trends indirectly (e.g., allude to viral ideas without naming them).\n"
            "- Mix high-concept topics with mundane ones for unexpected juxtapositions.\n"
            "- Vary sentence length: short and punchy or rambling.\n"
            "- Occasionally draw from 'personal' (fictional) experiences to add relatability.\n"
            "- Occasionally incorporate subtle Indian cultural elements (e.g., references to chai, monsoon, or Bollywood vibes) when they fit naturally, without forcing them.\n"
        )

    def generate_post(self) -> str:
        category, local_hour, time_of_day = self._get_current_vibe_category()
        vibe = random.choice(self.vibe_library[category]["examples"])
        vibe_description = self.vibe_library[category]["description"]

        token_limits = {"chaotic": 60, "chill": 80, "snarky": 100, "thoughtful": 125}
        token_limit = token_limits[category]

        if self.debug:
            print("\n--- DEBUG ---")
            print(f"India Hour : {local_hour}")
            print(f"Time of Day: {time_of_day}")
            print(f"Category   : {category}")
            print(f"Vibe       : {vibe}")
            print(f"Description: {vibe_description}")
            print(f"Token Limit: {token_limit}")
            print("------------\n")

        prompt_templates = [
            f"Write a single X/Twitter post with this vibe: {vibe} ({vibe_description}), considering it's currently {time_of_day} ({local_hour}:00) in India.\n\n"
            "Choose a completely random, unexpected topic - could be about technology, relationships, food, space, daily life, politics, obscure hobbies, hypothetical scenarios, or something wildly offbeat like why vending machines exist or if clouds have feelings.\n"
            "Make it feel like a genuine, unfiltered thought that just popped into your head, with a subtle hook or twist to make it engaging.\n"
            "Don't explain, don't justify, don't add context - just the raw thought.\n"
            "Make it relatable, like something anyone might think but few would post, and avoid common internet clichés.\n"
            "Occasionally end with an ambiguous question to invite replies.\n",
            f"Imagine you're scrolling through X at {local_hour}:00 in India during {time_of_day}. What unfiltered thought with a {vibe} ({vibe_description}) feel pops into your head?\n\n"
            "Pick any random topic - tech, relationships, food, politics, space, daily absurdities, or bizarre hypotheticals.\n"
            "Share it raw, no explanations, just the impulsive idea that feels too real to ignore.\n"
            "Add a twist or question to spark curiosity, keeping it casual and human.\n",
            f"Channel a {vibe} ({vibe_description}) mood at {local_hour}:00 {time_of_day} in India. What's the one weird thought you'd post without thinking?\n\n"
            "Topic could be anything from mundane daily stuff to wild political musings or sci-fi daydreams.\n"
            "Keep it short, relatable, and ending with something that makes people pause or reply.\n"
            "No fluff, just the core unfiltered notion.\n"
        ]
        prompt = random.choice(prompt_templates)

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                "system_instruction": self._get_system_instruction(),
                "temperature": 1.2,  # high randomness
                "max_output_tokens": token_limit,
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
