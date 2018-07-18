#Python script to scrape comments for hotels in Hakuba, Japan from booking.com. Hopefully will be used in the billion dollar company perfect match acc.
#Written by Joshua Bird May 2018

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import datetime
import urllib.request
import os
import re
import time
import sys
import cProfile
import sqlite3
import bs4 as bs
import os
import urllib.request
from time import sleep

#Selenium with Firefox driver setup
options = Options()
options.add_argument("--headless")
firefox_profile = webdriver.FirefoxProfile()
binary = FirefoxBinary("/usr/bin/firefox")
firefox_profile.set_preference("permissions.default.stylesheet", 2)
firefox_profile.set_preference("permissions.default.image", 2)
firefox_profile.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "False")
driver = webdriver.Firefox(firefox_profile, firefox_binary=binary, firefox_options=options)
Wait = WebDriverWait(driver, 1.5)

#Defining variables
iteration = 0
element = ""
elements = ""
no_reviews = False
no_element = False
error_count = 0
page_num = 1
max_num_of_reviews = 0

#Sqlite setup
conn = sqlite3.connect("/home/j_blrd/webscraping/database/database.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS unfiltered_guest_comments\
          (location_id int, property_id int, review_site_id int, date text, comment text)")
c.execute("CREATE TABLE IF NOT EXISTS property_master_table\
          (location_id int, property_id int, property_name text, property_webadress text, hotel, self_contained)")
c.execute("CREATE TABLE IF NOT EXISTS sequence_tracker\
          (name text, seq int)")
c.execute("SELECT * FROM location_master_table")

#Get Url
print("\n" + "\n".join(str(s).replace("(", "").replace(")", "").replace("'", "").replace(",", "|") for s in c.fetchall()))  # Get location list
dest_name = input("Select location name from list above:\n")
page = "https://www.booking.com/searchresults.en-gb.html?lang=en-gb&ss={}".format(dest_name)
c.execute("SELECT location_id FROM location_master_table WHERE location_name = '{}'".format(dest_name))
location_id = int(c.fetchone()[0])
print(location_id)


#Set all variables to nothing to prevent previous hotel's info bleeding into next hotel
def clearVariables():
    global element
    global elements
    global hotel_url
    global comment_url
    global name
    global overall_rating
    global individual_ratings
    global cleanliness
    global comfort
    global location
    global facilities
    global staff
    global value
    global wifi
    global reviewer_info
    global review_score
    global num_of_reviews
    global review_date
    global link_to_review
    global review_title
    global review_text
    global no_reviews
    global no_element
    global newest_date

    element = ""
    elements = ""
    hotel_url = ""
    comment_url = ""
    name = ""
    overall_rating = ""
    individual_ratings = ""
    cleanliness = ""
    comfort = ""
    location = ""
    facilities = ""
    staff = ""
    value = ""
    wifi = ""
    reviewer_info = ""
    review_score = ""
    num_of_reviews = 0
    review_date = ""
    link_to_review = ""
    review_title = ""
    review_text = ""
    no_reviews = False
    no_element = False
    newest_date = ""


#Setup to get rid of the stupid emojies
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

#Get Url
print("Getting Urls")
print("Page:")
previous_urls = {}
previous_urls = set()
hotel_urls = []
i = 0
repeat_url = 0

while(True):
    source = urllib.request.urlopen(page)
    soup = bs.BeautifulSoup(source, "lxml")

    for hotelURL in soup.find_all("a", href=True, class_="hotel_name_link url"):
        hotelURLs = ("https://www.booking.com" + hotelURL["href"])
        hotelURL1, hotelURL2 = hotelURLs.split(".com")
        hotelURL2, hotelURL3 = hotelURL2.split("#")
        hotelURL2 = hotelURL2[:-1] + "#"
        hotelURL1 = hotelURL1 + ".com"
        hotelURL2 = hotelURL2[1:]
        hotelURLs = hotelURL1 + hotelURL2 + hotelURL3
        shortened_url = hotelURLs.split(".html")[0]
        if shortened_url not in previous_urls:
            previous_urls.add(shortened_url)
            hotel_urls.append(hotelURLs)
        else:
            repeat_url += 1

    for nextPage in soup.find_all("a", href=True, class_="paging-next"):
        nextPageURL = (nextPage["href"])
        nextPageURL.replace(" ", "")

    if(nextPageURL == page):
        break
    else:
        page = nextPageURL
    i = i + 1
    print(i)
i = 0  # Dont resue variables like me
print("New hotels in " + dest_name + " " + str(len(hotel_urls)))
print("Repeat urls: " + str(repeat_url))

#Get element from page with css selector function


def getElement(name, css_selector):
    global driver
    global element
    global no_element
    try:
        Wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        element = driver.find_element_by_css_selector(css_selector).text
    except BaseException:
        print("Failed to find " + name)
        no_element = True

#Get element from page with xpath function


def getElementXpath(name, xpath):
    global driver
    global element
    try:
        Wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element_by_xpath(xpath).text
    except BaseException:
        print("Failed to find " + name)

#Get multiple elements from page with css selector function


def getElements(name, css_selector):
    global driver
    global elements
    global no_reviews
    try:
        Wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        elements = driver.find_elements_by_css_selector(css_selector)
    except BaseException:
        print("Failed to find " + name)
        if(name == "review date"):  # If it cant find reviews, it skips over the hotel
            no_reviews = True

