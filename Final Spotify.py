#Final Project 
import requests
import re
import os
import sqlite3
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

def strip_artists(lst):
    final_names = []
    for x in lst:
        if '/' in x[1]:
            name = x[1].split('With')
            final_names.append(name[0].strip())
        elif '&' in x[1]:
            name = x[1].split('&')
            final_names.append(name[0].strip())
        elif 'Featuring' in x[1]:
            name = x[1].split('Featuring')
            final_names.append(name[0].strip())
        elif 'DJ' in x[1]:
            name = x[1].split('DJ')
            final_names.append(name[1].strip())
        else:
            final_names.append(x[1])
    return final_names

def strip_titles(lst):
    final_titles = []
    for x in lst:
        if '(' in x[0]:
            title = x[0].split('(')
            final_titles.append(title[0].strip())
        elif "ft'" in x[0]:
            title = x[0].strip("\'")
            final_titles.append(title.strip())
        else:
            final_titles.append(x[0])
        return final_titles

def ultimate_tuple(lst):
    titles = strip_titles(lst)
    artists = strip_artists(lst)
    tuples = list(zip(titles, artists))
    return tuples


def fformat(cur, conn):
    cur.execute('SELECT title, artist FROM Pitchfork')
    thelist = cur.fetchall()
    conn.commit()
    return thelist


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

# def pop_list(lst):
#     pop_lst = []
#     for x in lst:
#         string = x[0] + ' (by ' + x[1] + ')'
#         pop_lst.append((string,thesongpopularity(x)))
#     return pop_lst

    #limit to top ten artists
    #api function



def pop_table(cur, conn, lst):
    """
    Input: Database cursor, connection, and list of tuples in the format (titles, artist). 
    Output: No output. 
    Purpose: Fills in the Spotify_Popularity_Scores table with ID, track, and popularity score. 
    ID is song's unique identification number for reference.
    """
    #Sets up Spotify_Popularity_Scores table
    cur.execute("CREATE TABLE IF NOT EXISTS Spotify_Popularity_Scores (song_ID INTEGER PRIMARY KEY, track TEXT, popularity INTEGER)")
    #Calls pop_lst()
    popularity_lst = pop_list(lst)
    #Reads Billboard Database and find the last index of data in Spotify_Popularity_Scores. Prevents duplicates when code is run again.
    cur.execute('SELECT track FROM Spotify_Popularity_Scores')
    track_list = cur.fetchall()
    index = len(track_list)
    #Adds songs in Billboard table (25 entries each time)
    for i in range(20):
        #song_ID identifies unique songs
        song_ID = index + 1
        track = popularity_lst[index][0]
        popularity = popularity_lst[index][1]
        cur.execute("INSERT INTO Spotify_Popularity_Scores (song_ID, track, popularity) VALUES (?, ?, ?)", (song_ID, track, popularity))
        index += 1
    conn.commit()

def get_top_albums_pitch():
    #options 
    pass 



def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/TopCharts.db')
    cur = conn.cursor()
    tuples_lst = format(cur, conn)
    # for x in tuples_lst:
    #     test.append(thesonggenre(x))
    # print(x)
    #print(tuples_lst)
    y = thesongpopularity(tuples_lst)
    print(y) 
    x = thesongdate(tuples_lst)
    print(x)
    #print(pop_list(tuples_lst))
    # print(refined_tuple_lst)
    # #pop_list(refined_tuple_lst)
    
    conn.close()



if __name__ == "__main__":
    main()
