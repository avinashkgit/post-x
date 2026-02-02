import os
import logging
from agents.generate_post_agent import GeneratePostAgent
from agents.x_poster_agent import XPosterAgent

logging.basicConfig(level=logging.INFO)

print("🚀 Starting X Post Bot...")

# Create agents
print("🤖 Initializing unified AI content generator...")
gen_agent = GeneratePostAgent(os.environ["GEMINI_API_KEY"], debug=True)

print("🐦 Initializing X poster...")
poster = XPosterAgent()

# Generate and post
print("✍️  Generating engaging post...")
post = gen_agent.generate_post()
print(f"📝 Generated post: {post}")

print("📤 Posting to X...")
try:
    result = poster.post(post)
    print("✅ Post successful!")
except RuntimeError as e:
    print(f"❌ Post failed: {e}")
    raise  # Re-raise to fail the workflow

print("🎉 Bot execution complete.")
