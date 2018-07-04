import sqlite3
import bs4 as bs
import os
import urllib.request
from time import sleep


page = "https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNYBGhiiAEBmAExwgEDYWJuyAEM2AED6AEB-AECkgIBeagCBA&sid=e0fb8230e5862b8cdc273f64c33475da&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Flabel%3Dgen173nr-1DCAEoggJCAlhYSDNYBGhiiAEBmAExwgEDYWJuyAEM2AED6AEB-AECkgIBeagCBA%3Bsid%3De0fb8230e5862b8cdc273f64c33475da%3Bclass_interval%3D1%3Bdest_id%3D900039080%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%26%3B&ac_presel=0&ss=Hakuba&ssne=Hakuba&ssne_untouched=Hakuba&city=900039080&checkin_month=2&checkin_monthday=17&checkin_year=2019&checkout_month=2&checkout_monthday=22&checkout_year=2019&group_adults=2&group_children=0&no_rooms=1"
i = 0
url_list = []

# Sqlite database initialization
conn = sqlite3.connect("/home/j_blrd/webscraping/database/urls.db")
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
        shortened_url = hotelURLs.split(".html")
        print(hotelURLs)
        if shortened_url[0] not in url_list:
            c.execute("INSERT INTO urls (url) VALUES(?)",(hotelURLs,))
            conn.commit()
        url_list.append(shortened_url[0])

    for nextPage in soup.find_all("a", href=True, class_="paging-next"):
        nextPageURL = (nextPage["href"])
        nextPageURL.replace(" ", "")

    if(nextPageURL == page):
        break
    else:
        page = nextPageURL
    i = i + 1
    print(i)

    if(i > 14):
        break

c.close
conn.close()
