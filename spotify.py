import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json


def main():
    global spotify
    #Getting the client ID and client secret after making them environment varibales
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    client_redirect = os.environ.get('SPOTIPY_REDIRECT_URI')

    #Performing a check to make sure that the environment variables are remembered.
    if client_id is None or client_secret is None:
        print("ERROR: Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT SECRET environment variables")
        return

    #Entering the URI of the playlist
    scope = "playlist-read-private, playlist-modify-private, playlist-modify-public"
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

    playlist1 = spotify.playlist_tracks('37i9dQZF1EJzGGGOWOiITB')
    playlist2 = spotify.playlist_tracks('6CPMN5JBkcD4Sk9vD0OIOA')

    uris = parsep1(playlist1)
    addp2(playlist2, uris)

"""
Input: playlist1
Output: ids
This function serves to parse through a playlist and return all of the song IDs.
"""

def parsep1(playlist1):
    uris = []
    for item in playlist1['items']:
        track = item['track']
        uri = track['uri']
        uris.append(uri)
    return uris

"""
Input: playlist2, ids
Output: None
This function serves to add songs from one playlist to another.
"""

def addp2(playlist2, uris):
    existing_uris = [item['track']['uri'] for item in playlist2['items']]
    uris_to_add = [uri for uri in uris if uri not in existing_uris]
    if uris_to_add:
        spotify.playlist_add_items('6CPMN5JBkcD4Sk9vD0OIOA', uris_to_add)

if __name__ == "__main__":
    main()
    
