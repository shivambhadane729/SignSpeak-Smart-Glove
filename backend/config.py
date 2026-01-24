import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_NAME = "SignSpeak Backend"
POLL_RATE_HZ = 10
# Secrets
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USE_GEMINI = True
