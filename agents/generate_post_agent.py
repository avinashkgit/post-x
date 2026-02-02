import random
from google import genai
from .base_agent import Agent


class GeneratePostAgent(Agent):
    def __init__(self, api_key: str, debug: bool = False):
        self.client = genai.Client(api_key=api_key)
        super().__init__(self.client)
        self.debug = debug

        # High-level vibes only (not content)
        self.vibes = [
            # light / fun
            "funny observation",
            "playful confusion",
            "absurd internet thought",
            "random joke that barely makes sense",
            "mildly sarcastic realization",
            "unexpectedly funny comparison",
            # curious / thoughtful
            "curious thought",
            "quiet realization",
            "unexpected insight",
            "thinking out loud",
            "soft philosophical wondering",
            "question that isn’t really a question",
            # chaotic / weird
            "brain glitch moment",
            "late-night thought",
            "unhinged but harmless thought",
            "connecting unrelated things",
            "this-shouldn’t-make-sense-but-does",
            "thought that feels illegal to post",
            # confident / spicy
            "light hot take",
            "confident but casual opinion",
            "take that sounds obvious after you hear it",
            "opinion stated without defending it",
            # calm / positive
            "calm appreciation",
            "small thing that made today better",
            "quietly enjoying something",
            "noticing something nice for no reason",
            # internet / culture
            "observation about online behavior",
            "weird pattern on the internet",
            "something everyone online does but nobody admits",
            "how the feed subtly changes your brain",
            # meta / self-aware
            "meta thought about thinking",
            "realizing why you posted this at all",
            "commenting on your own thought mid-post",
        ]

    def _get_system_instruction(self) -> str:
        return (
            "You are a real Twitter/X user.\n"
            "You post spontaneous thoughts about anything: science, tech, philosophy, jokes, daily life.\n"
            "Nothing is planned. Nothing is explained.\n\n"
            "RULES:\n"
            "- NO emojis. NO hashtags.\n"
            "- Do NOT teach or define things.\n"
            "- Avoid structure, lists, or conclusions.\n"
            "- Use uneven spacing and short lines.\n"
            "- Sound human, casual, and a little unpredictable.\n"
            "- This should feel like it came out of nowhere."
        )

    def generate_post(self) -> str:
        vibe = random.choice(self.vibes)

        if self.debug:
            print("\n--- DEBUG ---")
            print(f"Vibe: {vibe}")
            print("------------\n")

        prompt = (
            "Write a Twitter/X post.\n\n"
            f"VIBE: {vibe}\n\n"
            "Instructions:\n"
            "- Come up with your own hook naturally.\n"
            "- The topic can be anything.\n"
            "- Don’t explain context.\n"
            "- Don’t sound polished or finished.\n"
            "- Let it feel impulsive and real.\n"
            "- End however it wants."
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                "system_instruction": self._get_system_instruction(),
                "temperature": 1.0,  # higher = more randomness
                "top_p": 0.98,
            },
            contents=prompt,
        )

        return self._format(response.text.strip())

    def _format(self, text: str) -> str:
        text = text.replace("**", "").replace('"', "").strip()

        # occasional lowercase aesthetic
        if random.random() < 0.4:
            text = text.lower()

        # sometimes cut punctuation
        if random.random() < 0.25:
            text = text.rstrip(".!?")

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        output = ""
        for line in lines:
            output += line + ("\n\n" if random.random() > 0.5 else "\n")

        return output.strip()
