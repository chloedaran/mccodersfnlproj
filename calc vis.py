#calc vis
import requests
import re
import os
import csv
import sqlite3
import json
import matplotlib
import matplotlib.pyplot as plt

def avg_popranking(cur, conn):
    cur.execute('SELECT track, popularity FROM Spotify_Popularity_Scores')
    songpop_list = cur.fetchall()
    #get values of dict_song into a list.
    #loop again and then make them integers.
    pop_ls = []
    count = 0
    for i in songpop_list:
        #apend each ranking to the list of popularity rankings
        pop_ls.append(i[1])
    for pop in pop_ls:
        #sum each pop ranking in variable
        count = count + pop
    count = int(count)
    #find mean song popularity for this list from the database
    mean_songpop = count/len(pop_ls)
    print(mean_songpop)
    return mean_songpop
        
def deviations(cur, conn, mean_songpop):
    """Take difference between each song's popularity ranking and the mean for that list"""
    cur.execute('SELECT track, popularity FROM Spotify_Popularity_Scores')
    songpop_list = cur.fetchall()
    pop_ls = []
    diff_ls = []
    for i in songpop_list:
        #apend each ranking to the list of popularity rankings
        pop_ls.append(i[1])
    for i in pop_ls:
        diff = i - mean_songpop
        diff_ls.append(int(diff))
    print(diff_ls)
    return diff_ls

def plot_deviations(cur, conn, diff_ls):
    cur.execute('SELECT track, popularity FROM Spotify_Popularity_Scores')
    songpop_list = cur.fetchall()
    x = []
    y = []
    for i in songpop_list:
        x.append(i[0]) #song titles are along the x-axis
    for i in diff_ls:
        y.append(i) #diff of avg popularity and mean is y-axis
    plt.line(x, y)
    plt.xlabel("Songs")
    plt.ylabel("Deviation from Mean Popularity")
    plt.title("Songs' Popularity Deviations from the Mean Popularity")
    plt.show()

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/TopCharts.db')
    cur = conn.cursor()
    mean = avg_popranking(cur, conn)
    diff_ls = deviations(cur, conn, mean)
    plot_deviations(cur, conn, diff_ls)
    
    conn.close()



if __name__ == "__main__":
    main()