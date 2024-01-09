# File for Spotify
import spotipy 
from spotipy.oauth2 import SpotipyOAuth

def authenticate_spotify():
    #Authenticates with Spotify and returns a spotify client
    
    # TODO: replace these with the actual Spotify credentials
    client_id = "your_spotify_client_id"
    client_secret = "your_spotify_client_secret"
    redirect_uri = "your_spotify_redirect_uri"
    scope = "user-library-read"
    
    # Create instance of SpotifyOAuth
    
    auth_manager = SpotipyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    return sp

def fetch_spotify_library(sp):
    """
    Fetches user's spotify library.
    
    Args:
        sp: A Spotify Client
    
    Returns:
        A list of songs in the user's Spotify library.
    """
    # Fetch first page of user's library
    results = sp.current_user_saved_tracks()
    
    # Extract songs from first page
    songs = results['items']
    
    # While there are more pages, fetch the next page and add its songs to the list
    while results['next']:
        results = sp.next(results)
        songs.extend(results['items'])
        
    # Return the list of songs
    return songs

def fetch_recently_played(sp):
    """
    Fetches the user's recently played songs from Spotify.
    
    Args:
        sp: A Spotify Client
    
    Returns:
        A list of the user's recently played songs.
    """
    # Fetch first page of user's recently played songs
    results = sp.current_user_recently_played()
    
    # Extract tracks and play time
    tracks = [{'played_at': item['played_at'], 'track': item['track']} for item in results['items']]
    
    # Return the list of tracks
    return tracks

def fetch_top_artist_and_tracks(sp):
    """
    Fetches the user's top artists and tracks from Spotify.
    
    Args:
        sp: A Spotify Client
    
    Returns:
        A tuple containing two lists: top artists and top tracks
    """

    # Fetch top artists and tracks
    top_artists = sp.current_user_top_artists()
    top_tracks = sp.current_user_top_tracks()
    
    # Extract artist and track info
    top_artists = [artist['name'] for artist in top_artists['items']]
    top_tracks = [{'name': track['name'], 'artist': track['artists'][0]['name']} for track in top_tracks['items']]
    
    return top_artists, top_tracks

def analyze_genres(sp, top_artists):
    """
    Analyzes the genres of the user's top artists.
    
    Args:
        sp: A Spotify Client
        top_artists: A list of the user's top artists
    
    Returns:
        A dictionary with artist names as keys and list of genres as values
    """
    
    # Dictionary to store genres
    genres = {}
    
    # For each artist, fetch their genres and add to genres
    for artist in top_artists:
        results = sp.search(q='artist:' + artist, type='artist')
        artist_info = results['artists']['items'][0]
        genres[artist] = artist_info['genres']
        
    return genres

def fetch_audio_features(sp, top_tracks):
    """
    
    Fetches audio features for top tracks
    
    Args:
        sp: a spotify client
        top_tracks: list of top tracks
    
    Returns:
        A dictionary with track names as key and audio features as values
    """
    
    # Dictionary to store audio features
    audio_features = {}
    
    # For each track, fetch its audio features and add to audio_features
    for track in top_tracks:
        results = sp.search(q='track:' + track['name'], type='track')
        track_id = results['tracks']['items'][0]['id']
        features = sp.audio_features([track_id])[0]
        audio_features[track['name']] = features
    
    return audio_features

def analyze_diversity(top_artists, top_tracks):
    """
        Analyzes the diversity of the top artists and tracks
        
        Args:
            top_artists: A list of top artists
            top_tracks: A list of top tracks
            
        Returns:
            A tuple containing two integers: the number of unique artists and tracks
    """
    
    # Calculate number of unique artists and tracks
    num_artists = len(set(top_artists))
    num_tracks = len(set([track['name'] for track in top_tracks]))
    
    return num_artists, num_tracks