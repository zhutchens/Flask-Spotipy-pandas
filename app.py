from flask import Flask, render_template, redirect, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import datetime
import pandas as pd
import matplotlib

load_dotenv()
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


app = Flask(__name__)

@app.get('/') 
def home():
    return render_template('index.html')

@app.get('/sign_up')
def sign_up_page():
    return render_template('sign_up.html')

@app.get('/sign_in')
def sign_in_page():
    return render_template('sign_in.html')

@app.get('/playlist')
def playlist_page():
    return render_template('playlist.html')

@app.post('/playlist')
def get_playlist_info():
    link = request.form.get("link")
    playlist_id = link.split('/')[4]
    if '?' in playlist_id:
        playlist_id = playlist_id.split('?')[0]
    #print(playlist_id)
    playlist = spotify.playlist(playlist_id)
    # List will look like: name, owner, number of tracks, 
    track_names = []
    track_albums = []
    track_artists = []
    track_duration = []

    for track in playlist['tracks']['items']:
        track_names.append(track['track']['name'])
        track_albums.append(track['track']['album']['name'])
        track_artists.append(track['track']['artists'][0]['name'])
        track_duration.append(datetime.timedelta(milliseconds=track['track']['duration_ms']))

    df = pd.DataFrame(data=track_artists)
    print(df.head())
    #plot = df.iloc[0].plot(kind='pie', explode=(0.5, 0.5 ,0.5), autopct='%1.0f%%')
    #charts.append(plot)
    data = zip(track_names, track_duration, track_artists, track_albums)
    #print(data)
    return render_template('playlist.html', data=data)

