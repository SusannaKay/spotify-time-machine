import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint


load_dotenv('.env')
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
redirect_uri = os.environ.get('redirect_uri')
scope="playlist-modify-private"

USER_ENDPOINT = 'https://api.spotify.com/v1/me'
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret,redirect_uri=redirect_uri,scope=scope,cache_path='.cache')
sp = spotipy.Spotify(auth_manager=auth_manager)

user_id = sp.current_user()['id']


date= input('Which year do you want to travel to? type in YYYY-MM-DD format ')


URL = f'https://www.billboard.com/charts/hot-100/{date}'

response = requests.get(URL)
website = response.text

soup = BeautifulSoup(website,'html.parser')

titles = soup.select('li ul li h3')

songs_list =[title.getText().strip() for title in titles]
year = date.split("-")[0]

uri_list = []
for song in songs_list:
    song_uri = sp.search(q=f"track:{song} year:{year}", type="track")
    print(song_uri)
    try:
        uri = song_uri["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
    except IndexError:
        print('non esiste la canzone')

playlist = sp.user_playlist_create(user=user_id,public=False,name=f'{date} Billboard 100')

sp.playlist_add_items(playlist_id=playlist["id"], items=uri_list)