import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.dash(__name__, external_stylesheets=external_stylesheets)

# DEFINE LAYOUT OF APP
app.layout = html.Div([
    html.H1("Spotify Data Visualization"),
    html.Div([
        html.Div([
            dcc.Graph(id='library-graph', className='container'),
            dcc.Graph(id='listening-habits-graph', className='container')
        ], className="three columns"),
    
        html.Div([
            dcc.Graph(id='top-artists-graph', className='container'),
            dcc.Graph(id='top-tracks-graph', className='container')
        ], className="three columns"),
    
        html.Div([
            dcc.Graph(id='genres-graph', className='container'),
            dcc.Graph(id='mood-graph', className='container')
        ], className="three columns"),
    
        html.Div([
            dcc.Graph(id='artist-diversity-graph', className='container'),
            dcc.Graph(id='track-diversity-graph', className='container'),
        ], className="three columns"),
    ], className="row")
])


# Define a function to update each graph
@app.callback(
    Output('ibrary-graph', 'figure'),
    [input('library', 'data')]
)
def update_library_graph(data):
    return process_library_data(data)
@app.callback(
    Output('listening-habits-graph', 'figure'),
    [Input('recently_played', 'data')]
)
def update_listening_habits_graph(data):
    return process_recently_played_data(data)

@app.callback(
    Output('top-artists-graph', 'figure'),
    [Input('top_artists', 'data'), Input('top_tracks', 'data')]
)
def update_top_artists_graph(top_artists, top_tracks):
    return process_top_artists_and_tracks(top_artists, top_tracks)[0]

@app.callback(
    Output('top-tracks-graph', 'figure'),
    [Input('top_artists', 'data'), Input('top_tracks', 'data')]
)
def update_top_tracks_graph(top_artists, top_tracks):
    return process_top_artists_and_tracks(top_artists, top_tracks)[1]

@app.callback(
    Output('genres-graph', 'figure'),
    [Input('genres', 'data')]
)
def update_genres_graph(data):
    return process_genres_data(data)

@app.callback(
    Output('mood-graph', 'figure'),
    [Input('audio_features', 'data')]
)
def update_mood_graph(data):
    return process_audio_features_data(data)

@app.callback(
    Output('artist-diversity-graph', 'figure'),
    [Input('top_artists', 'data'), Input('top_tracks', 'data')]
)
def update_artist_diversity_graph(top_artists, top_tracks):
    return process_diversity_data(top_artists, top_tracks)[0]

@app.callback(
    Output('track-diversity-graph', 'figure'),
    [Input('top_artists', 'data'), Input('top_tracks', 'data')]
)
def update_track_diversity_graph(top_artists, top_tracks):
    return process_diversity_data(top_artists, top_tracks)[1]

# RUN THE APP
if __name__ == '__main__':
    app.run_server(debug=True)

"""
    START: LIBRARY SECTION
"""
def process_library_data(library):
    """
    Process the library data to prepare for visualization
    
    Args:
        library: List of songs in user's spotify library
        
    Returns:
        A plotly figure
    """
    
    # count number of tracks per artist
    artist_counts={}
    for song in library:
        artist = song['track']['artist'][0]['name']
        if artist not in artist_counts:
            artist_counts[artist] = 0
        artist_counts[artist] += 1

    # create a bar chart
    fig = go.Figure(data=go.Bar(x=list(artist_counts.keys()), y=list(artist_counts.values()))) 
    
    # set chart title and labels
    fig.update_layout(title_text='Number of Tracks per Artist', xaxis_title='Artist', yaxis_title='Number of Tracks')
    
    return fig

def visualize_library(library):
    
    # Process library data for visualization
    data = process_library_data(library)
    
    # Define app layout
    app.layout = html.div([
        html.h1("Spotify Library Overview"),
        dcc.Grahp(id='library-graph', figure=data)
    ])
    
"""
    END: LIBRARY SECTION
"""


"""
    START: RECENTLY PLAYED SECTION
"""
def process_recently_played_data(recently_played):
    """
        Process reccently played data for visualization
        
        Args:
            recently_played: A list of recently played tracks with their play time
        
        Returns:
            A plotly figure
    """
    
    # Convert data to a DataFrame
    df = pd.DataFrame(recently_played)
    
    # convert the 'played_at' column to datetime
    df['played_at'] = pd.to_datetime(df['played_at'])
    
    # Count number of tracks played each day
    df['date'] = df['played_at'].dt.date
    daily_counts = df['date'].value_counts().sort_index()
    
    # create line graph
    fig = go.Figure(data=go.Scatter(x=daily_counts.index, y=daily_counts.values, mode='lines'))
    
    # set chart title and labels
    fig.update_layout(title_text='Listening Habits Over Time', xaxis_title='Date', yaxis_title='Number of Tracks Played')
    
    return fig

def visualize_listening_habits(recently_played):
    # process recently played data for visualization
    data = process_recently_played_data(recently_played)
    
    # define app layout
    app.layout  = html.Div([
        html.H1("Listening Habits Over Time"),
        dcc.Graph(id='listening-habits-graph', figure=data)
    ])

"""
    END: RECENTLY PLAYED SECTION
"""


