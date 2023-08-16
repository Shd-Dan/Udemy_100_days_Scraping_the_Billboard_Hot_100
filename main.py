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

date = "2001-04-25"
URL = f"https://www.billboard.com/charts/hot-100/{date}"
# Getting data from the website
response = requests.get(url=URL)
hot_100_page = response.text

soup = BeautifulSoup(hot_100_page, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
song_test = song_names[0]

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
# print(user_id)

with open("token.txt", "r") as file:
    data = file.read()

token_acc = ast.literal_eval(data)['access_token']

sp = spotipy.Spotify(auth=token_acc)
results = sp.search(q=song_test, type="track")
pprint(results)