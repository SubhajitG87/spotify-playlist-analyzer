from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

    # HuggingFace Inference API (for open-source LLM access)
    # Get a free token at https://huggingface.co/settings/tokens
    HF_API_KEY = os.getenv('HF_API_KEY')

    # Customizable parameters
    # Open-source LLM model via HuggingFace Inference API
    # Examples:
    #   - "mistralai/Mistral-7B-Instruct-v0.2" (good quality, ~13GB GPU)
    #   - "google/flan-t5-large" (text-to-text, CPU-friendly)
    #   - "HuggingFaceH4/zephyr-7b-beta" (instruction-tuned)
    #   - "bigscience/bloom-560m" (very small, fast)
    LLM_MODEL = os.getenv('LLM_MODEL', "google/flan-t5-large")
    ANALYSIS_BATCH_SIZE = 100  # Number of songs to analyze in one batch
    MOOD_CATEGORIES = ['happy', 'sad', 'energetic', 'calm', 'neutral']
    DASHBOARD_PORT = 8050
    DEBUG_MODE = True