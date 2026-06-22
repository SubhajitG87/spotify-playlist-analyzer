import pandas as pd
from datetime import datetime
from config import Config

class DataAnalyzer:
    def __init__(self, spotify_client):
        self.spotify_client = spotify_client

    def analyze_playlist(self, playlist_id):
        """Analyze playlist and extract key metrics"""
        tracks = self.spotify_client.get_playlist_tracks(playlist_id)
        
        track_data = []
        track_ids = []
        
        for track in tracks:
            if track['track']:  # Check if track exists
                track_info = track['track']
                track_ids.append(track_info['id'])
                
                track_data.append({
                    'name': track_info['name'],
                    'artist': track_info['artists'][0]['name'],
                    'album': track_info['album']['name'],
                    'release_date': track_info['album']['release_date'],
                    'popularity': track_info['popularity'],
                    'duration_ms': track_info['duration_ms'],
                })

        # Get audio features in batches
        audio_features = []
        for i in range(0, len(track_ids), Config.ANALYSIS_BATCH_SIZE):
            batch = track_ids[i:i + Config.ANALYSIS_BATCH_SIZE]
            audio_features.extend(self.spotify_client.get_audio_features(batch))

        # Combine track data with audio features
        for i, track in enumerate(track_data):
            if audio_features[i]:
                track.update({
                    'danceability': audio_features[i]['danceability'],
                    'energy': audio_features[i]['energy'],
                    'key': audio_features[i]['key'],
                    'loudness': audio_features[i]['loudness'],
                    'mode': audio_features[i]['mode'],
                    'speechiness': audio_features[i]['speechiness'],
                    'acousticness': audio_features[i]['acousticness'],
                    'instrumentalness': audio_features[i]['instrumentalness'],
                    'liveness': audio_features[i]['liveness'],
                    'valence': audio_features[i]['valence'],
                    'tempo': audio_features[i]['tempo']
                })
        
        return pd.DataFrame(track_data)