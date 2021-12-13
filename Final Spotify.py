#Final Project 
from typing import final
import requests
import re
import os
import sqlite3
from requests import api
import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


cid = '5e6f0741afdd4e2892e4aa3dacd22f8a'
secret = '803eb81ea146492fb5ec1edca8e1b9d5'


client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def billboard_selection(cur, conn):
    cur.execute('SELECT Billboard.title, Billboard.artist FROM Billboard')
    tlist = cur.fetchall()
    conn.commit()
    return tlist

def pitchfork_selection(cur, conn):
    cur.execute('SELECT Pitchfork.title, Pitchfork.artist FROM Pitchfork')
    tlist = cur.fetchall()
    conn.commit()
    return tlist

def strip_titles(lst):
    final_titles = []
    for x in lst:
        if '$' in x[0]:
            title = x[0].replace('$','s')
            final_titles.append(title)
        elif "('" in x[0]:
            title = x[0].strip("(")
            final_titles.append(title.strip())
        elif 'ft' in x[0]:
            title = x[0].split('ft')
            final_titles.append(title[0].strip())
        else:
            final_titles.append(x[0])
    for x in final_titles:
        if x == 'P*$$y Fairy (OTW)':
            final_titles.remove(x)
    return final_titles

def final_tuples(ptuples_lst, p_stripped):
    artists = []
    for x in ptuples_lst:
        artists.append(x[1])
    y = list(zip(p_stripped, artists))
    return y


def thesongpopularity(songnamelist):
    newnew =[]
    for i in songnamelist:
        res = sp.search(q='track:' + str(i[0]))
        thepop = res['tracks']['items'][0]['popularity']
        newnew.append(thepop)
    return (newnew)

def thesongdate(songnamelist):
    newnew =[]
    for i in songnamelist: 
        res = sp.search(q='track:' + str(i[0]))
        thepop = res['tracks']['items'][0]['album']['release_date']
        newnew.append(thepop)
    return newnew

def theseason(newnew):
    #gets list of dates from thesongdate()
    season_lst = []
    for date in newnew:
        if date[5:7] == '05' or date[5:7] =='06' or date[5:7] == '07' or date[5:7] == '08':
            season = "summer"
            season_lst.append(season)
        elif date[5:7] == '09' or date[5:7] =='10':
            season = "fall"
            season_lst.append(season)
        elif date[5:7] == '11' or date[5:7] =='12' or date[5:7] =='01' or date[5:7] == '02':
            season = "winter"
            season_lst.append(season)
        elif date[5:7] == '03' or date[5:7] == '04':
            season = "spring"
            season_lst.append(season)
        else:
            season = 'other'
            season_lst.append(season)
    return season_lst

def theflist(songlist, apidatalist, season_lst):
    songgg = []
    for item in songlist:
        songgg.append(item[0])
    x = list(zip(songgg, apidatalist, season_lst))
    return x


def flistdates(songlist, apidatalist):
    songz = []
    for item in songlist:
        songz.append(item[0])
    y = list(zip(songz, apidatalist))
    return y


def pop_table(cur, conn, lst):
    #cur.execute("DROP TABLE IF EXISTS Spotify_Popularity_Scores")
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_Popularity_Scores (song_ID INTEGER PRIMARY KEY, track TEXT, popularity INTEGER)")
    #Calls pop_lst()
    popularity_lst = theflist(final_tuples(lst,strip_titles(lst)), thesongpopularity(lst), theseason(thesongdate(lst)))
    #Reads Billboard Database and find the last index of data in Spotify_Popularity_Scores. Prevents duplicates when code is run again.
    cur.execute('SELECT track FROM Spotify_Popularity_Scores')
    track_list = cur.fetchall()
    index = len(track_list)
    #Adds songs in Billboard table (25 entries each time)
    for i in range(25):
        #song_ID identifies unique songs
        song_ID = index + 1
        track = popularity_lst[index][0]
        popularity = popularity_lst[index][1]
        cur.execute("INSERT INTO Spotify_Popularity_Scores (song_ID, track, popularity) VALUES (?, ?, ?)", (song_ID, track, popularity))
        index += 1
    conn.commit()

