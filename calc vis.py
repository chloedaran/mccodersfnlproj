#calc vis
import requests
import re
import os
import csv
import sqlite3
import json
import matplotlib
import matplotlib.pyplot as plt

def avg_popranking(cur, conn, table):
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
    plt.plot(x, y, 'ro')
    plt.xlabel("Songs")
    plt.xticks(x, rotation = 'vertical')
    plt.ylabel("Deviation from Mean Popularity")
    plt.title("Songs' Popularity Deviations from the Mean Popularity")
    plt.tight_layout()
    plt.show()


def writeText(filename, cur, conn):

    # path = os.path.dirname(os.path.abspath(__file__)) + os.sep

    # outFile = open(path + filename, "w")
    # outFile.write("Comparing the Average Popularity of a BillBoard Hot 100 Songs and Pitchfork on Spotify\n")
    # outFile.write("=============================================================\n\n")
    # pop_output = (average_popularity(cur, conn))
    # #This line rounds the average popularity to one decimal place.
    # rounded_pop = int(pop_output*100) / 100
    # outFile.write("The average popularity of a Billboard Hot 100 song on Spotify is " + str(rounded_pop) + "." + "\n\n")
    # outFile.close()
    pass

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/TopCharts.db')
    cur = conn.cursor()
    mean = avg_popranking(cur, conn, 'Spotify_Popularity_Scores')
    diff_ls = deviations(cur, conn, mean)
    plot_deviations(cur, conn, diff_ls)
    
    conn.close()



if __name__ == "__main__":
    main()