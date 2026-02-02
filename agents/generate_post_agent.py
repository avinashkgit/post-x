import random
from google import genai
from .base_agent import Agent


class GeneratePostAgent(Agent):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        super().__init__(self.client)

        # ---- Pattern-interrupt hooks (mixed energy) ----
        self.hooks = [
            "i know this is going to annoy some people, but",
            "this might sound random, but",
            "tell me i’m wrong, but",
            "i wasn’t even thinking about this until",
            "maybe this is obvious, but",
            "i just realized something kind of funny about",
            "not sure who needs to hear this, but",
            "lowkey can’t stop thinking about how",
        ]

        # ---- Personas (Twitter-native voices) ----
        self.personas = [
            "a burnt-out creative who types in lowercase",
            "a casual observer tweeting like it’s a group chat",
            "a curious overthinker",
            "someone scrolling and posting without much filter",
        ]

        # ---- Reality anchors (light context) ----
        self.anchors = [
            "the way the feed looks today",
            "a reply i just read",
            "that update everyone’s talking about",
            "scrolling way too long",
            "something i noticed earlier",
            "reading comments instead of the post",
        ]

        # ---- Post modes (THIS is the big unlock) ----
        self.post_modes = {
            "hot_take": {
                "tone": "confident but not aggressive",
                "ending": "invite disagreement or correction",
                "meaning": [
                    "because i think we overthink this stuff",
                    "because nobody ever says this part out loud",
                    "because it feels obvious once you notice it",
                ],
            },
            "observational_funny": {
                "tone": "light, amused, slightly sarcastic",
                "ending": "let the joke land without explaining it",
                "meaning": [
                    "because this keeps happening everywhere",
                    "because once you see it, you can’t unsee it",
                ],
            },
            "curious": {
                "tone": "genuinely curious, not judgmental",
                "ending": "end with a soft question or wondering",
                "meaning": [
                    "because i’m actually curious how people see this",
                    "because i feel like i’m missing something",
                ],
            },
            "realization": {
                "tone": "calm, slightly impressed",
                "ending": "trail off or let it sit",
                "meaning": [
                    "because it kind of explains a lot",
                    "because this suddenly made things click",
                ],
            },
            "chaotic": {
                "tone": "slightly unhinged but playful",
                "ending": "abrupt or absurd",
                "meaning": [
                    "because nothing about this makes sense anyway",
                    "because at this point, why not",
                ],
            },
            "appreciative": {
                "tone": "calm, genuine, grounded",
                "ending": "simple statement or soft thought",
                "meaning": [
                    "because some things are actually just good",
                    "because this made my day a little better",
                ],
            },
        }

    def _get_system_instruction(self) -> str:
        return (
            "You are a real Twitter/X user.\n"
            "You are not sad by default.\n"
            "You post for many reasons: humor, curiosity, confidence, chaos, appreciation.\n\n"
            "RULES:\n"
            "- NO emojis. NO hashtags.\n"
            "- Do not explain context.\n"
            "- Avoid formal structure or conclusions.\n"
            "- Sound like you posted this without rereading.\n"
            "- Avoid AI words (delve, testament, journey, tapestry, resonate).\n"
            "- If lowercase style is implied, do not capitalize."
        )

    def generate_post(self) -> str:
        persona = random.choice(self.personas)
        hook = random.choice(self.hooks)
        anchor = random.choice(self.anchors)
        mode_key = random.choice(list(self.post_modes.keys()))
        mode = self.post_modes[mode_key]
        meaning = random.choice(mode["meaning"])

        prompt = (
            f"Write a Twitter/X post as {persona}.\n\n"
            f"Start with this hook:\n'{hook}'\n\n"
            f"Lightly reference this somewhere:\n'{anchor}'\n\n"
            f"POST MODE: {mode_key}\n"
            f"TONE: {mode['tone']}\n"
            f"ENDING STYLE: {mode['ending']}\n\n"
            "Somewhere include one short line explaining why this matters to you, "
            f"like: '{meaning}'.\n\n"
            "Guidelines:\n"
            "- This can be funny, curious, confident, chaotic, or calm.\n"
            "- Do NOT default to sadness or frustration.\n"
            "- Use uneven line breaks.\n"
            "- It’s okay to contradict yourself lightly.\n"
            "- Do not summarize or teach.\n"
            "- End naturally based on the mode, not always with a question."
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

        # occasional lowercase aesthetic
        if random.random() < 0.25:
            text = text.lower()

        # remove overly neat endings
        if random.random() < 0.2:
            text = text.rstrip(".!?")

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        formatted = ""
        for line in lines:
            formatted += line + ("\n\n" if random.random() > 0.45 else "\n")

        return formatted.strip()
