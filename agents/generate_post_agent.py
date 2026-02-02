import random
from google import genai
from .base_agent import Agent


class GeneratePostAgent(Agent):
    def __init__(self, api_key: str, debug: bool = False):
        self.client = genai.Client(api_key=api_key)
        super().__init__(self.client)

        self.debug = debug  # toggle prints on/off

        # ---- Pattern-interrupt hooks ----
        self.hooks = [
            "this might sound random, but",
            "tell me if i’m missing something, but",
            "i just realized something kind of wild about",
            "maybe this is obvious, but",
            "i wasn’t even thinking about this until",
            "lowkey can’t stop thinking about how",
            "i know this sounds dumb, but",
            "not sure why this clicked just now, but",
        ]

        # ---- Personas ----
        self.personas = [
            "a curious overthinker",
            "someone tweeting like it’s a group chat",
            "a slightly nerdy observer",
            "a casual scroller posting without much filter",
            "a thoughtful person with a sense of humor",
        ]

        # ---- Topic domains ----
        self.domains = {
            "science": {
                "angle": [
                    "how strange reality actually is",
                    "how little we really understand",
                    "how counterintuitive this feels",
                ],
                "meaning": [
                    "because it makes everyday life feel less boring",
                    "because it messes with my sense of reality",
                    "because this never stops being weird to me",
                ],
            },
            "tech": {
                "angle": [
                    "how fast things change",
                    "how normalized this already feels",
                    "how nobody really questions this anymore",
                ],
                "meaning": [
                    "because i remember when this felt futuristic",
                    "because we adapted way too fast",
                    "because this is probably changing us quietly",
                ],
            },
            "philosophy": {
                "angle": [
                    "what this says about people",
                    "how much of life is just interpretation",
                    "how weird meaning actually is",
                ],
                "meaning": [
                    "because it changes how i look at small things",
                    "because i catch myself thinking about this a lot",
                    "because it sneaks up on you",
                ],
            },
            "jokes": {
                "angle": [
                    "how ridiculous this is when you zoom out",
                    "how this feels like a bit but isn’t",
                    "how this sounds fake but isn’t",
                ],
                "meaning": [
                    "because once you notice it, it’s everywhere",
                    "because this is unintentionally hilarious",
                ],
            },
            "culture": {
                "angle": [
                    "how quickly we move on",
                    "how performative this feels",
                    "how everyone pretends this is normal",
                ],
                "meaning": [
                    "because it says more than we admit",
                    "because this didn’t used to feel like this",
                ],
            },
            "random": {
                "angle": [
                    "how my brain made this connection",
                    "why this popped into my head",
                    "how this makes no sense but still feels true",
                ],
                "meaning": [
                    "because my brain does this sometimes",
                    "because this felt worth saying out loud",
                ],
            },
        }

        # ---- Context anchors ----
        self.anchors = [
            "scrolling the feed",
            "reading a comment",
            "something i saw earlier",
            "a random notification",
            "a conversation i overheard",
            "staring at my screen for too long",
        ]

        # ---- Post modes ----
        self.post_modes = {
            "observational": "light, curious, slightly amused",
            "hot_take": "confident but not aggressive",
            "curious": "genuinely wondering",
            "playful": "slightly absurd or ironic",
            "reflective": "calm, thoughtful, not deep on purpose",
        }

    def _get_system_instruction(self) -> str:
        return (
            "You are a real Twitter/X user.\n"
            "You post about many things: science, tech, jokes, philosophy, culture, random thoughts.\n"
            "You are not trying to educate or impress.\n\n"
            "RULES:\n"
            "- NO emojis. NO hashtags.\n"
            "- Do NOT explain concepts.\n"
            "- Avoid formal structure or conclusions.\n"
            "- Use casual language and uneven spacing.\n"
            "- Avoid AI words (delve, testament, journey, tapestry, resonate).\n"
            "- This should feel like a thought, not a post."
        )

    def generate_post(self) -> str:
        persona = random.choice(self.personas)
        hook = random.choice(self.hooks)
        anchor = random.choice(self.anchors)

        domain_key = random.choice(list(self.domains.keys()))
        domain = self.domains[domain_key]
        angle = random.choice(domain["angle"])
        meaning = random.choice(domain["meaning"])

        mode_key = random.choice(list(self.post_modes.keys()))
        mode_tone = self.post_modes[mode_key]

        # ---- DEBUG PRINT (random choices) ----
        if self.debug:
            print("\n--- POST DEBUG ---")
            print(f"Persona     : {persona}")
            print(f"Hook        : {hook}")
            print(f"Domain      : {domain_key}")
            print(f"Angle       : {angle}")
            print(f"Meaning     : {meaning}")
            print(f"Mode        : {mode_key}")
            print(f"Tone        : {mode_tone}")
            print(f"Anchor      : {anchor}")
            print("------------------\n")

        prompt = (
            f"Write a Twitter/X post as {persona}.\n\n"
            f"Start with this hook:\n'{hook}'\n\n"
            f"Lightly reference this somewhere:\n'{anchor}'\n\n"
            f"TOPIC DOMAIN: {domain_key}\n"
            f"ANGLE: {angle}\n"
            f"TONE: {mode_tone}\n\n"
            "Somewhere include one short line explaining why this matters to you, "
            f"like: '{meaning}'.\n\n"
            "Guidelines:\n"
            "- This can be funny, curious, playful, insightful, or random.\n"
            "- Do NOT explain or teach.\n"
            "- Let the thought wander slightly.\n"
            "- Use uneven line breaks.\n"
            "- End naturally."
        )

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                "system_instruction": self._get_system_instruction(),
                "temperature": 0.95,
                "top_p": 0.97,
            },
            contents=prompt,
        )

        return self._clean_and_format(response.text.strip())

    def _clean_and_format(self, text: str) -> str:
        text = text.replace("**", "").replace('"', "").strip()

        if random.random() < 0.25:
            text = text.lower()

        if random.random() < 0.2:
            text = text.rstrip(".!?")

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        formatted = ""
        for line in lines:
            formatted += line + ("\n\n" if random.random() > 0.45 else "\n")

        return formatted.strip()
