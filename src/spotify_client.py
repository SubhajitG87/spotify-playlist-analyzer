import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config

class SpotifyClient:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=Config.SPOTIFY_CLIENT_ID,
            client_secret=Config.SPOTIFY_CLIENT_SECRET,
            redirect_uri=Config.SPOTIFY_REDIRECT_URI,
            scope='playlist-read-private user-library-read'
        ))

    def get_user_playlists(self):
        """Get all playlists for the authenticated user"""
        results = self.sp.current_user_playlists()
        return [(playlist['name'], playlist['id']) for playlist in results['items']]

    def get_playlist_tracks(self, playlist_id):
        """Extract all tracks from a playlist"""
        results = self.sp.playlist_tracks(playlist_id)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        return tracks

    def get_audio_features(self, track_ids):
        """Get audio features for multiple tracks"""
        return self.sp.audio_features(track_ids)