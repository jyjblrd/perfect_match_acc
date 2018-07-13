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
import urllib.request
import os
import re
import time
import sys
import cProfile
import sqlite3

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
conn = sqlite.connect("/home/j_blrd/webscraping/database/database.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS comments\
          (hotel_name TEXT, overall TEXT, cleanliness TEXT, comfort TEXT, location TEXT, facilities TEXT, staff TEXT, value TEXT, wifi TEXT)")

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

#Setup to get rid of the stupid emojies
emoji_pattern = re.compile("["
               u"\U0001F600-\U0001F64F"  # emoticons
               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
               u"\U0001F680-\U0001F6FF"  # transport & map symbols
               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
               "]+", flags=re.UNICODE)

#Get element from page with css selector function
def getElement(name, css_selector):
    global driver
    global element
    global no_element
    try:
        Wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        element = driver.find_element_by_css_selector(css_selector).text
    except:
        print("Failed to find " + name)
        no_element = True

#Get element from page with xpath function
def getElementXpath(name, xpath):
    global driver
    global element
    try:
        Wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element_by_xpath(xpath).text
    except:
        print("Failed to find " + name)

#Get multiple elements from page with css selector function
def getElements(name, css_selector):
    global driver
    global elements
    global no_reviews
    try:
        Wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        elements = driver.find_elements_by_css_selector(css_selector)
    except:
        print("Failed to find " + name)
        if(name == "reviewer info"): #If it cant find reviews, it skips over the hotel
            no_reviews = True

#Get multiple elements from page with xpath function
def getElementsXpath(name, xpath):
    global driver
    global elements
    try:
        Wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        elements = driver.find_elements_by_xpath(xpath)
    except:
        print("Failed to find " + name)

#Get the hotel urls from the database
c.execute("SELECT url FROM urls") #Selects the urls in database
hotel_urls = c.fetchall()

#Main loop
while(True):
    if(page_num == 1): #get the hotel name, rating, ect is only needed once
        hotel_url = hotel_urls[iteration] #Gets the next hotel url
        hotel_name = hotel_url[:-10][33:] #Get rid of everything in the url but the hotel name
        comment_url = "https://www.booking.com/reviews/jp/hotel/" + hotel_name #Splice hotel name onto url
        driver.get(comment_url) #Get Page

        getElement("hotel name", ".standalone_header_hotel_link")
        name = element
        element = ""
        print(name)

        getElement("overall rating", "#review_list_score > span > span")
        if(no_element == True): #If there is no overall rating it just skips the hotel
            no_element = False
            iteration += 1
            print(iteration)
            continue

        overall_rating = element
        element = ""
        #print(overall_rating) #Debugging only, slows down program a bit

        getElements("individual rating", "p.review_score_value")
        individual_ratings = [x.text for x in elements]
        if(len(individual_ratings) == 8):
            c.executemany("INSERT INTO comments \
                (hotel_name, overall, cleanliness, comfort, location, facilities, staff, value, wifi) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", individual_ratings)

        elif(len(individual_ratings) == 7): #Some hotels dont have a wifi score
            print("no wifi score")
            c.executemany("INSERT INTO comments \
                (hotel_name, overall, cleanliness, comfort, location, facilities, staff, value) \
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)", individual_ratings)

        #print(individual_ratings) #Debugging only, slows down program a bit
        elements = ""

    print("page: ", page_num)
    getElements("reviewer info", "div.review_item_reviewer")
    if(no_reviews == False): #If there are no reviews get them
        reviewer_info = [x.text for x in elements]
        reviewer_info = [x.split("\n") for x in reviewer_info] #Split the name, country and num of reviews into seperate parts
        reviewer = reviewer_info
        elements = ""

        getElements("review score", "span.review-score-badge")
        review_score = [x.text for x in elements]
        del review_score[0] #delete the first element in list because it is the overall score (same css selector)
        num_of_reviews = len(reviewer_info)
        for i in range(0, num_of_reviews): #runs as many times as there are reviews on the page.
            reviewer_info[i].append(review_score[i]) #Add the review score to the list
        elements = ""

        getElements("review date", "p.review_item_date")
        review_date = [x.text for x in elements]
        for i in range(0, num_of_reviews):
            reviewer_info[i].append(review_date[i]) #Add the review date to the list
        elements = ""

        getElements("link to review", "a.review_item_header_content")
        link_to_review = [x.get_attribute("href") for x in elements]
        for i in range(0, num_of_reviews):
            reviewer_info[i].append(link_to_review[i]) #Add link to review to the list
        elements = ""

        for i in range(0, num_of_reviews):
            getElementXpath("review title", '//*[@id="review_list_page_container"]/ul/li['+str(i+1)+']/div[4]/div/div[1]/div[2]/a/span')
            review_title = (emoji_pattern.sub(r"", element)) #Gets rid of the emojis that were crashing the program
            element = ""
            reviewer_info[i].append(review_title) #Add the review title to the list

        getElements("review text", "div.review_item_review_content")
        review_text = [x.text.replace("눇", "").replace("눉", "").replace("\n", " ").split(" Stayed in ", 1)[0] for x in elements] #replace the weird unicode and carriage returns
        review_text = [(emoji_pattern.sub(r"", x)) for x in review_text] #Gets rid of the emojis
        for i in range(0, num_of_reviews):
            reviewer_info[i].append(review_text[i]) #Add review text to the list
        elements = ""

        for a in range(0, num_of_reviews):
            c.execute(CREATE TABLE IF NOT EXISTS
#            print(reviewer_info[a]) #Print collected data (for debugging only. Slows down program because it has to print so much

        c.executemany("INSERT INTO comments VALUES (

    try: #Try to get next page of reviews
            driver.find_element_by_css_selector("div.review_list_pagination:nth-child(4) > p:nth-child(2) > a:nth-child(1)").click()
        clearVariables()
        page_num += 1 #Next page
    except: #Move onto next page
        row += 1
        spreadsheet_row += 1
        print("")
        print("Hotel number ", row)
        wb.save("/home/j_blrd/webscraping/spreadsheets/comments.xls")
        page_num = 1
        clearVariables()
#This is a bad workaround but it works

driver.quit()
