import os
import logging
from agents.generate_post_agent import GeneratePostAgent
from agents.x_poster_agent import XPosterAgent

logging.basicConfig(level=logging.INFO)

# Create agents
gen_agent = GeneratePostAgent(os.environ['GEMINI_API_KEY'])
poster = XPosterAgent()

# Generate and post
post = gen_agent.generate_post()
poster.post(post)