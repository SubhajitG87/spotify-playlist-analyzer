from dash import Dash, dcc, html
import plotly.express as px
from config import Config

class Dashboard:
    def __init__(self):
        self.app = Dash(__name__)

    def create_layout(self, df, insights):
        """Create interactive dashboard layout"""
        self.app.layout = html.Div([
            html.H1("Spotify Playlist Analysis Dashboard"),
            
            html.Div([
                html.H3("AI-Generated Insights"),
                html.P(insights)
            ]),
            
            dcc.Graph(
                figure=px.scatter(df, x='energy', y='valence',
                                color='mood', hover_data=['name', 'artist'],
                                title='Song Energy vs Valence by AI-Detected Mood')
            ),
            
            dcc.Graph(
                figure=px.box(df, y=['danceability', 'energy', 'valence'],
                             title='Distribution of Musical Features')
            ),
            
            dcc.Graph(
                figure=px.histogram(df, x='release_date', 
                                  title='Song Release Timeline',
                                  color='mood')
            ),
            
            html.Div([
                html.H3("Mood Distribution"),
                dcc.Graph(
                    figure=px.pie(df, names='mood', 
                                title='Distribution of AI-Detected Moods')
                )
            ])
        ])

    def run(self):
        """Run the dashboard server"""
        self.app.run_server(debug=Config.DEBUG_MODE, port=Config.DASHBOARD_PORT)