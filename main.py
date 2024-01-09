import spotify
import dash_app

def main():
    # Autheticate with Spotify
    sp = spotify.authenticate_spotify()

    # Fetch user's Spotify library and visualize it
    library = spotify.fetch_spotify_library(sp)
    dash_app.visualize_library(library)
    
    # Fetch user's recently played tracks and visualize them
    recently_played = spotify.fetch_recently_played(sp)
    dash_app.visualize_listening_habits(recently_played)
    
    # Fetch user's top artists and tracks and visualize them
    top_artists, top_tracks = spotify.fetch_top_artists_and_tracks(sp)
    dash_app.visualize_top_artists_and_tracks(top_artists, top_tracks)
    
    # analyze genres of the top artists and visualize them
    genres = spotify.analyze_genres(sp, top_artists)
    dash_app.visualize_genres(genres)

    # Fetch audio features of the top tracks and visualize them
    audio_features = spotify.fetch_audio_features(sp, top_tracks)
    dash_app.visualize_mood_and_attributes(audio_features)
    
    # Analyze diversity of the top artists and tracks and visualize it
    dash_app.visualize_diversity(top_artists, top_tracks)
    
if __name__ == '__main__':
    main()

