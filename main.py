import os
from agents.generate_post_agent import GeneratePostAgent
from agents.x_poster_agent import XPosterAgent

# Create agents
gen_agent = GeneratePostAgent(os.environ['GEMINI_API_KEY'])
poster = XPosterAgent(
    os.environ['TWITTER_BEARER_TOKEN'],
    os.environ['TWITTER_CONSUMER_KEY'],
    os.environ['TWITTER_CONSUMER_SECRET'],
    os.environ['TWITTER_ACCESS_TOKEN'],
    os.environ['TWITTER_ACCESS_TOKEN_SECRET']
)

# Generate and post
post = gen_agent.generate_post()
poster.post(post)