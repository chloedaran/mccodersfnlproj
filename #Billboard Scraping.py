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

    #put it in a database
    # cur.execute("CREATE TABLE Top Songs (id INTEGER PRIMARY KEY, song TEXT)")
    # for i in range(len(ls_of_titles)):
    #     cur.execute("INSERT INTO Top Songs (id,song) VALUES (?,?)",(i, ls_of_titles[i]))

    
        #     titles = soup.find(class_="c-title  a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max")
        #class_="['c-title',  'a-font-primary-bold-s', 'u-letter-spacing-0021', 'lrv-u-font-size-18@tablet', 'lrv-u-font-size-16 u-line-height-125', 'u-line-height-normal@mobile-max']"
        # for j in titles:
    #elif chart == "top-songs":   
        # titles = soup.find(id="title-of-a-story")
        # titles.find_all('h3', class_=)
        # soup.find_all('h3')


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
    print(get_top_genres())
    gather_data_BS('hot-100-songs/')
    gather_data_BS('top-billboard-200-albums/')
    # (cur, conn)



    # conn.close()



if __name__ == "__main__":
    main()