from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = "gemini-1.5-flash"
    COLLECTION_NAME = "omniagent_memory"
    MAX_ITERATIONS = 10

settings = Settings()