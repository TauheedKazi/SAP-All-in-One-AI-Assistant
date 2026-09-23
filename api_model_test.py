import os
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Fetch active models
models = client.models.list()

print("Available Models on your Groq Key:\n")
for model in models.data:
    print(f"• ID: {model.id}")