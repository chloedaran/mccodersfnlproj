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


# def get_top_genres():
#     artist =[]
#     results = sp.search(q="artist:", limit = 50)
#     for result in results['tracks']['items']:
#         artist.append(results['name'])
#     return  artist 

def thesongpopularity(songname):

    res = sp.search(q='track:' + str(songname[0]))
    thepop = res['tracks']['items'][0]['popularity']
    return thepop


def getbillboard(cur, conn):
    cur.execute('SELECT song, artist FROM Billboard')
    bill_songs = cur.fetchall()
    conn.commit()
    return bill_songs

    #limit to top ten artists
    #api function

def clean_titles(listof):
    
    
    #finallist = list(zip(finalsongs, finalnames)
    #return finallist
   
    #api function
    #50 songs artist dictionary 
    pass


def reformat_fnl_tup():
     
    pass 

def create_table(cur, conn, list):
    #calculate the proportion of songs an artist has in the top 100 
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_Popularity_Scores (song_ID INTEGER PRIMARY KEY, track TEXT, popularity INTEGER)")
    pop_list = reformat_fnl_tup(list)
    
    pass

def get_top_albums_pitch():
    #options 
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
