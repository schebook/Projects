import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json

#Getting the client ID and client secret after making them environment varibales
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
client_redirect = os.environ.get('SPOTIPY_REDIRECT_URI')

#Performing a check to make sure that the environment variables are remembered.
if client_id is None or client_secret is None:
    print("ERROR: Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT SECRET environment variables")

#Entering the URI of the playlist
playlist_uri = "spotify:playlist:37i9dQZF1EJzGGGOWOiITB"
scope = "playlist-read-private, playlist-modify-private, playlist-modify-public"
spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scope))

playlist1 = spotify.playlist_tracks('37i9dQZF1EJzGGGOWOiITB')
playlist2 = spotify.playlist_tracks('6CPMN5JBkcD4Sk9vD0OIOA')

# print(json.dumps(playlist2, indent=4))

for items in playlist2['items']:
    track_id = items['track']['id']
    print(id)
