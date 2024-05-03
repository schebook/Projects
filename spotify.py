import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

"""
Input: None
Output: spotify
This function authetnicates with Spotify and returns the authenticated value.
"""

def authenticate():
    try:
        #Getting the client ID and client secret after making them environment variables
        client_id = os.environ.get("SPOTIPY_CLIENT_ID")
        client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
        client_redirect = os.environ.get("SPOTIPY_REDIRECT_URI")

        #Performing a check to make sure the environment variables are remembered
        if client_id is None or client_secret is None or client_redirect is None:
            print("ERROR: Set SPOTIPY_CLIENT_ID, SPOTIPY_REDIRECT_URL and SPOTIPY_CLIENT SECRET environment variables")
            return None
        
        #Entering the URI of the playlist
        scope = "playlist-read-private, playlist-modify-private, playlist-modify-public"
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=client_redirect, scope=scope))

        return spotify
    
    except spotipy.oauth2.SpotifyOauthError as auth_error:
        print(f"Authentication error: {auth_error}")
    except spotipy.SpotifyException as spotify_error:
        print(f"Spotify API Error: {spotify_error}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")

"""
Input: spotify, playlist_id, handle_pagination
Output: ids
This function serves to parse through a playlist and return all of the song IDs.
There should only be 50 songs at any given time, so no need to make a while loop.
"""

def parse_playlist(spotify, playlist_id, handle_pagination = True):
    try:
        tracks = []
        results = spotify.playlist_tracks(playlist_id)
        tracks.extend(item['track']['uri'] for item in results['items'])

        while handle_pagination and results['next']:
            results = spotify.next(results)
            tracks.extend(item['track']['uri'] for item in results['items'])
        
        return tracks
    except Exception as e:
        print(f"An unexpected error occured: {e}")


"""
Input: spotify, playlist_id
Output: None
This serves to remove all duplicates within a playlist with a set. There is a better way to do this for sure. 
"""
def removeDupes(spotify, playlist_id):
    try:
        tracks_uris = parse_playlist(spotify, playlist_id, handle_pagination=True)
        unique_uris = []
        seen_uris = set()

        for uri in tracks_uris:
            if uri not in seen_uris:
                unique_uris.append(uri)
                seen_uris.add(uri)

        spotify.playlist_replace_items(playlist_id, unique_uris)
    except Exception as e:
        print(f"An unexpected error occured: {e}")


"""
Input: spotify, source_playlist, target_playlist
Output: None
This function takes in a source and target playlist ID. It then adds the songs to the playlist if they are not already in it.
"""
def addTracks(spotify, source_playlist, target_playlist):
    source_tracks = parse_playlist(spotify, source_playlist, handle_pagination=True )
    target_tracks = parse_playlist(spotify, target_playlist, handle_pagination=True)

    tracks_to_add = []
    for tracks in source_tracks:
        if tracks not in target_tracks:
            tracks_to_add.append(tracks)
    
    if tracks_to_add:
        try:
            spotify.playlist_add_items(target_playlist, tracks_to_add)
        except Exception as e:
            print(f"An unexpected error has occured: {e}")


def main():
    spotify = authenticate()
    if not spotify:
        print("Failed to authenticate with Spotify")
        return
    
    source_playlist_id = "37i9dQZF1EJzGGGOWOiITB"
    target_playlist_id = "6CPMN5JBkcD4Sk9vD0OIOA"

    #Adding tracks from the source playlist to the target playlist.
    addTracks(spotify, source_playlist_id, target_playlist_id)
    


if __name__ == "__main__":
    main()
