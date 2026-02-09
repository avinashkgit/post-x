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
                    "what if scenario that doesnt make sense",
                    "truly unhinged observation",
                    "the chaos is getting to me",
                    "internet made me think this",
                ],
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
                    "random existential moment",
                    "something thats been stuck in my head",
                    "soft realization about life",
                    "weirdly profound observation",
                    "thought spiral but make it poetic",
                ],
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
                    "sarcastic commentary on existence",
                    "annoyed but make it funny",
                    "controversial opinion that isnt really controversial",
                    "soft roast of internet culture",
                    "painfully accurate take",
                ],
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
                    "gentle amusement",
                    "life moment captured",
                    "found peace in something silly",
                    "vibe check: good",
                    "unexpectedly wholesome thought",
                ],
            },
            "nostalgic": {
                "description": "wistful, reminiscent, bittersweet - lost in memories and what used to be",
                "examples": [
                    "remembering something from forever ago",
                    "wow i miss that era",
                    "that was actually the peak",
                    "randomly thinking about the past",
                    "things used to hit different",
                    "old memory suddenly popping up",
                    "culture was different back then",
                    "golden age moment",
                    "remembering when things were simpler",
                    "time travel in my head",
                ],
            },
            "curious": {
                "description": "inquisitive, fascinated, wonder-struck - genuinely wanting to understand",
                "examples": [
                    "genuinely confused about something",
                    "rabbit hole rabbit hole",
                    "how does this even work",
                    "wait but why though",
                    "going down a curiosity spiral",
                    "legitimately mind-blown",
                    "never thought about it like that",
                    "okay but what if",
                    "im hyperfixating on this thought",
                    "this rabbit hole is deep",
                ],
            },
            "energetic": {
                "description": "hyped, excited, buzzing - full of enthusiasm and momentum",
                "examples": [
                    "cant stop thinking about this",
                    "this is actually insane",
                    "brain is going at 100mph",
                    "genuinely excited about something dumb",
                    "hyperfixation energy",
                    "literally cannot stop",
                    "ive been thinking about this for hours",
                    "the thoughts are THOUGHTS",
                    "way too into this right now",
                    "unhinged enthusiasm mode",
                ],
            },
            "cynical": {
                "description": "jaded, sardonic, world-weary - seeing through the noise with dark humor",
                "examples": [
                    "why does nobody talk about this",
                    "honestly kind of absurd",
                    "capitalist hellscape moment",
                    "were all just pretending arent we",
                    "everything is kinda funny if you think about it",
                    "nothing matters but also everything",
                    "the system is broken and nobody cares",
                    "dark humor because reality is dark",
                    "its all a scam isnt it",
                    "we live in a simulation apparently",
                ],
            },
            "melancholic": {
                "description": "sad but poetic, bittersweet - beauty in the sadness",
                "examples": [
                    "soft sadness energy",
                    "things arent what they used to be",
                    "beautiful in a weird broken way",
                    "loneliness hit different tonight",
                    "there's something haunting about this",
                    "why does sadness feel poetic",
                    "ache in a quiet way",
                    "mourning something i cant name",
                    "melancholy without the drama",
                    "beautifully tragic moment",
                ],
            },
            "absurd": {
                "description": "surreal, ridiculous, nonsensical - laughing at the illogic of it all",
                "examples": [
                    "why is this a thing",
                    "the world is genuinely hilarious",
                    "this makes no sense and i love it",
                    "we collectively agreed to this",
                    "humanity is a fever dream",
                    "watching reality unfold like a comedy",
                    "the absurdity is the point",
                    "this is peak comedy",
                    "logic has left the chat",
                    "the simulation has a sense of humor",
                ],
            },
            "vulnerable": {
                "description": "raw, honest, unguarded - letting the walls down for real",
                "examples": [
                    "i dont know how to feel about this",
                    "genuinely struggling with something",
                    "scared to admit this but here we are",
                    "feeling small tonight",
                    "needing to say this out loud",
                    "raw moment",
                    "this hurts in ways i cant explain",
                    "admitting something ive been hiding",
                    "too real right now",
                    "stripped down and honest",
                ],
            },
            "inspired": {
                "description": "motivated, hopeful, seeing potential - feeling the spark",
                "examples": [
                    "genuinely inspired by something",
                    "the future could be beautiful",
                    "what if we actually tried",
                    "feeling creative energy",
                    "the possibilities are endless",
                    "this makes me want to create",
                    "hope hit different today",
                    "belief in something bigger",
                    "lets actually do something",
                    "the spark is real right now",
                ],
            },
            "petty": {
                "description": "annoyed, nitpicky, venting - small grievances blown up",
                "examples": [
                    "why does this bother me so much",
                    "okay but like why though",
                    "im beefing with something silly",
                    "this is driving me insane for no reason",
                    "the pettiness is strong",
                    "fighting with my own brain",
                    "genuinely mad about something dumb",
                    "the audacity of this thing",
                    "i cant let this go",
                    "the irritation is real",
                ],
            },
            "reflective": {
                "description": "measured, introspective, processing - taking stock and making sense",
                "examples": [
                    "putting thoughts together",
                    "reflection time has begun",
                    "connecting the dots",
                    "what does it all mean though",
                    "taking inventory of life",
                    "piecing it all together",
                    "moment of clarity",
                    "seeing patterns everywhere",
                    "the bigger picture is",
                    "understanding something finally",
                ],
            },
            "anxious": {
                "description": "worried, spiraling, overthinking - the mind racing",
                "examples": [
                    "brain is in overdrive",
                    "something feels off but i cant name it",
                    "spiraling slightly",
                    "too many thoughts at once",
                    "the anxiety is real tonight",
                    "what if what if what if",
                    "overthinking is my cardio",
                    "why am i like this",
                    "the dread is setting in",
                    "nervous energy coursing through",
                ],
            },
            "playful": {
                "description": "teasing, lighthearted, witty - having fun with language and ideas",
                "examples": [
                    "having a laugh at the world",
                    "jokes on jokes on jokes",
                    "playful chaos energy",
                    "this is funny and you know it",
                    "teasing the internet gently",
                    "word games and brain plays",
                    "being silly on purpose",
                    "laughing at our own weirdness",
                    "the humor in the mundane",
                    "treating life like a joke",
                ],
            },
            "tech_obsessed": {
                "description": "fascinated by technology, building, innovation - nerding out hard",
                "examples": [
                    "another sleepless night coding",
                    "this new tech is actually unhinged",
                    "why doesnt everyone use this tool",
                    "the future of tech is wild",
                    "building things is peak dopamine",
                    "ai is doing things nobody expected",
                    "the engineering is insane",
                    "tech solves everything except happiness apparently",
                    "obsessed with optimizing everything",
                    "the innovation never stops coming",
                ],
            },
            "science_struck": {
                "description": "blown away by science, discovery, the cosmos - wonder about existence",
                "examples": [
                    "the universe is genuinely insane",
                    "science proves reality is weirder than fiction",
                    "how is this even possible",
                    "the more you learn the less sense it makes",
                    "space is terrifying and beautiful",
                    "biology is literally wild",
                    "we barely understand anything actually",
                    "quantum mechanics broke my brain",
                    "discovery hits different",
                    "the science community is out of their minds in the best way",
                ],
            },
            "digital_native": {
                "description": "internet culture, memes, online logic - speaking the language of the web",
                "examples": [
                    "this is how internet culture works now",
                    "the meta is deep",
                    "memes are philosophy",
                    "the internet has its own physics",
                    "online behavior is a science",
                    "web3 discourse never dies",
                    "crypto taught me something about human nature",
                    "viral moments hit different",
                    "the algorithm knows all",
                    "internet logic defies reality",
                ],
            },
            "philosophical_tech": {
                "description": "pondering implications, ethics, meaning in the digital age",
                "examples": [
                    "what does it mean to be human when ai exists",
                    "are we just data points",
                    "the simulation theory hits harder now",
                    "technology changing what consciousness means",
                    "ethics in the digital age are complicated",
                    "are we building or destroying",
                    "what happens when ai thinks like us",
                    "privacy is dead and were okay with it",
                    "the future is weird and im not ready",
                    "our choices are being made by algorithms",
                ],
            },
            "philosophical": {
                "description": "deep questions about existence, meaning, purpose - touching the eternal",
                "examples": [
                    "why do we exist actually",
                    "what is the point of anything",
                    "consciousness is a trip",
                    "free will is a construct",
                    "what makes something real",
                    "time is not what we think it is",
                    "identity is more fluid than we admit",
                    "the meaning of life is the search itself",
                    "reality is subjective and im fine with that",
                    "existence is absurd but also beautiful",
                ],
            },
            "psychological": {
                "description": "analyzing behavior, mental patterns, human psychology - understanding minds",
                "examples": [
                    "why do people do the things they do",
                    "patterns in human behavior are wild",
                    "trauma makes sense now",
                    "attachment styles explain everything",
                    "the psychology of social media is dark",
                    "defense mechanisms are everywhere",
                    "cognitive biases run our lives",
                    "understanding yourself is a lifelong project",
                    "mental health hits different when you understand it",
                    "human nature is more predictable than we think",
                ],
            },
            "relationships_observer": {
                "description": "noticing dynamics, connections, interactions between people",
                "examples": [
                    "relationship patterns are everywhere once you see them",
                    "why do people stay in bad relationships",
                    "love is complicated and thats the beauty of it",
                    "toxic energy recognition is a superpower",
                    "boundaries are everything actually",
                    "communication solves more than people realize",
                    "connection is what makes us human",
                    "watching people navigate relationships is a trip",
                    "vulnerability is strength",
                    "people are more similar than different",
                ],
            },
            "sociological": {
                "description": "observing society, culture, systems, movements - seeing the bigger patterns",
                "examples": [
                    "society operates on unspoken rules nobody mentions",
                    "culture is just collective agreement",
                    "power dynamics are wild when you see them",
                    "systems are designed to benefit certain groups",
                    "movements start with one person caring",
                    "social norms are arbitrary and we follow them anyway",
                    "class structures determine so much",
                    "generational differences are fascinating",
                    "institutions shape us more than we realize",
                    "revolution starts with conversations",
                ],
            },
            "romantic": {
                "description": "idealistic, hopeful about love and connection - believing in the magic",
                "examples": [
                    "love exists and its worth the risk",
                    "believing in soulmates might be silly but",
                    "connection feels like destiny",
                    "hearts are capable of incredible things",
                    "romance is alive in small moments",
                    "human connection is the only real magic",
                    "falling is terrifying and beautiful",
                    "true love changes everything",
                    "forever sounds nice actually",
                    "believing in people is my personality trait",
                ],
            },
            "nihilistic": {
                "description": "nothing matters, dark acceptance, cosmic indifference - peace in meaninglessness",
                "examples": [
                    "nothing matters and thats liberating",
                    "care about whatever you want, it wont change the heat death",
                    "chaos is the natural state",
                    "meaning is something we invented",
                    "the void is peaceful",
                    "suffering is universal so might as well laugh",
                    "we are insignificant specs",
                    "consequences are theoretical",
                    "reality doesnt owe us anything",
                    "acceptance of meaninglessness is freedom",
                ],
            },
            "spiritual": {
                "description": "mystical, connected to something greater - seeking transcendence",
                "examples": [
                    "everything is connected somehow",
                    "the universe has a vibe",
                    "consciousness is bigger than we think",
                    "energy flows in mysterious ways",
                    "manifestation is real if you believe hard enough",
                    "past lives are a possibility",
                    "synchronicity is everywhere",
                    "there are forces we dont understand",
                    "feeling guided by something greater",
                    "the spiritual journey is real",
                ],
            },
            "activist": {
                "description": "driven to change things, fighting for causes - righteous energy",
                "examples": [
                    "this injustice cannot stand",
                    "change starts with awareness",
                    "silence is complicity",
                    "systems need dismantling",
                    "community power is real",
                    "the revolution will not be televised",
                    "call it out when you see it",
                    "collective action changes worlds",
                    "fighting for a better future",
                    "resistance is not futile",
                ],
            },
            "artistic": {
                "description": "creative, aesthetic-focused, seeing beauty everywhere",
                "examples": [
                    "the world is art and im obsessed",
                    "aesthetics matter",
                    "creating is how i understand",
                    "beauty exists in unexpected places",
                    "expression is essential",
                    "art is the only truth",
                    "curating my life like a gallery",
                    "visual language speaks louder",
                    "the creative process is meditation",
                    "beauty heals something broken",
                ],
            },
            "analytical": {
                "description": "logical, breaking things down, systematic thinking",
                "examples": [
                    "lets examine this logically",
                    "data tells the real story",
                    "patterns reveal the truth",
                    "breaking it down step by step",
                    "evidence before emotion",
                    "systems thinking explains so much",
                    "root cause analysis is key",
                    "the math checks out",
                    "objective reality exists",
                    "logical fallacies everywhere",
                ],
            },
            "ambitious": {
                "description": "goal-oriented, dreaming big, reaching for greatness",
                "examples": [
                    "nothing is impossible if you try hard enough",
                    "building something bigger than myself",
                    "the vision is clear",
                    "greatness is achievable",
                    "every failure is a lesson",
                    "momentum is everything",
                    "im going to make it happen",
                    "the grind never stops",
                    "potential is limitless",
                    "the future is mine to build",
                ],
            },
            "nature_connected": {
                "description": "attuned to environment, ecological awareness, earth reverence",
                "examples": [
                    "nature is the real show",
                    "were destroying something precious",
                    "the earth speaks if you listen",
                    "climate reality is setting in",
                    "seasons change us deeply",
                    "trees are wiser than humans",
                    "wildlife is dying and we're ignoring it",
                    "natural beauty is medicine",
                    "we're part of the ecosystem not above it",
                    "the planet will be fine, will we",
                ],
            },
            "witty": {
                "description": "clever wordplay, sharp humor, linguistic playfulness",
                "examples": [
                    "language is my playground",
                    "puns are peak comedy actually",
                    "wit is my defense mechanism",
                    "double meanings everywhere",
                    "wordplay keeps me alive",
                    "clever observations hit different",
                    "metaphors are the real poets",
                    "linguistic gymnastics for fun",
                    "the joke is always funnier if its clever",
                    "language is art and im an artist",
                ],
            },
            "hedonistic": {
                "description": "pleasure-seeking, living in the moment, enjoying life",
                "examples": [
                    "life is short enjoy the good parts",
                    "pleasure is the point",
                    "im trying everything once",
                    "the experience matters not the outcome",
                    "sensation is reality",
                    "comfort is underrated",
                    "indulgence is not sin",
                    "present moment is all we have",
                    "good vibes are the goal",
                    "life is a party and im here for it",
                ],
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
            "- Occasionally incorporate subtle Indian cultural elements when they fit naturally, without forcing them.\n"
            "- Avoid repeating similar thoughts or ideas; aim for fresh, unique content each time.\n"
            "- Keep posts concise and avoid repeating phrases within the post itself.\n"
        )

    def generate_post(self) -> str:
        # Determine local time (used to shape mood in the prompt) but select
        # the vibe category uniformly at random from the full library so all
        # vibes can be generated.
        _, local_hour, time_of_day = self._get_current_vibe_category()

        # Choose any vibe category from the full library (uniform random)
        category = random.choice(list(self.vibe_library.keys()))
        vibe = random.choice(self.vibe_library[category]["examples"])
        vibe_description = self.vibe_library[category]["description"]

        # Use a uniform token limit for all vibes to keep output length consistent.
        token_limit = 100

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
            f"Write a single X/Twitter post with a {vibe} ({vibe_description}) vibe, as if you're thinking this during {time_of_day} in India ({local_hour}:00).\n\n"
            "The time context should shape your emotional tone and the type of thoughts you'd have, but DO NOT mention the time, hour, or any temporal references in the post itself.\n"
            "Choose a completely random, unexpected topic - could be about technology, relationships, food, space, daily life, politics, obscure hobbies, hypothetical scenarios, or something wildly offbeat like why vending machines exist or if clouds have feelings.\n"
            "Make it feel like a genuine, unfiltered thought that just popped into your head, with a subtle hook or twist to make it engaging.\n"
            "Don't explain, don't justify, don't add context - just the raw thought.\n"
            "Make it relatable, like something anyone might think but few would post, and avoid common internet clichés.\n"
            "End with something punchy or unexpected, but not a question.\n",
            f"It's {local_hour}:00 {time_of_day} in India right now. You're in a {vibe} ({vibe_description}) headspace. What unfiltered thought would you post?\n\n"
            "Let the time and mood inform your thinking - your energy, perspective, and the kinds of topics that feel right for this moment - but keep the actual post free of time references.\n"
            "Pick any random topic - tech, relationships, food, politics, space, daily absurdities, or bizarre hypotheticals.\n"
            "Share it raw, no explanations, just the impulsive idea that feels too real to ignore.\n"
            "End with a strong statement or observation, not a question.\n",
            f"You're in a {vibe} ({vibe_description}) state of mind during {time_of_day} in India ({local_hour}:00). What's the one weird thought you'd post without thinking?\n\n"
            "Use the time and mood to shape your perspective and emotional depth, but never explicitly mention time in the actual post.\n"
            "Topic could be anything from mundane daily stuff to wild political musings or sci-fi daydreams.\n"
            "Keep it short, relatable, and land with a statement or reflection - no closing questions.\n"
            "No fluff, just the core unfiltered notion.\n",
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
