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

def format(cur, conn):
    cur.execute('SELECT Billboard.title, Billboard.artist FROM Billboard')
    tlist = cur.fetchall()
    conn.commit()
    return tlist

def formatpit(cur, conn):
    cur.execute('SELECT Pitchfork.title, Pitchfork.artist FROM Pitchfork')
    tlist = cur.fetchall()
    conn.commit()
    return tlist

# def strip_artists(lst):
#     final_names = []
#     for x in lst:
#         if '/' in x[1]:
#             name = x[1].split('With')
#             final_names.append(name[0].strip())
#         elif '&' in x[1]:
#             name = x[1].split('&')
#             final_names.append(name[0].strip())
#         elif 'Featuring' in x[1]:
#             name = x[1].split('Featuring')
#             final_names.append(name[0].strip())
#         elif 'DJ' in x[1]:
#             name = x[1].split('DJ')
#             final_names.append(name[1].strip())
#         else:
#             final_names.append(x[1])
#     return final_names

def strip_titles(lst):
    final_titles = []
    for x in lst:
        if '$' in x[0]:
            title = x[0].replace('$','s')
            final_titles.append(title)
        elif "('" in x[0]:
            title = x[0].strip("(")
            final_titles.append(title.strip())
        if 'ft' in x[0]:
            title = x[0].split('ft')
            final_titles.append(title.strip())
            #final_titles.append(x[0].strip())
        else:
            final_titles.append(x[0])
    return final_titles

def final_tuples(listt, list2):
    new = []
    for x in listt:
        new.append(x[1])

    y = list(zip(list2,new))
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

def theflist(songlist, apidatalist):
    songgg = []
    for item in songlist:
        songgg.append(item[0])
    x = list(zip(songgg, apidatalist))
    return x


def flistdates(songlist, apidatalist):
    songz = []
    for item in songlist:
        songz.append(item[0])
    y = list(zip(songz, apidatalist))
    return y




def pop_table(cur, conn, lst):
    cur.execute("DROP TABLE IF EXISTS Spotify_Popularity_Scores")
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_Popularity_Scores (song_ID INTEGER PRIMARY KEY, track TEXT, popularity INTEGER)")

    #Calls pop_lst()
    popularity_lst = theflist(final_tuples(lst,strip_titles(lst)) , thesongpopularity(lst))
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
    cur.execute("DROP TABLE IF EXISTS Spotify_Popularity_Scores2")
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_Popularity_Scores2 (song_ID INTEGER PRIMARY KEY, track TEXT, popularity INTEGER)")

    #Calls pop_lst()
    popularity_lst = theflist(lst , thesongpopularity(lst))
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
    cur.execute("DROP TABLE IF EXISTS Spotify_Dates")
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_Dates (song_ID INTEGER PRIMARY KEY, track TEXT, date TEXT)")

    #Calls pop_lst()
    date_list = theflist(final_tuples(lst,strip_titles(lst)), thesongdate(lst))
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
        cur.execute("INSERT INTO Spotify_Dates(song_ID, track, date) VALUES (?, ?, ?)", (song_ID, track, date))
        index += 1
    conn.commit()

def date_table2(cur, conn, lst):
    cur.execute("DROP TABLE IF EXISTS Spotify_Dates2")
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_Dates2 (song_ID INTEGER PRIMARY KEY, track TEXT, date TEXT)")

    #Calls pop_lst()
    date_list = theflist(lst, thesongdate(lst))
    #Reads Billboard Database and find the last index of data in Spotify_Popularity_Scores. Prevents duplicates when code is run again.
    cur.execute('SELECT track FROM Spotify_Dates2')
    track_list = cur.fetchall()
    index = len(track_list)
    #Adds songs in Billboard table (25 entries each time)
    for i in range(25):
        #song_ID identifies unique songs
        song_ID = index + 1
        track = date_list[index][0]
        date = date_list[index][1]
        cur.execute("INSERT INTO Spotify_Dates2(song_ID, track, date) VALUES (?, ?, ?)", (song_ID, track, date))
        index += 1
    conn.commit()



def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/TopCharts.db')
    cur = conn.cursor()
    tuples_lst = format(cur, conn)
    tuples_lst2 = formatpit(cur, conn)
    u = strip_titles(tuples_lst2)
    #c = final_tuples(tuples_lst2, u)
    print(u)

    # pop_table(cur, conn, tuples_lst)
    # date_table(cur, conn, tuples_lst)

    # pop_table2(cur, conn, tuples_lst2)
    # date_table2(cur, conn, tuples_lst2)

    conn.close()



if __name__ == "__main__":
    main()
