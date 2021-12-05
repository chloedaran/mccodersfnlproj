#Final Project 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json

cid = '5e6f0741afdd4e2892e4aa3dacd22f8a'
secret = '803eb81ea146492fb5ec1edca8e1b9d5'


client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)




def get_top_genres():
    popularity = []
    for i in range(0,10000,50):
        track_results = sp.search(q='year:2018', type='track', limit=50,offset=i)
        for i, t in enumerate(track_results['tracks']['items']):
            popularity.append(t['popularity'])
    return popularity
    #limit to 50 artists

def get_artist_genre():
    #limit to top ten artists
    pass
def get_top_songs():
    #50 songs artist dictionary 
    pass

def main():

    # path = os.path.dirname(os.path.abspath(__file__))
    # conn = sqlite3.connect(path+'/music.db')
    # cur = conn.cursor()
    print(get_top_genres())
    # (cur, conn)



    # conn.close()



if __name__ == "__main__":
    main()
