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

def avg_popranking2(cur, conn):
    cur.execute('SELECT track, popularity FROM Spotify_Popularity_Scores2')
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

def deviations2(cur, conn, mean_songpop):
    """Take difference between each song's popularity ranking and the mean for that list"""
    cur.execute('SELECT track, popularity FROM Spotify_Popularity_Scores2')
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
def plot_deviations2(cur, conn, diff_ls):
    cur.execute('SELECT track, popularity FROM Spotify_Popularity_Scores2')
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


def season_cat(cur, conn):
    season_var =[]
    cur.execute('SELECT track, date FROM Spotify_Dates')
    date_list = cur.fetchall()
    for item in date_list:
        if item[6:8] == '05' or '06' or '07' or '08':
            season_var.append('summer')
        elif item[6:8] == '09' or '10':
            season_var.append('fall') 
        elif item[6:8] == '11' or '12' or '01' or '02':
            season_var.append('winter')
        elif item[6:8] == '03' or '04':
            season_var.append('spring')
    return season_var
def season_cat2(cur, conn):
    season_var =[]
    cur.execute('SELECT track, date FROM Spotify_Dates2')
    date_list = cur.fetchall()
    for item in date_list:
        if item[6:8] == '05' or '06' or '07' or '08':
            season_var.append('summer')
        elif item[6:8] == '09' or '10':
            season_var.append('fall') 
        elif item[6:8] == '11' or '12' or '01' or '02':
            season_var.append('winter')
        elif item[6:8] == '03' or '04':
            season_var.append('spring')
    return season_var

def season_data(cur, conn, list):
    cur.execute('SELECT season FROM Spotify_Dates')
    season_list = cur.fetchall()
    index = len(season_list)
    for i in range (25):
        season = season_list[index]
        cur.execute('INSERT INTO Spotify_Dates(season) VALUES (?)', (season))
        index += 1
    conn.commit()
def season_data2(cur, conn, list):
    cur.execute('SELECT season FROM Spotify_Dates2')
    season_list = cur.fetchall()
    index = len(season_list)
    for i in range (25):
        season = season_list[index]
        cur.execute('INSERT INTO Spotify_Dates2(season) VALUES (?)', (season))
        index += 1
    conn.commit()
def season_pie_graph(cur, conn, seasonlist):
    pass



def writeText(filename, cur, conn):

    path = os.path.dirname(os.path.abspath(__file__)) + os.sep

    outFile = open(path + filename, "w")
    outFile.write("Comparing the Average Popularity of a BillBoard Hot 100 Songs and Pitchfork Best Songs of 2020 on Spotify\n")
    outFile.write("=============================================================\n\n")
    pop_output = (avg_popranking(cur, conn))
    pop_output2 = (avg_popranking2(cur, conn))

    # #This line rounds the average popularity to one decimal place.
    rounded_pop = int(pop_output*100) / 100
    rounded_pop2 = int(pop_output2*100) /100
    outFile.write("The average popularity of a Billboard Hot 100 song on Spotify is " + str(rounded_pop) + "." + "\n\n")
    outFile.write("The average popularity of a Pitchfork's 100 Best Songs " + str(rounded_pop2) + "." + "\n\n")
    outFile.close()
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