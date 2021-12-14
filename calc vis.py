#calc vis
import requests
import re
import os
import csv
import sqlite3
import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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
    plt.title("Songs' Popularity Deviations from the Mean Popularity Billboard")
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
    plt.title("Songs' Popularity Deviations from the Mean Popularity Pitchfork")
    plt.tight_layout()
    plt.show()


def season_billboard_songs(cur, conn, meansongpop):
    """Join songs in Spotify and Pitchfork by season"""
    cur.execute('SELECT Spotify_Dates.track, Spotify_Dates.season FROM Spotify_Dates JOIN Spotify_Popularity_Scores ON Spotify_Popularity_Scores.track = Spotify_Dates.track WHERE Spotify_Popularity_Scores.popularity > ?', (meansongpop,))
    #select all titles and seasons where the popularity rating is greater than the mean. 
    #need to add seasons to S-Dates
    #should return in form [(title, season)]
    b =cur.fetchall()
    fall_count = 0
    spring_count = 0
    winter_count = 0
    summer_count = 0
    other_count = 0
    for i in b:
        if i[1] == "fall":
            fall_count += 1
        elif i[1] == "spring":
            spring_count += 1
        elif i[1] == "winter":
            winter_count += 1
        elif i[1] == "summer":
            summer_count += 1
        else:
            other_count +=1
    total_count = fall_count + spring_count + winter_count + summer_count + other_count
    #get %s of each season
    fall_pct = fall_count/total_count
    spring_pct = spring_count/total_count
    winter_pct = winter_count/total_count
    summer_pct = summer_count/total_count
    other_pct = other_count/total_count
    pct_dict_bb = {"Fall": fall_pct, "Spring": spring_pct, "Winter": winter_pct, "Summer": summer_pct, "Other": other_pct}
    #print(pct_list_top_80)
    return pct_dict_bb

def season_pitch_songs(cur, conn, meansongpop):
    """Join songs in Spotify and Pitchfork by season"""
    cur.execute('SELECT Spotify_Dates2.track, Spotify_Dates2.season FROM Spotify_Dates2 JOIN Spotify_Popularity_Scores2 ON Spotify_Popularity_Scores2.track = Spotify_Dates2.track WHERE Spotify_Popularity_Scores2.popularity > ?', (meansongpop,))
    #select all titles and seasons where the popularity rating is greater than the mean. 
    #need to add seasons to S-Dates
    #should return in form [(title, season)]
    b =cur.fetchall()
    fall_count = 0
    spring_count = 0
    winter_count = 0
    summer_count = 0
    other_count = 0
    for i in b:
        if i[1] == "fall":
            fall_count += 1
        elif i[1] == "spring":
            spring_count += 1
        elif i[1] == "winter":
            winter_count += 1
        elif i[1] == "summer":
            summer_count += 1
        else:
            other_count +=1
    total_count = fall_count + spring_count + winter_count + summer_count + other_count
    #get %s of each season
    fall_pct = fall_count/total_count
    spring_pct = spring_count/total_count
    winter_pct = winter_count/total_count
    summer_pct = summer_count/total_count
    other_pct = other_count/total_count
    pct_list_top_80 = [fall_pct, spring_pct, winter_pct, summer_pct, other_pct]

    pct_dict_pf = {"Fall": fall_pct, "Spring": spring_pct, "Winter": winter_pct, "Summer": summer_pct, "Other": other_pct}
    return pct_dict_pf

def season_normal_songs(cur, conn):
    cur.execute('SELECT Spotify_Dates.track, Spotify_Dates.season FROM Spotify_Dates JOIN Spotify_Popularity_Scores ON Spotify_Popularity_Scores.track = Spotify_Dates.track')
    #select all titles and seasons where the popularity rating is greater than the mean. 
    #need to add seasons to S-Dates
    #should return in form [(title, season)]
    b =cur.fetchall()
    fall_count = 0
    spring_count = 0
    winter_count = 0
    summer_count = 0
    other_count = 0
    for i in b:
        if i[1] == "fall":
            fall_count += 1
        elif i[1] == "spring":
            spring_count += 1
        elif i[1] == "winter":
            winter_count += 1
        elif i[1] == "summer":
            summer_count += 1
        else:
            other_count +=1
    total_count = fall_count + spring_count + winter_count + summer_count + other_count
    #get %s of each season
    fall_pct = fall_count/total_count
    spring_pct = spring_count/total_count
    winter_pct = winter_count/total_count
    summer_pct = summer_count/total_count
    other_pct = other_count/total_count
    pct_list_all = [fall_pct, spring_pct, winter_pct, summer_pct, other_pct]
    
    return pct_list_all

