from xlwt import Workbook
import xlrd
import bs4 as bs
import os
import urllib.request
from time import sleep


page = "https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggJCAlhYSDNYBGhiiAEBmAExwgEDYWJuyAEM2AED6AEB-AECkgIBeagCBA&sid=e0fb8230e5862b8cdc273f64c33475da&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.html%3Flabel%3Dgen173nr-1DCAEoggJCAlhYSDNYBGhiiAEBmAExwgEDYWJuyAEM2AED6AEB-AECkgIBeagCBA%3Bsid%3De0fb8230e5862b8cdc273f64c33475da%3Bclass_interval%3D1%3Bdest_id%3D900039080%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bgroup_adults%3D2%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%252CA%3Bsb_price_type%3Dtotal%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%26%3B&ac_presel=0&ss=Hakuba&ssne=Hakuba&ssne_untouched=Hakuba&city=900039080&checkin_month=2&checkin_monthday=17&checkin_year=2019&checkout_month=2&checkout_monthday=22&checkout_year=2019&group_adults=2&group_children=0&no_rooms=1"
row = 1
col = 1
i = 0
numOfHotel = 0

wb = Workbook()
sheet1 = wb.add_sheet("Hotel Urls")
sheet2 = wb.add_sheet("Hotel Keyword", cell_overwrite_ok=True)
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
        print(hotelURLs)
        sheet1.write(row,0,hotelURLs)
        row = row + 1
        numOfHotel = numOfHotel + 1

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

    
sheet1.col(0).width = 50000
wb.save("/home/j_blrd/Booking.com Webscraping/Spreadsheets/Hotel Urls booking.com.xls")

print("saving...")
sleep(5)
print("saved")
'''
workbook = xlrd.open_workbook("/home/jblrd/Python/Hotel Urls.xls")
sheet = workbook.sheet_by_index(0)

print("Hotel Keywords")
row = 1
while(True):
    if(row == numOfHotel):
        break
    page = sheet.cell_value(row, 0)
    source = urllib.request.urlopen(page)
    soup = bs.BeautifulSoup(source,"lxml")

    for h1 in soup.find_all("h1", class_="ui_header h1"):
        print(h1.text)
        sheet2.write(row,0,h1.text)
    
    for span in soup.find_all("span", class_="ui_tagcloud"):
        print(span.text)
        sheet2.write(row,col,span.text)
        col = col + 1

    for span in soup.find_all("span", class_="overallRating"):
        print(span.text)
        sheet2.write(row,18,span.text)

    for span in soup.find_all("span", class_="reviewCount"):
        print(span.text)
        sheet2.write(row,19,span.text)

    for b in soup.find_all("b", class_="rank"):
        print(b.text)
        sheet2.write(row,20,b.text)

    for div in soup.find_all("div", class_="bb_price_texthasStrikeThrough"):
        print(div.text)
        sheet2.write(row,21,div.text)
    
    row = row + 1
    col = 1

col = 0
width = 5000
while(col < 27):
    sheet2.col(col).width = width
    col = col + 1
    
wb.save("Hotel Keywords.xls ")
'''
print("Finished")
