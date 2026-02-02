import random
from google import genai
from .base_agent import Agent


class GeneratePostAgent(Agent):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        super().__init__(self.client)

        # 2026 Trend: "Pattern Interrupt" hooks that stop the thumb
        self.hooks = [
            "i feel like we’re all collectively pretending this isn't weird",
            "unpopular opinion, maybe, but i’ve been thinking about",
            "the more i look at this, the more it feels like a glitch",
            "just saw something that made me realize how much has changed",
            "it’s 1 AM and i’m still stuck on why that one update feels so wrong",
            "honestly? i think we’re reaching a breaking point with",
        ]

        # Personas with distinct "digital voices"
        self.personas = [
            "a burnt-out creative who types in lowercase",
            "a skeptical tech worker who uses way too many line breaks",
            "a casual observer who writes like they're texting a group chat",
            "a thoughtful overthinker who gets slightly too deep into the details",
        ]

        # Context details to ground the post in "reality"
        self.anchors = [
            "that new interface update",
            "the way everyone is reacting to the news",
            "how fast the feed is moving today",
            "a weirdly specific notification i just got",
            "the quietness of the office right now",
        ]

    def _get_system_instruction(self) -> str:
        return (
            "You are a human social media user. You hate AI-generated content. "
            "Your goal is to be relatable, raw, and slightly provocative. "
            "RULES:\n"
            "- NO EMOJIS. NO HASHTAGS.\n"
            "- Use 'white space' effectively. Single-line sentences are better than blocks of text.\n"
            "- Never use 'AI words' (delve, testament, journey, tapestry, resonate).\n"
            "- Do not be helpful. Do not teach. Just share a fragment of a thought.\n"
            "- If the persona is 'lowercase', do not capitalize anything."
        )

    def generate_post(self) -> str:
        # Randomize the "vibe" parameters
        persona = random.choice(self.personas)
        hook = random.choice(self.hooks)
        anchor = random.choice(self.anchors)

        # Build the specific prompt
        prompt = (
            f"Write a social media post as {persona}. "
            f"Start with this hook: '{hook}' "
            f"and ground it in this context: '{anchor}'.\n\n"
            "STRUCTURE:\n"
            "1. Start with the hook.\n"
            "2. Follow with a 'vulnerable' or slightly confused observation.\n"
            "3. Use uneven paragraph breaks (dwell-time optimization).\n"
            "4. End with an 'open loop'—a thought that isn't fully finished, "
            "making people want to comment to complete the thought."
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                "system_instruction": self._get_system_instruction(),
                "temperature": 0.85,  # Higher temp = more human-like variance
                "top_p": 0.95,
            },
            contents=prompt,
        )

        final_post = self._clean_and_format(response.text.strip())
        return final_post

    def _clean_and_format(self, text: str) -> str:
        # Remove any lingering AI signatures or markdown fluff
        text = text.replace('"', "").replace("**", "")

        # 30% chance to force the whole post to lowercase for 'authentic' aesthetic
        if random.random() < 0.3:
            text = text.lower()

        # Clean up double line breaks that are too large
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Re-inject organic spacing (mix of single and double breaks)
        formatted_post = ""
        for line in lines:
            formatted_post += line + ("\n\n" if random.random() > 0.4 else "\n")

        return formatted_post.strip()