def pop_table2(cur, conn, lst):
    #cur.execute("DROP TABLE IF EXISTS Spotify_Popularity_Scores2")
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_Popularity_Scores2 (song_ID INTEGER PRIMARY KEY, track TEXT, popularity INTEGER)")
    #Calls pop_lst()
    popularity_lst = theflist(lst , thesongpopularity(lst), theseason(thesongdate(lst)))
    #Reads Billboard Database and find the last index of data in Spotify_Popularity_Scores. Prevents duplicates when code is run again.
    cur.execute('SELECT track FROM Spotify_Popularity_Scores2')
    track_list = cur.fetchall()
    index = len(track_list)
    #Adds songs in Billboard table (25 entries each time)
    for i in range(25):
        #song_ID identifies unique songs
        song_ID = index + 1
        track = popularity_lst[index][0]
        popularity = popularity_lst[index][1]
        cur.execute("INSERT INTO Spotify_Popularity_Scores2 (song_ID, track, popularity) VALUES (?, ?, ?)", (song_ID, track, popularity))
        index += 1
    conn.commit()

def date_table(cur, conn, lst):
    #cur.execute("DROP TABLE IF EXISTS Spotify_Dates")
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_Dates (song_ID INTEGER PRIMARY KEY, track TEXT, date TEXT, season TEXT)")
    #Calls pop_lst()
    date_list = theflist(final_tuples(lst,strip_titles(lst)), thesongdate(lst), theseason(thesongdate(lst)))
    #Reads Billboard Database and find the last index of data in Spotify_Popularity_Scores. Prevents duplicates when code is run again.
    cur.execute('SELECT track FROM Spotify_Dates')
    track_list = cur.fetchall()
    index = len(track_list)
    #Adds songs in Billboard table (25 entries each time)
    for i in range(25):
        #song_ID identifies unique songs
        song_ID = index + 1
        track = date_list[index][0]
        date = date_list[index][1]
        season = date_list[index][2]
        cur.execute("INSERT INTO Spotify_Dates(song_ID, track, date, season) VALUES (?, ?, ?, ?)", (song_ID, track, date, season))
        index += 1
    conn.commit()

def date_table2(cur, conn, lst):
    #cur.execute("DROP TABLE IF EXISTS Spotify_Dates2")
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_Dates2 (song_ID INTEGER PRIMARY KEY, track TEXT, date TEXT, season TEXT)")
    #Calls pop_lst()
    date_list = theflist(lst, thesongdate(lst), theseason(thesongdate(lst)))
    #Reads Pitchfork Database and find the last index of data in Spotify_Popularity_Scores. Prevents duplicates when code is run again.
    cur.execute('SELECT track FROM Spotify_Dates2')
    track_list = cur.fetchall()
    index = len(track_list)
    #Adds songs in Pitchfork table (25 entries each time)
    for i in range(25):
        #song_ID identifies unique songs
        song_ID = index + 1
        track = date_list[index][0]
        date = date_list[index][1]
        season = date_list[index][2]
        cur.execute("INSERT INTO Spotify_Dates2(song_ID, track, date, season) VALUES (?, ?, ?, ?)", (song_ID, track, date, season))
        index += 1
    conn.commit()



def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/TopCharts.db')
    cur = conn.cursor()
    btuples_lst = billboard_selection(cur, conn)
    ptuples_lst = pitchfork_selection(cur, conn)
    strip_titles(btuples_lst)
    p_stripped = strip_titles(ptuples_lst)
    c = final_tuples(ptuples_lst, p_stripped)
    #print(c)

    
    b_stripped = strip_titles(btuples_lst)
    k = final_tuples(btuples_lst, b_stripped)
    #print(k)
    #print(thesongdate(c))
    

    #pop_table(cur, conn, btuples_lst)
    #date_table(cur, conn, btuples_lst)
    
    pop_table2(cur, conn, c)
    date_table2(cur, conn, c)
    conn.close()



if __name__ == "__main__":
    main()