"""
    START: TOP ARTIST AND TRACKS SECTION
"""
def process_top_artists_and_tracks(top_artists, top_tracks):
    """
    Processes the top artists and tracks data for visualization
    
    Args:
        top_artists: A list of top artists
        top_tracks: A list of top tracks 
    Returns:
        A tuple of two plotly figures
    """
    
    # Count number of tracks per artist
    artist_counts = {}
    for track in top_tracks:
        artist = track['artist']
        if artist not in artist_counts:
            artist_counts[artist] = 0
        artist_counts[artist] += 1
        
    # create a bar chart for top artists
    artists_fig = go.Figure(data=go.Bar(x=list(artist_counts.keys()), y=list(artist_counts.values())))
    
    # set chart title and labels for top artists
    artists_fig.update_layout(title_text='Top Artists', xaxis_title='Artist', yaxis_title='Number of tracks')
    
    # count the number of times each track appears
    track_counts = {}
    for track in top_tracks:
        track_name = track['name']
        if track_name not in track_counts:
            track_counts[track_name] = 0
        track_counts[track_name] += 1
        
    # create a bar chart for top tracks
    tracks_fig = go.Figure(data=go.Bar(x=list(track_counts.keys()), y=list(track_counts.values())))
    
    return artists_fig, tracks_fig

def visualize_top_artists_and_tracks(top_artists, top_tracks):
    """
    Visualize top artists and tracks
    """

    # process top artists and tracks data for visualization
    artists_fig, tracks_fig = process_top_artists_and_tracks(top_artists, top_tracks)
    
    # define app layout
    app.layout = html.Div([
        html.H1("Top Artists and Tracks"),
        dcc.Graph(id='top-artists-graph', figure=artists_fig),
        dcc.Graph(id='top-tracks-graph', figure=tracks_fig)
    ])
"""
    END: TOP ARTISTS AND TRACKS SECTION
"""
    
"""
    START: GENRES SECTION
"""
def process_genres_data(genres):
    """
    Processes the genres data for visualization
    
    Args:
        genres: A dictionary with artist names as keys and list of genres as values
    Returns:
        A plotly figure
    """
    
    # Count number of artists per genre
    genre_counts = {}
    for artist, artist_genres in genres.items():
        for genre in artist_genres:
            if genre not in genre_counts:
                genre_counts[genre] = 0
            genre_counts[genre]+=1
            
    # create a bar chart
    fig = go.Figure(data=go.Bar(x=list(genre_counts.keys()), y=list(genre_counts.values())))
    
    # set chart title and lables
    fig.update_layout(title_text='Number of Artist per Genre', xaxis_title='Genre', yaxis_title='Number of Artists')
    
    return fig

def visualize_genres(genres):
    # process genres data for visualization
    
    data = process_genres_data(genres)
    
    # Define app layout
    app.layout = html.Div([
        html.H1("Genre Analysis"),
        dcc.Graph(id='genres-graph', figure=data)
    ])
"""
    END: GENRES SECTION
"""

"""
    START: AUDIO FEATURES SECTION
"""
def process_audio_features_data(audio_features):
    """
    Process the audio features to prepare for visualization
    
    Args:
        audio_features: a dictionary with track names as keys and audio features as values
        
    Returns:
        A plotly figure
    """
    
    # Extract the energy and valence for each track
    energy = [features['energy'] for features in audio_features.values()]
    valence = [features['valence'] for features in audio_features.values()]
    tracks = list(audio_features.keys())
    
    # Create a scatter plot
    fig = go.Figure(data=go.Scatter(x=energy, y=valence, mode='markers', text=tracks))
    
    # Set chart title and labels
    fig.update_layout(title_text='Mood and Attributes of Music', xaxis_title='Energy', yaxis_title='Valence')
    
    return fig

def visualize_mood_and_attributes(audio_features):
    # Process the audio features data for visualization
    data = process_audio_features_data(audio_features)
    
    # Define app layout
    app.layout = html.Div([
        html.H1("Mood and Attributes of Music"),
        dcc.Graph(id='mood-graph', figure=data)
    ])
    
    #TODO: run app
"""
    END: AUDIO FEATURES SECTION
"""

"""
    START: DIVERSITY SECTION
"""
def process_diversity_data(top_artists, top_tracks):
    """
    Processes the diversity data for visualization
    
    Args:
        top_artists: list of top artists
        top_tracks: list of top tracks
        
    Returns:
        A tuple of two plotly figures
    """
    
    #count number of tracks per artist
    artist_counts = {}
    for track in top_tracks:
        artist = track['artist']
        if artist not in artist_counts:
            artist_counts[artist] = 0
        artist_counts[artist] += 1

    # create a bar chart for artist diversity
    artists_fig = go.Figure(data=go.Bar(x=list(artist_counts.keys()), y=list(artist_counts.values())))
    
    # set chart title and labels for artist diversity
    artists_fig.update_layout(title_text='Artist Diversity', xaxis_title='Artist', yaxis_title='Number of Tracks')
    
    # count number of times each track appears
    track_counts = {}
    for track in top_tracks:
        track_name = track['name']
        if track_name not in track_counts:
            track_counts[track_name] = 0
        track_counts[track_name] += 1
    
    # create bar chart for track diversity
    tracks_fig = go.Figure(data=go.Bar(x=list(track_counts.keys()), y=list(track_counts.values())))

    # set chart title and labels for track diversity
    tracks_fig.update_layout(title_text='Track Diversity', xaxis_title='Track', yaxis_title='Play Count')
    
    return artists_fig, tracks_fig

def visualize_diversity(top_artists, top_tracks):
    # Process the top artists and tracks data for visualization
    artists_fig, tracks_fig = process_diversity_data(top_artists, top_tracks)
    
    # Define app layout
    app.layout = html.Div([
        html.H1("Listening Diversity"),
        dcc.Graph(id='artist-diversity-graph', figure=artists_fig),
        dcc.Graph(id='track-diveristy-graph', figure=tracks_fig)
    ])