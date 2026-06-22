import logging
import re
import requests
from config import Config

logger = logging.getLogger(__name__)

HF_API_BASE = "https://api-inference.huggingface.co/models"
REQUEST_TIMEOUT = 30  # seconds


class LLMAnalyzer:
    """Analyzes song moods and generates playlist insights using a hosted open-source LLM
    via the HuggingFace Inference API."""

    def __init__(self):
        self.model = Config.LLM_MODEL
        self.api_key = Config.HF_API_KEY
        self.api_url = f"{HF_API_BASE}/{self.model}"

        if not self.api_key:
            logger.warning(
                "HF_API_KEY is not set. HuggingFace Inference API will not be authenticated "
                "(rate limits apply). Set it in your .env file."
            )

        logger.info("Using HuggingFace model: %s", self.model)

    def _call_hf_api(self, prompt: str, max_new_tokens: int = 10) -> str:
        """Send a prompt to the HuggingFace Inference API and return the generated text."""
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "do_sample": False,
                "return_full_text": False,
            }
        }

        try:
            resp = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT
            )
            resp.raise_for_status()
            data = resp.json()

            # Handle both list and dict responses
            if isinstance(data, list) and len(data) > 0:
                return data[0].get("generated_text", "").strip()
            elif isinstance(data, dict):
                return data.get("generated_text", "").strip()
            return ""
        except requests.HTTPError as e:
            if resp.status_code == 503:
                logger.warning("Model is loading on HuggingFace servers (503). Retry later.")
            elif resp.status_code == 429:
                logger.warning("Rate limited by HuggingFace API (429). Consider adding an API key.")
            else:
                logger.error("HuggingFace API HTTP error %s: %s", resp.status_code, e)
            return ""
        except requests.Timeout:
            logger.warning("HuggingFace API request timed out after %ss", REQUEST_TIMEOUT)
            return ""
        except Exception as e:
            logger.error("HuggingFace API request failed: %s", e)
            return ""

    def analyze_song_mood(self, song_name: str, artist: str) -> str:
        """Analyze song mood using the hosted LLM.

        Returns a single mood word from Config.MOOD_CATEGORIES.
        Returns 'neutral' if classification fails.
        """
        categories = ", ".join(Config.MOOD_CATEGORIES)
        prompt = (
            f"Classify the mood of the song '{song_name}' by {artist} "
            f"into one word from this list: {categories}. "
            f"Answer with the single mood word only."
        )
        raw = self._call_hf_api(prompt, max_new_tokens=8)
        text = raw.lower().strip(' "\'.,;!?\n-')

        logger.debug("Mood raw output for '%s': '%s'", song_name, text)

        # Try exact match against mood categories
        for mood in Config.MOOD_CATEGORIES:
            if mood == text:
                return mood

        # Try word-boundary search
        for mood in Config.MOOD_CATEGORIES:
            if re.search(r'\b' + re.escape(mood) + r'\b', text):
                return mood

        # Partial match fallback (first 4 chars)
        for mood in Config.MOOD_CATEGORIES:
            if len(mood) >= 4 and mood[:4] in text:
                return mood

        logger.debug("No mood match found (raw='%s'), returning 'neutral'", text)
        return "neutral"

    def generate_playlist_insights(self, stats: dict) -> str:
        """Generate overall playlist insights using the hosted LLM."""
        prompt = (
            f"Analyze this Spotify playlist:\n"
            f"- {stats['total_songs']} songs\n"
            f"- Average popularity: {stats['avg_popularity']:.1f}/100\n"
            f"- Average energy: {stats['avg_energy']:.2f}\n"
            f"- Average danceability: {stats['avg_danceability']:.2f}\n"
            f"- Top artist: {stats['top_artist']}\n\n"
            "Provide 3 short, unique insights about this music taste."
        )
        raw = self._call_hf_api(prompt, max_new_tokens=150)
        if raw:
            return raw
        return "Unable to generate insights at this time."