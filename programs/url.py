import sqlite3
import bs4 as bs
import os
import urllib.request
from time import sleep

dest_id =   900039080
dest_type = "city"
page = "https://www.booking.com/searchresults.en-gb.html?lang=en-gb&dest_id={}&dest_type={}".format(dest_id, dest_type)
i = 0
new_urls = 0

# Sqlite database initialization
conn = sqlite3.connect("/home/j_blrd/webscraping/database/database.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS urls(url TEXT)")

print("Hotel URLs:")

while(True):
    source = urllib.request.urlopen(page)
    soup = bs.BeautifulSoup(source,"lxml")

    for hotelURL in soup.find_all("a", href=True, class_="hotel_name_link url"):
        hotelURLs = ("https://www.booking.com"+hotelURL["href"])
        hotelURL1, hotelURL2 = hotelURLs.split(".com")
        hotelURL2, hotelURL3 = hotelURL2.split("#")
        hotelURL2 = hotelURL2[:-1] + "#"
        hotelURL1 = hotelURL1 + ".com"
        hotelURL2 = hotelURL2[1:]
        hotelURLs = hotelURL1 + hotelURL2 + hotelURL3
        shortened_url = (hotelURLs.split(".html"))[0]
#        print(hotelURLs)
        c.execute("SELECT * FROM urls WHERE url like (? || '%')", (shortened_url,))
        check = c.fetchone()
        if check is None:
            c.execute("INSERT INTO urls (url) VALUES(?)",(hotelURLs,))
            conn.commit()
            new_urls += 1

    for nextPage in soup.find_all("a", href=True, class_="paging-next"):
        nextPageURL = (nextPage["href"])
        nextPageURL.replace(" ", "")

    if(nextPageURL == page):
        break
    else:
        page = nextPageURL
    i = i + 1
    print(i)

print("New Urls:" + str(new_urls))
c.close
conn.close()
