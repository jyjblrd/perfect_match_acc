#Scraping Accommodation Pictures and Website Adresses
#Written By Joshua Bird May 2018

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
from xlwt import Workbook
from PIL import Image
import xlrd
import urllib.request
import os
import re
import datetime
import sys

#Selenium with Firefox driver setup
options = Options()
options.add_argument("--headless")
firefox_profile = webdriver.FirefoxProfile()
binary = FirefoxBinary("/usr/bin/firefox")
firefox_profile.set_preference("permissions.default.stylesheet", 2)
firefox_profile.set_preference("permissions.default.image", 2)
firefox_profile.set_preference("dom.ipc.plugins.enabled.libflashplayer.so", "False")
driver = webdriver.Firefox(firefox_profile, firefox_binary=binary, firefox_options=options)
Wait = WebDriverWait(driver, 3)

#Defining variables
row = 1
col = 2
element = ""
elements = ""

#Excel spreadsheet setup
wb = Workbook()
workbook = xlrd.open_workbook("/home/j_blrd/webscraping/spreadsheets/comments.xls")
data_sheet = wb.add_sheet("imagesAndWebsites", cell_overwrite_ok=True)
sheet = workbook.sheet_by_index(0) #Open first sheet
data_sheet.write(0, 0, "#")
data_sheet.write(0, 1, "Hotel Name")
data_sheet.write(0, 2, "Hotel Website")
data_sheet.write(0, 3, "Hotel Picture")
data_sheet.write(0, 4, "Hotle Picture Url")

def clearVariables():
		
	global element
	global elements
	global hotel_website
	global hotel_name
	global hotel_url
	global hotel_url_with_plus
	global hotel_image_url
	
	element = ""
	elements = ""
	hotel_website = ""
	hotel_name = ""
	hotel_url = ""
	hotel_url_with_plus = ""
	hotel_image_url = ""

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

#Get link from page with class name function
def getElementAttribute(name, css_selector, attribute):
    global driver
    global element
    try:
        Wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        element = driver.find_element_by_css_selector(css_selector).get_attribute(attribute)
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

#Get multiple elements from page with xpath function
def getElementsXpath(name, xpath):
    global driver
    global elements
    try:
        Wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        elements = driver.find_elements_by_xpath(xpath)
    except:
        print("Failed to find " + name)

#Main loop
while(True):
	hotel_name = sheet.cell_value(row, 0) #Get the hotel name from booking.com comments spreadsheet
	if hotel_name.find("Hakuba") == -1:
		hotel_name = hotel_name + " Hakuba"
	hotel_name_with_plus = hotel_name.replace(" ", "+") #Replace spaces with + so it can be inserted into google url
	print(hotel_name) #Print Hotel Name
	
	hotel_url = "https://www.google.com/search?rlla=0&tbm=lcl&hl=en&q=" + hotel_name_with_plus #Splice hotel name onto google maps search url
	driver.get(hotel_url) #Get Page
	
	getElementAttribute("hotel's website", "a.yYlJEf.L48Cpd", "href") #Try find hotel's website element
	hotel_website = element
	element = ""
	print(hotel_website)
	
	getElementAttribute("image of hotel", "div.hDtdnc", "style") #Try get the link to the image of the hotel
	hotel_image_url = element[23:][:-3]
	if("https:" in hotel_image_url) != True and hotel_image_url != "": #For some reason some of the url's dont have https: at the beginning so this just adds that
		hotel_image_url = "https:" + hotel_image_url
	element = ""
	print(hotel_image_url)
	
	if(hotel_image_url != ""): #Get the image from the link only if there is an image
		urllib.request.urlretrieve(hotel_image_url, "/home/j_blrd/webscraping/imageCache/" + hotel_name + ".png") #Get the link of the image and download it
		img = Image.open("/home/j_blrd/webscraping/imageCache/" + hotel_name + ".png")
		r, g, b = img.split()
		img = Image.merge("RGB", (r, g, b))
		img.save("/home/j_blrd/webscraping/imageCache/" + hotel_name + ".bmp")
		data_sheet.insert_bitmap("/home/j_blrd/webscraping/imageCache/" + hotel_name + ".bmp", row, 3)
	
	#Start writing data to spreadsheet
	data_sheet.write(row, 0, row)
	data_sheet.write(row, 1, hotel_name)
	data_sheet.write(row, 2, hotel_website)
	data_sheet.write(row, 4, hotel_image_url)
	
	wb.save("/home/j_blrd/webscraping/spreadsheets/imagesAndWebsites.xls")
	
	print("\n")
	clearVariables()
	row += 1
	print(row)
	
	
