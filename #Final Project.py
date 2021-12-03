#Final Project 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests
import re
import os
import csv
import sqlite3
import json

cid = '5e6f0741afdd4e2892e4aa3dacd22f8a'
secret = '803eb81ea146492fb5ec1edca8e1b9d5'

ccm = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = ccm)




