import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd
from youtubesearchpython import VideosSearch

cid = input("Enter your Spotify client id:")
sid = input("Enter your Spotify secret id:")
client_id = cid
client_secret = sid

client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def playlist_to_dict(URL):
    playlist_id = URL
    
    playlist_tracks_data = sp.playlist_tracks(playlist_id)
    tracks = playlist_tracks_data['items']
    while playlist_tracks_data['next']:
        playlist_tracks_data = sp.next(playlist_tracks_data)
        tracks.extend(playlist_tracks_data['items'])
    
    playlist_tracks_artist = []
    playlist_tracks_titles = []
    for track in tracks:
        if(track['track']['id']!=None):
            playlist_tracks_titles.append(track['track']['name'])
            playlist_tracks_artist.append(track['track']['artists'][0]['name'])
    
    list = dict(zip(playlist_tracks_titles, playlist_tracks_artist))
    return list

def search_youtube(song_dict):
    link_list = []
    for track in song_dict:
        query = "{} - {}".format(track, song_dict[track])
        videosSearch = VideosSearch(query, limit = 1)
        result = videosSearch.result()
        link = result["result"][0]["link"]
        link_list.append(link)
    return link_list

song_list = playlist_to_dict("")
link_list = search_youtube(song_list)
df = pd.DataFrame(list(song_list.items()),columns = ['Song Name','Artist'])
df['Song Link'] = link_list

df.to_csv('song_output.csv', index=False)