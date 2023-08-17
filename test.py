from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Scraping Billboard 100
date = "2001-04-25"
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="a6706a1fa89149af8c447e422a51ec2c",
        client_secret="ba629c8b2d2b40cab370c791cdd61d93",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

"""
#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

#Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("added")
"""