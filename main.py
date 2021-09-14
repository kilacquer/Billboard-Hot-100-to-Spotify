from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys

URL ="https://www.billboard.com/charts/hot-100/"

CLIENTSECRET = ""
CLIENTID = ""
USERID = ""


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENTID,
                                               client_secret=CLIENTSECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private"))

def get_Date():
    date = input("Enter date to get top 100 (Use YYYY-MM-DD): ")
    return date

def extract(date):
    post = requests.get(f"{URL}{date}")
    soup = BeautifulSoup(post.content, "html.parser")
    return soup

def transform(soup):
    song_titles = [title.getText() for title in soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")]
    return song_titles

def load(titles):
    song_uri = []
    for title in titles:
        if len(sys.argv) > 1:
            name = ' '.join(sys.argv[1:])
        else:
            name = f"{title}"

        results = sp.search(q=f"track: {name}", type='track')
        try:
            uri = results['tracks']['items'][0]['uri']
            song_uri.append(uri)
        except IndexError:
            print(f"{title} doesn't exist in Spotify. Skipped")
    return(song_uri)


inp = get_Date()
PLAYLIST_NAME = f"Billboard 100 During {inp}"
ready = extract(inp)
setlist = transform(ready)
go = load(setlist)

playlist = sp.user_playlist_create(user=USERID, name=PLAYLIST_NAME, public=False)
PLAYLISTID = playlist['id']

sp.playlist_add_items(PLAYLISTID, go)


