import logging
from config import Config
from spotify_client import SpotifyClient
from data_analyzer import DataAnalyzer
from llm_analyzer import LLMAnalyzer
from dashboard import Dashboard

logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG_MODE else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Run the Spotify Playlist Analyzer pipeline."""
    # Initialize components
    logger.info("Initializing Spotify Playlist Analyzer...")
    spotify_client = SpotifyClient()
    data_analyzer = DataAnalyzer(spotify_client)
    llm_analyzer = LLMAnalyzer()
    dashboard = Dashboard()

    # Get user's playlists
    logger.info("Fetching user playlists...")
    playlists = spotify_client.get_user_playlists()

    if not playlists:
        print("No playlists found. Make sure your account has playlists and the token has correct scopes.")
        return

    # Display available playlists
    print("\nAvailable playlists:")
    for i, (name, _) in enumerate(playlists):
        print(f"  {i+1}. {name}")

    # Get user input for playlist selection
    try:
        playlist_index = int(input("\nEnter the number of the playlist to analyze: ")) - 1
        if playlist_index < 0 or playlist_index >= len(playlists):
            print(f"Invalid selection. Please enter a number between 1 and {len(playlists)}.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    selected_playlist = playlists[playlist_index][1]
    logger.info("Analyzing playlist: %s", playlists[playlist_index][0])

    # Analyze playlist data
    df = data_analyzer.analyze_playlist(selected_playlist)

    if df.empty:
        print("No track data could be retrieved for this playlist.")
        return

    # Analyze mood for each song
    print(f"Analyzing mood for {len(df)} songs with AI (this may take a while)...")
    df['mood'] = df.apply(
        lambda x: llm_analyzer.analyze_song_mood(x['name'], x['artist']),
        axis=1
    )

    # Generate playlist insights
    stats = {
        'total_songs': len(df),
        'avg_popularity': df['popularity'].mean(),
        'avg_energy': df['energy'].mean(),
        'avg_danceability': df['danceability'].mean(),
        'top_artist': df['artist'].mode()[0] if not df['artist'].mode().empty else "N/A"
    }
    logger.debug("Playlist stats: %s", stats)
    insights = llm_analyzer.generate_playlist_insights(stats)

    # Create and display dashboard
    print("\n" + "=" * 60)
    print("AI-Generated Playlist Insights:")
    print(insights)
    print("=" * 60 + "\n")

    dashboard.create_layout(df, insights)
    print(f"Dashboard is running on http://localhost:{Config.DASHBOARD_PORT}")
    dashboard.run()


if __name__ == "__main__":
    main()