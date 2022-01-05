import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from youtubesearchpython import VideosSearch
import pathlib

from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

counter = 0
fileLocation = pathlib.Path(__file__).parent.resolve()

def get_Info(sp, URL, df, copy):
    cover_url = sp.playlist_cover_image(URL)
    cover_url = cover_url[0]['url']
    response = requests.get(cover_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    resized_img = img.resize((160,160))

    cover_img = ImageTk.PhotoImage(resized_img)
    img_label.pack()
    img_label.configure(image=cover_img)
    img_label.image = cover_img

    playlist_name = sp.playlist(URL, fields="name")
    playlist_name = playlist_name['name']
    name_label.config(text = playlist_name)    
    name_label.pack()

    playlist_creation = copy['items'][0]['added_at']
    playlist_creation = playlist_creation[0:10]

    playlist_size = copy['total']
    size_info.config(text="{}, created on {}, contains {} songs".format(playlist_name, playlist_creation, playlist_size))
    size_info.pack()

    mode = df['Artist'].value_counts().idxmax()
    item_counts = df['Artist'].value_counts()
    max_item = item_counts.max()    
    artist_info.config(text = "The most frequent artist in this playlist is {}, appearing {} times".format(mode, str(max_item)))
    artist_info.pack()

def playlist_to_dict(URL):
    global counter
    client_credentials_manager = SpotifyClientCredentials(client_id='2ff1294d1713472bbc130b0ab371c331',client_secret='2c6eb62cb99147f795b7bc3f3376c83a')
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    #these are credentials to a throwaway account

    playlist_id = URL
    playlist_tracks_data = sp.playlist_tracks(playlist_id)
    playlist_tracks_copy = playlist_tracks_data

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
    
    song_list = dict(zip(playlist_tracks_titles, playlist_tracks_artist))

    link_list = []
    for track in song_list:
        query = "{} - {}".format(track, song_list[track])
        videosSearch = VideosSearch(query, limit = 1)
        result = videosSearch.result()
        link = result["result"][0]["link"]
        link_list.append(link)  

    df = pd.DataFrame(list(song_list.items()),columns = ['Song Name','Artist'])
    df['Song Link'] = link_list


    get_Info(sp, playlist_id, df, playlist_tracks_copy)

    output_csv = "song_output" + str(counter) + ".csv" 
    df.to_csv(output_csv, index=False)
    counter = counter + 1
    csv_info.config(text="File saved to: {} with name {}".format(str(fileLocation),output_csv))
    csv_info.pack()

root = Tk()
root.title("Spotify Playlist Information")
root.geometry("500x400")

background_image = ImageTk.PhotoImage(file='bg.jpg')
background_label = Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = Frame(root, bg='grey', bd=1)
frame.pack()

name_label = Label(text = "", font=('',30))  
img_label = Label()  
img_label.config(image='')

entry = Entry(frame, font=('',10), width=375)
entry.pack(side=TOP, ipady=5)

button = Button(frame, text="Enter and Process Playlist", font=40, command=lambda: playlist_to_dict(entry.get()))
button.pack()

lower_frame = Frame(root, bg = 'grey', bd=5)
lower_frame.place(relx=0.5, rely=0.75, relwidth=1.0, relheight=0.6, anchor='n')

size_info = Label(lower_frame, text = "", width=300)
artist_info = Label(lower_frame, text = "", width=300)
csv_info = Label(lower_frame, text="", width=300)

root.mainloop()