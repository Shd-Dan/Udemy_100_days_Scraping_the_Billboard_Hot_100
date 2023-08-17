import ast
import os
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify_id = os.environ.get("SPOT_CLIENT_ID")
spotify_cs = os.environ.get("SPOT_CLIENT_SECRET")
APP_REDIRECT_URI = "http://example.com"

# input_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
date = "2001-04-25"
URL = f"https://www.billboard.com/charts/hot-100/{date}"

# Getting data from the website
response = requests.get(url=URL)
hot_100_page = response.text

soup = BeautifulSoup(hot_100_page, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

"""Spotify Authentication"""
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_id,
                                               client_secret=spotify_cs,
                                               redirect_uri="http://example.com",
                                               state=None,
                                               scope="playlist-modify-private",
                                               cache_path="token.txt",
                                               username="ShD",
                                               proxies=None,
                                               show_dialog=True,
                                               requests_session=True,
                                               requests_timeout=None))
user = sp.current_user()
user_id = user["id"]

with open("token.txt", "r") as file:
    data = file.read()

token_acc = ast.literal_eval(data)['access_token']  # convert token.txt inside data to dictionary
sp = spotipy.Spotify(auth=token_acc)

# Getting URIs of songs
URIs = []
for name in song_names:
    data = sp.search(q=name, type="track")
    try:
        result = data['tracks']['items'][0]['album']['artists'][0]['uri']
        URIs.append(result)
    except IndexError:
        print(f"{name} doesn't exist in Spotify. Skipped.")
print(URIs)
test_URI = ["3qwGe91Bz9K2T8jXTZ815W"]

# New playlist in spotify
spotify_playlist = sp.user_playlist_create(user=user_id,
                                           name=f"{date} Billboard 100",
                                           public=False)


# Adding list of songs to playlist
sp.playlist_add_items(playlist_id=spotify_playlist['id'], items=test_URI)

playlist_address = f"https://open.spotify.com/playlist/{spotify_playlist['id']}"
print(playlist_address)