#Get multiple elements from page with xpath function


def getElementsXpath(name, xpath):
    global driver
    global elements
    try:
        Wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        elements = driver.find_elements_by_xpath(xpath)
    except BaseException:
        print("Failed to find " + name)


#Main loop
while(True):
    #startup stuff
    conn.commit()
    clearVariables()

    if(page_num == 1):  # get the hotel name, rating, ect is only needed once
        hotel_url = hotel_urls[iteration]  # Gets the next hotel url
        hotel_name = hotel_url.split("?")[0].split("/")[-1]
        country_code = hotel_url.split("?")[0].split("/")[-2]
        comment_url = "https://www.booking.com/reviews/" + country_code + "/hotel/" + hotel_name  # Splice hotel name onto url

        driver.get(comment_url)  # Get Page
        getElement("hotel name", ".standalone_header_hotel_link")
        name = element
        element = ""
        print("\n" + name)

        getElement("overall rating", "#review_list_score > span > span")
        if no_element is True:  # If there is no overall rating it just skips the hotel
            no_element = False
            iteration += 1
            page = 1
            continue

        overall_rating = element
        element = ""
        #print(overall_rating) #Debugging only, slows down program a bit

        # Check if hotel is already in db
        c.execute("SELECT property_id FROM property_master_table WHERE property_name = ? LIMIT 1", (name,))
        entry = c.fetchone()

        if entry is None:
            # Sequence counting stuff
            sequence_name = "property_master_table_location_" + str(location_id)
            c.execute("SELECT seq FROM sequence_tracker WHERE name = ? LIMIT 1", (sequence_name,))  # Check if sequence already exist
            entry = c.fetchone()

            if entry is None:
                c.execute("INSERT INTO sequence_tracker (name, seq) VALUES(?, 1)", (sequence_name,))
                entry = [0]
            property_id = int(entry[0]) + 1
            c.execute("UPDATE sequence_tracker SET seq = ? WHERE name = ?", (property_id, sequence_name))

            # Putting stuff in propeerty_master_table
            c.execute("INSERT INTO property_master_table (location_id, property_id, property_name) VALUES(?, ?, ?)",
                      (location_id, property_id, name))
        else:
            print("hotel already in db")
            property_id = int(entry[0])
            print(property_id)

        getElements("individual rating", "p.review_score_value")
        individual_ratings = [x.text for x in elements]
        if(len(individual_ratings) == 8):
            pass  # ToDo: add this to the database

        elif(len(individual_ratings) == 7):  # Some hotels dont have a wifi score
            pass
            #ToDo: same as above
            #print("no wifi score")
            #c.executemany("INSERT INTO comments \
            #    (hotel_name, overall, cleanliness, comfort, location, facilities, staff, value) \
            #    VALUES (?, ?, ?, ?, ?, ?, ?, ?)", individual_ratings)

        #print(individual_ratings) #Debugging only, slows down program a bit
        elements = ""

        c.execute("SELECT date FROM unfiltered_guest_comments WHERE location_id = ? AND property_id = ?",
                  (location_id, property_id))  # Get all dates for the previous comments
        newest_date = int(max([x[0] for x in c.fetchall()], default = 0))

    print(page_num)
    print(newest_date)

    getElements("review date", "p.review_item_date")
    if no_reviews is False:  # If there are no reviews get them
        review_date = [int(time.mktime(datetime.strptime(x.text[10:], "%d %B %Y").timetuple())) for x in elements]  # Converts "16 July 2018" to unix time
        reviewer_info = [[x] for x in review_date]
        element = ""

        num_of_reviews = len(reviewer_info)

        getElements("review text", "div.review_item_review_content")
        review_text = [x.text.replace("눇", "").replace("눉", "").replace("\n", " ").split(" Stayed in ", 1)[0] for x in elements]  # replace the weird unicode and carriage returns
        review_text = [(emoji_pattern.sub(r"", x)) for x in review_text]  # Gets rid of the emojis
        for i in range(0, num_of_reviews):
            reviewer_info[i].append(review_text[i])  # Add review text to the list
        elements = ""

        reviewer_info.sort(reverse = True)

        review_date = [x[0] for x in reviewer_info]

        try:
            target_index = review_date.index(newest_date)
        except ValueError:
            target_index = None

        print("Added " + str(target_index) + " new comments")
        reviewer_info[:target_index]


        for a in range(0, num_of_reviews):
            c.execute("INSERT INTO unfiltered_guest_comments (location_id, property_id, date, comment) VALUES(?, ?, ?, ?)",
                      (location_id, property_id, reviewer_info[a][0], reviewer_info[a][1]))
#            c.execute("INSERT INTO unfiltered_guest_comments (
#            print(reviewer_info[a]) #Print collected data (for debugging only. Slows down program because it has to print so much

        #c.executemany("INSERT INTO comments VALUES (

    try:  # Try to get next page of reviews
        driver.find_element_by_css_selector("div.review_list_pagination:nth-child(4) > p:nth-child(2) > a:nth-child(1)").click()
        if target_index:
            page_num = 1
            iteration += 1
        else:
            page_num += 1  # Next page
    except BaseException:  # Move onto next page
        page_num = 1
        iteration += 1

c.close()
conn.close()
driver.quit()
