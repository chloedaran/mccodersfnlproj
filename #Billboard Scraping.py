#Billboard Scraping

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import sqlite3
import json



#use Beautiful soup and html parser to get info from website and store in database. and run calculations on Billboard data
def create_request_url(chart):
    base_url = f"http://billboard.com/charts/year-end/2020/{chart}"
    return base_url
    #page = requests.get(url)
#print(page.text)

def gather_data_BS(chart):
    #gathers data from Beautiful Soup from the base_url and stores in a database
    url = create_request_url(chart)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    if chart == "hot-100-songs/":
        ls_of_titles = []
        first = soup.find('h3', class_="c-title a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max u-letter-spacing-0028@tablet")
        first_title = first.text
        ls_of_titles.append(first_title.strip())
        all_h3s = soup.find_all('h3', class_= "c-title a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max")
        #, class_="['c-title',  'a-font-primary-bold-s', 'u-letter-spacing-0021', 'lrv-u-font-size-18@tablet', 'lrv-u-font-size-16 u-line-height-125', 'u-line-height-normal@mobile-max']")
    #class_="c-title  a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max" breaking it. but its the right class.
        for i in all_h3s:
            title =i.text
            ls_of_titles.append(title.strip())
        print(ls_of_titles)
    elif chart == "top-billboard-200-albums/":
        ls_of_albums = []
        first = soup.find('h3', class_="c-title a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max u-letter-spacing-0028@tablet")
        first_title = first.text
        ls_of_albums.append(first_title.strip())
        albums = soup.find_all('h3', class_="c-title a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max")
        for i in albums:
            title = i.text
            ls_of_albums.append(title.strip())
        print(ls_of_albums)
        #create a dictionary of each album and the other albums it has in it


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
    together = list(together)
    print(together)
    return together


def get_top_artist_per_genre(popularity):
    #get the top artist given a list of popular genres from spotipy. 
    # return a dictionary w genre as key and the top 10 artists in that category as values
    pass 

def pct_top_artists():
    #get the pct of artists in the top genre that also have a song in the top genre
    pass
def main():

    # path = os.path.dirname(os.path.abspath(__file__))
    # conn = sqlite3.connect(path+'/music.db')
    # cur = conn.cursor()
    #print(get_top_genres())
    #gather_data_BS('hot-100-songs/')
    #gather_data_BS('top-billboard-200-albums/')
    gather_data_pitch()
    # (cur, conn)



    # conn.close()



if __name__ == "__main__":
    main()