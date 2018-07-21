import time
import sqlite3
import pandas as pd
import json
import requests
import urllib.request
import geopy.distance
from math import sin, cos, sqrt, atan2, radians

R = 6371.0
api_key = "AIzaSyDBw6Im3VFllQckVbq-CWApPfJm21mOUP0"

#Sqlite setup
conn = sqlite3.connect("/home/j_blrd/webscraping/database/database.db")
c = conn.cursor()

print(pd.read_sql_query("SELECT * FROM location_master_table", conn))

dest_name = input("Select location name from list above:\n")
c.execute("SELECT location_id FROM location_master_table WHERE location_name = ?", (dest_name,))
location_id = int(c.fetchone()[0])

c.execute("SELECT property_name, property_id FROM property_master_table WHERE location_id = ?", (location_id,))
hotel_list = [list(x) for x in c.fetchall()]

def findArea(lat, lng):
    distances = []

    areas = {"Happo":    (36.6978602, 137.8362237),
             "Echoland": (36.6926348, 137.8413703),
             "Goryu":    (36.6667387, 137.8322317),
             "Hakuba47": (36.6849873, 137.8261543)}

    hotel = (lat, lng)

    for x in areas:
        distances.append(geopy.distance.distance(areas[x], hotel).km)

    print(list(areas.keys())[distances.index(min(distances))])

for i in range(0, len(hotel_list)):
    hotel_name = hotel_list[i][0].replace(" ", "%")
    property_id = hotel_list[i][1]

    print("\n" + str(property_id) + ": " + hotel_name)

    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?\
input=" + hotel_name + "&inputtype=textquery&fields=geometry,photos&key=" + api_key

    response = requests.get(url)
    json_data = json.loads(response.text)

    if(json_data["status"] != "OK"):
        continue

    location = json_data["candidates"][0]["geometry"]["location"]
    lat = location["lat"]
    lng = location["lng"]
    findArea(lat, lng)

    if("photos" not in json_data["candidates"][0]):
        continue

    photo_reference = json_data["candidates"][0]["photos"][0]["photo_reference"]
    image_url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&\
photoreference=" + photo_reference  + "&key=" + api_key
    urllib.request.urlretrieve(image_url, "/home/j_blrd/webscraping/database/images/"+str(location_id)+"_"+str(property_id))

