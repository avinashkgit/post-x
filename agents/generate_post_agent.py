import random
from google import genai
from .base_agent import Agent


class GeneratePostAgent(Agent):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        super().__init__(self.client)

        # ---- Persona (who is speaking) ----
        self.personas = [
            "an office worker scrolling late at night",
            "a tired but thoughtful professional",
            "someone slightly burnt out but observant",
            "a curious person who overthinks things",
            "someone casually sharing a thought with friends",
            "a tech-aware but non-expert person",
            "a fan reacting emotionally, not logically",
        ]

        # ---- Emotional state (how it feels) ----
        self.emotions = [
            "a bit tired",
            "slightly annoyed",
            "quietly hopeful",
            "confused but curious",
            "mildly frustrated",
            "thoughtful and calm",
            "unsure how to feel",
        ]

        # ---- Intent styles (how the post behaves) ----
        self.intents = [
            "reacting in the moment",
            "thinking out loud",
            "sharing a small realization",
            "venting without blaming",
            "reflecting without teaching",
            "wondering rather than concluding",
        ]

        # ---- Length bands ----
        self.length_modes = {
            "short": "Keep it brief and natural. One or two short paragraphs at most.",
            "medium": "Let it breathe. A few short paragraphs with pauses.",
            "long": "Write a longer post with multiple short paragraphs. It can ramble slightly."
        }

        # ---- Core topic prompts ----
        self.topics = [
            # News / current events
            (
                "React to a news or current event without summarizing it. "
                "Avoid facts or headlines. Focus only on how it makes you feel or think."
            ),

            # Humor / memes
            (
                "Share a funny or relatable thought based on everyday life. "
                "Dry humor, irony, or quiet sarcasm works best."
            ),

            # Reflection / life
            (
                "Share a personal thought about life, growth, routine, or change. "
                "Not advice. Just experience."
            ),

            # Tech / AI
            (
                "Share a casual thought about technology, AI, or digital life. "
                "Curious or skeptical, but never expert-like."
            ),

            # Lifestyle / mental state
            (
                "Write about habits, burnout, relationships, mental state, or routine. "
                "Make it feel like a confession or late-night realization."
            ),

            # Entertainment / pop culture
            (
                "Share a personal take on a movie, show, celebrity, or pop culture moment. "
                "Sound like you’re talking to friends, not reviewing."
            ),

            # Food
            (
                "Write about food tied to mood, memory, craving, or disappointment. "
                "No recipes. Just feeling."
            ),

            # Sports
            (
                "Write a sports-related post driven by emotion or instinct. "
                "Bias and overconfidence are allowed."
            ),

            # Opinions
            (
                "Share an opinion that feels slightly risky to post. "
                "Respectful, honest, and uncertain."
            ),

            # Open question
            (
                "Build toward a question people would realistically reply to. "
                "You can include brief personal context."
            ),

            # Lists
            (
                "Write a loose, casual list of thoughts or observations. "
                "Messy structure is fine."
            ),
        ]

    def _build_prompt(self) -> str:
        persona = random.choice(self.personas)
        emotion = random.choice(self.emotions)
        intent = random.choice(self.intents)
        length_key = random.choice(list(self.length_modes.keys()))
        length_rule = self.length_modes[length_key]
        topic = random.choice(self.topics)

        return (
            f"Write a social media post as {persona}. "
            f"The tone should feel {emotion}. "
            f"You are {intent}. "
            f"{topic} "
            f"{length_rule} "
            "Use natural language, contractions, and occasional sentence fragments. "
            "It’s okay if it’s imperfect or slightly rambling. "
            "Avoid sounding confident, authoritative, or polished. "
            "Do not teach, summarize, or conclude. "
            "End with a genuine question if it feels natural. "
            "No hashtags, no emojis."
        )

    def _cleanup(self, text: str) -> str:
        # Remove classic AI polish phrases
        kill_phrases = [
            "In conclusion",
            "Overall",
            "Ultimately",
            "This shows that",
            "It is important to note",
            "One must understand",
        ]
        for phrase in kill_phrases:
            text = text.replace(phrase, "")

        # Normalize spacing
        text = text.strip()
        return text

    def generate_post(self) -> str:
        prompt = self._build_prompt()

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        post = response.text.strip()
        post = self._cleanup(post)

        return post
