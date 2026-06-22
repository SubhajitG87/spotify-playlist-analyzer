# Spotify Playlist Analyzer

An advanced Python application that analyzes Spotify playlists using the Spotify API and an open-source LLM (via HuggingFace Inference API) to generate insights and interactive dashboards.

## Features
- Fetches detailed track information from Spotify playlists
- Analyzes audio features using Spotify's API
- Uses an open-source LLM to analyze song moods and generate playlist insights
- Creates interactive dashboards with various metrics and visualizations
- Real-time data visualization

## Prerequisites
- Python 3.8+
- [Spotify Developer Account](https://developer.spotify.com/dashboard) (for API credentials)
- [HuggingFace Account](https://huggingface.co/join) (for a free API token to access open-source LLMs)
- Git (for cloning/publishing)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/spotify-playlist-analyzer.git
   cd spotify-playlist-analyzer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API credentials**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and fill in your credentials:
   - `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` from your Spotify Developer Dashboard
   - `HF_API_KEY` from [HuggingFace Settings](https://huggingface.co/settings/tokens)

## Configuration

Key settings in `config.py` (or overridable via `.env`):

| Setting | Default | Description |
|---------|---------|-------------|
| `LLM_MODEL` | `google/flan-t5-large` | HuggingFace model for mood/insight analysis |
| `ANALYSIS_BATCH_SIZE` | `100` | Number of songs analyzed in one API batch |
| `MOOD_CATEGORIES` | `['happy', 'sad', 'energetic', 'calm', 'neutral']` | Available mood categories |
| `DASHBOARD_PORT` | `8050` | Port for the dashboard server |
| `DEBUG_MODE` | `True` | Toggle debug logging |

**Note:** No GPU or local model download is required – the LLM runs remotely via the HuggingFace Inference API.

## Usage

1. **Run the application**
   ```bash
   python src/main.py
   ```

2. Select a playlist from the displayed list
3. Wait for the AI analysis to complete (depends on playlist size)
4. Access the interactive dashboard at [http://localhost:8050](http://localhost:8050)

## Project Structure

```
spotify-playlist-analyzer/
├── .env.example          # Environment variable template
├── .github/workflows/    # GitHub Actions CI
├── config.py             # Application configuration
├── requirements.txt      # Python dependencies
├── README.md
└── src/
    ├── main.py           # Entry point
    ├── spotify_client.py # Spotify API wrapper
    ├── data_analyzer.py  # Track data extraction & processing
    ├── llm_analyzer.py   # LLM mood & insight analysis (HuggingFace API)
    └── dashboard.py      # Plotly/Dash interactive dashboard
```

## Deploying to GitHub

1. **Create a new repository on GitHub** (do NOT initialize with README/`.gitignore`).

2. **Push your local code**
   ```bash
   git remote add origin git@github.com:your-username/spotify-playlist-analyzer.git
   git branch -M main
   git push -u origin main
   ```

3. **GitHub Actions** will automatically run CI (linting, syntax check, import tests) on every push.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [HuggingFace Inference API](https://huggingface.co/docs/api-inference/index)
- [Dash](https://dash.plotly.com/) by Plotly