def season_normal_songs2(cur, conn):
    cur.execute('SELECT Spotify_Dates2.track, Spotify_Dates2.season FROM Spotify_Dates2 JOIN Spotify_Popularity_Scores2 ON Spotify_Popularity_Scores2.track = Spotify_Dates2.track')
    #select all titles and seasons where the popularity rating is greater than the mean. 
    #need to add seasons to S-Dates
    #should return in form [(title, season)]
    b =cur.fetchall()
    fall_count = 0
    spring_count = 0
    winter_count = 0
    summer_count = 0
    other_count = 0
    for i in b:
        if i[1] == "fall":
            fall_count += 1
        elif i[1] == "spring":
            spring_count += 1
        elif i[1] == "winter":
            winter_count += 1
        elif i[1] == "summer":
            summer_count += 1
        else:
            other_count +=1
    total_count = fall_count + spring_count + winter_count + summer_count + other_count
    #get %s of each season
    fall_pct = fall_count/total_count
    spring_pct = spring_count/total_count
    winter_pct = winter_count/total_count
    summer_pct = summer_count/total_count
    other_pct = other_count/total_count
    pct_list_all = [fall_pct, spring_pct, winter_pct, summer_pct, other_pct]
    return pct_list_all
    
    #idea: could compare totals in top songs to regular proportions.
def season_bar_graph(pct_dict_bb, pct_list_all):
    labels = []
    for i in pct_dict_bb.keys():
        labels.append(i)
    y = []
    for items in pct_dict_bb.values():
        y_item = items * 100
        y.append(y_item)
    z = []
    for items in pct_list_all:
        z_item = items * 100
        z.append(z_item)
    x = np.arange(len(labels))
    plt.bar(x - .2, y, 0.4, label = "Songs Above Mean")
    plt.bar(x + 0.2, z, 0.4, label = "All Songs")
    plt.xticks(x, labels)
    plt.xlabel("Seasons")
    plt.ylabel("Percentage")
    plt.title("Percents by Season for Billboard")
    plt.legend()
    plt.show()



def season_bar_graph2(pct_dict_pf, pct_list_all):
    labels = []
    for i in pct_dict_pf.keys():
        labels.append(i)
    y = []
    for items in pct_dict_pf.values():
        y_item = items * 100
        y.append(y_item)
    z = []
    for items in pct_list_all:
        z_item = items * 100
        z.append(z_item)
    x = np.arange(len(labels))
    plt.bar(x - .2, y, 0.4, label = "Songs Above Mean")
    plt.bar(x + 0.2, z, 0.4, label = "All Songs")
    plt.xticks(x, labels)
    plt.xlabel("Seasons")
    plt.ylabel("Percentage")
    plt.title("Percents by Season for Pitchfork")
    plt.legend()
    plt.show()

def season_pie_graph(seasonlist):
    sizes = seasonlist
    labels = 'Fall', 'Winter', 'Spring', 'Summer', 'Other'
    colors = ['red', 'cyan', 'pink', 'gold', 'grey']
    plt.pie(sizes, labels = labels, colors = colors, autopct='%1.1f%%', startangle = 180)
    plt.axis('equal')
    plt.title("Distribution of Songs Released Per Season for Billboard Hot 100 of 2020")
    plt.show()

def season_pie_graph2(seasonlist2):
    sizes = seasonlist2
    labels = 'Fall', 'Winter', 'Spring', 'Summer', 'Other'
    colors = ['red', 'cyan', 'pink', 'gold', 'grey']
    plt.pie(sizes, labels = labels, colors = colors, autopct='%1.1f%%', startangle = 180)
    plt.axis('equal')
    plt.title("Distribution of Songs Released Per Season for Pitchfork Best 100 of 2020")
    plt.show()


def writeText(filename, cur, conn):
    path = os.path.dirname(os.path.abspath(__file__)) + os.sep
    outFile = open(path + filename, "w")
    outFile.write("Comparing the Average Popularity of a BillBoard Hot 100 Songs and Pitchfork Best Songs of 2020 on Spotify\n")
    outFile.write("============================================================\n\n")
    pop_output = (avg_popranking(cur, conn))
    pop_output2 = (avg_popranking2(cur, conn))

    rounded_pop = int(pop_output*100) / 100
    rounded_pop2 = int(pop_output2*100) /100
    outFile.write("The average popularity of a Billboard Hot 100 song on Spotify is " + str(rounded_pop) + "." + "\n\n")
    outFile.write("The average popularity of a Pitchfork's 100 Best Songs " + str(rounded_pop2) + "." + "\n\n")
    outFile.close()
    

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/TopCharts.db')
    cur = conn.cursor()
    mean = avg_popranking(cur, conn)
    mean2 = avg_popranking2(cur, conn)
    diff_ls = deviations(cur, conn, mean)
    plot_deviations(cur, conn, diff_ls)

    mean2 = avg_popranking2(cur, conn)
    diff_ls2 = deviations2(cur, conn, mean2)
    plot_deviations2(cur, conn, diff_ls2)
    mean_songs = season_billboard_songs(cur, conn, mean)
    mean_songs2 = season_pitch_songs(cur, conn, mean2)
    normal_songs = season_normal_songs(cur, conn)
    normal_songs2 = season_normal_songs2(cur, conn)
    season_pie_graph(normal_songs)
    season_pie_graph2(normal_songs2)
    season_bar_graph(mean_songs, normal_songs)
    writeText("Average Popularity.txt", cur, conn)
    season_bar_graph2(mean_songs2, normal_songs2)
    conn.close()



if __name__ == "__main__":
    main()