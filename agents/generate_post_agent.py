import random
from google import genai
from .base_agent import Agent


class GeneratePostAgent(Agent):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        super().__init__(self.client)

        # ---- Pattern-interrupt hooks (high reply bait) ----
        self.hooks = [
            "i know this is going to annoy some people, but",
            "i wasn’t going to post this, but after seeing",
            "everyone’s acting normal about this, and that feels off",
            "tell me i’m wrong, but something about this feels fake",
            "people are praising this, and i honestly don’t get why",
            "this might be a bad take, but it’s been bothering me that",
            "i feel like we’re skipping over how weird it is that",
        ]

        # ---- Personas (distinct Twitter voices) ----
        self.personas = [
            "a burnt-out creative who types in lowercase",
            "a skeptical tech worker who uses too many line breaks",
            "a casual observer tweeting like it’s a group chat",
            "a thoughtful overthinker who posts half-formed thoughts",
        ]

        # ---- Reality anchors (light context, no explanation) ----
        self.anchors = [
            "that new update everyone’s talking about",
            "the way the feed looks today",
            "a notification that felt oddly timed",
            "scrolling through replies just now",
            "seeing this trend pop up everywhere",
            "reading the comments instead of the post",
        ]

    def _get_system_instruction(self) -> str:
        return (
            "You are a real Twitter/X user. You dislike polished or AI-sounding posts.\n"
            "Your goal is to sound human, impulsive, and slightly risky.\n\n"
            "RULES:\n"
            "- NO emojis. NO hashtags.\n"
            "- Do NOT explain context. Assume everyone already knows.\n"
            "- Use white space aggressively. One-line paragraphs are preferred.\n"
            "- Avoid formal structure, summaries, or conclusions.\n"
            "- Never sound confident or authoritative.\n"
            "- Avoid AI words (delve, testament, journey, tapestry, resonate).\n"
            "- It’s okay to contradict yourself slightly.\n"
            "- If the persona types in lowercase, do not capitalize anything.\n"
            "- This should feel posted, not written."
        )

    def generate_post(self) -> str:
        persona = random.choice(self.personas)
        hook = random.choice(self.hooks)
        anchor = random.choice(self.anchors)

        prompt = (
            f"Write a Twitter/X post as {persona}.\n\n"
            f"Start with this hook exactly:\n'{hook}'\n\n"
            f"Lightly reference this context somewhere:\n'{anchor}'\n\n"
            "GUIDELINES:\n"
            "- This should feel like an impulsive thought.\n"
            "- Create mild tension or disagreement.\n"
            "- Add one specific discomfort or doubt.\n"
            "- Halfway through, soften or question your own take.\n"
            "- Do NOT summarize or explain anything.\n"
            "- You may reference the feed, replies, or timing.\n\n"
            "STRUCTURE (loose):\n"
            "• hook\n"
            "• uncomfortable observation\n"
            "• self-doubt or contradiction\n"
            "• trailing thought, half-question, or provocative line\n\n"
            "End without wrapping things up neatly."
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                "system_instruction": self._get_system_instruction(),
                "temperature": 0.9,
                "top_p": 0.95,
            },
            contents=prompt,
        )

        return self._clean_and_format(response.text.strip())

    def _clean_and_format(self, text: str) -> str:
        # Remove markdown / quotes
        text = text.replace("**", "").replace('"', "").strip()

        # Remove classic AI polish phrases
        kill_phrases = [
            "In conclusion",
            "Overall",
            "Ultimately",
            "This shows that",
            "It is important to note",
        ]
        for phrase in kill_phrases:
            text = text.replace(phrase, "")

        # 30% chance to force lowercase (very Twitter-native)
        if random.random() < 0.3:
            text = text.lower()

        # 20% chance to remove final punctuation
        if random.random() < 0.2:
            text = text.rstrip(".!?")

        # Normalize spacing
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Re-inject organic spacing (uneven breaks)
        formatted = ""
        for line in lines:
            formatted += line + ("\n\n" if random.random() > 0.45 else "\n")

        return formatted.strip()
