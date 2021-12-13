#Billboard Scraping

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json




#use Beautiful soup and html parser to get info from website and store in database. and run calculations on Billboard data

def createDatabase(name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+name)
    cur = conn.cursor()
    return cur, conn


def gather_data_pitch():
    titles_list = []
    artist =[]
    songname =[]
    thenewnew =[]
    base_url2 = f"https://pitchfork.com/features/lists-and-guides/best-songs-2020/" 
    page = requests.get(base_url2)
    soup = BeautifulSoup(page.content, 'html.parser')
    x = soup.find_all('div', class_ = "body__inner-container")
    for i in x:
        songdata = i.find_all('h2')
        for v in songdata:
            ssongdata = v.text
            titles_list.append(ssongdata.strip())
    for r in titles_list:
        thenewnew.append(r.split(':'))
    for t in thenewnew:
        artist.append(t[0])
        res = re.sub(r'[^\w\s]', '', t[1])
        songname.append(res)
    together = zip(artist, songname)
    togetherr = list(together)
    print(togetherr)
    return togetherr


def gather_data_BS():
    #gathers data from Beautiful Soup from the base_url and stores in a database
    url = "http://billboard.com/charts/year-end/2020/hot-100-songs/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    ls_of_titles = []
    ls_of_artists = []
    first_song = soup.find('h3', class_="c-title a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max u-letter-spacing-0028@tablet")
    first_song = first_song.text.strip()
    ls_of_titles.append(first_song)
    first_artist = soup.find('span', class_="c-label a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block u-font-size-20@tablet")
    first_artist = first_artist.text.strip()
    ls_of_artists.append(first_artist)
    # first_input = first_song, first_artist
    # ls_of_titles.append(first_input)
        #find all titles
    all_titles = soup.find_all('h3', class_= "c-title a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max")
    all_artists = soup.find_all('span', class_="c-label a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block")
    for i in all_titles:
        title = i.text
        title = title.strip()
        ls_of_titles.append(title)
    for i in all_artists:
        artist = i.text.strip()
        ls_of_artists.append(artist)
    together = zip(ls_of_titles, ls_of_artists)
    together = list(together)
    print(together)
    return together


def set_up_Billboard(cur, conn):
    "Input: Database cursor and connection. No output. Creates Table that will hold Top 100 hummed songs"
    #cur.execute("DROP TABLE IF EXISTS Billboard")
    cur.execute("CREATE TABLE IF NOT EXISTS Billboard (song_id INTEGER PRIMARY KEY, song_rank INTEGER, title TEXT, artist TEXT)")
    conn.commit()
def set_up_Pitchfork(cur, conn):
    "Input: Database cursor and connection. No output. Creates Table that will hold Top 100 hummed songs"
    #cur.execute("DROP TABLE IF EXISTS Pitchfork")
    cur.execute("CREATE TABLE IF NOT EXISTS Pitchfork (song_id INTEGER PRIMARY KEY, song_rank INTEGER, title TEXT, artist TEXT)")
    conn.commit()

def fill_data_in_Billboard(cur,conn):
    "Input: Database cursor and connection. No output. Fills in the Billboard table with songs, artists, and ID. ID is song's unique identification number for reference."
    #Calls get_data()
    data_list = gather_data_BS()
    
    cur.execute('SELECT title FROM Billboard')
    songs_list = cur.fetchall()
    index = len(songs_list)
    for i in range(25):
        song = data_list[index][0]
        artist = data_list[index][1]
        song_id = index + 1
        cur.execute("INSERT OR IGNORE INTO Billboard (song_rank, title, artist) VALUES (?,?,?)", (song_id, song, artist))
        index +=1
    conn.commit()

def fill_data_in_Pitchfork(cur,conn):
    "Input: Database cursor and connection. No output. Fills in the Pitchfork table with songs, artists, and ID. ID is song's unique identification number for reference."
    #Calls get_data()
    data_list = gather_data_pitch()
    cur.execute('SELECT title FROM Pitchfork')
    songs_list = cur.fetchall()
    index = len(songs_list)
    for i in range(25):
        song = data_list[index][1]
        artist = data_list[index][0]
        song_id = index + 1
        cur.execute("INSERT OR IGNORE INTO Pitchfork (song_rank, title, artist) VALUES (?,?,?)", (song_id, song, artist))
        index +=1
    conn.commit()




def main():
    # path = os.path.dirname(os.path.abspath(__file__))
    # conn = sqlite3.connect(path+'/music.db')
    # cur = conn.cursor()

    cur, conn = createDatabase('TopCharts.db')
    gather_data_BS()
    set_up_Billboard(cur, conn)
    fill_data_in_Billboard(cur, conn)
    
    gather_data_pitch()
    set_up_Pitchfork(cur, conn)
    fill_data_in_Pitchfork(cur, conn)

    # gather_data_BS('top-billboard-200-albums/')
    # gather_data_BS('top-artists/')
    # (cur, conn)



    # conn.close()



if __name__ == "__main__":
    main()