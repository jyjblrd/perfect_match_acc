from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from xlwt import Workbook
import xlrd
import os
import re
import datetime
import time

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
numOfHotel = 210
name = ""
element = ""
elements = ""
page = ""
last_hotel_name = ""
max_num_of_rooms = 0
error_count = 0
checkin  = ["2019-02-15", "2019-02-22", "2019-03-04"] #February 15 2019, February 22 2019, March 4 2019
checkout = ["2019-02-21", "2019-02-28", "2019-03-10"] #February 21 2019, February 28 2019, March 10 2019

#Excel spreadsheet setup
wb = Workbook()
workbook = xlrd.open_workbook("/home/j_blrd/webscraping/urls.xls")
data_sheet = wb.add_sheet("data_sheet", cell_overwrite_ok=True)
sheet = workbook.sheet_by_index(0) #Open first sheet

#Get element from page with css selector function
def getElement(name, css_selector):
	global driver
	global element
	try:
		Wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
		element = driver.find_element_by_css_selector(css_selector).text
	except:
		print("Failed to find " + name)

#Get multiple elements from page with css selector function
def getElements(name, css_selector):
	global driver
	global elements
	try:
		Wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
		elements = driver.find_elements_by_css_selector(css_selector)
	except:
		print("Failed to find " + name)

#Main loop
for n in range(0,3):
	while(True):
		try:
			page = sheet.cell_value(row, 0)
		except:
			print("moving on to next date range", n)
			row = 1
			page = sheet.cell_value(row, 0)
			break
		page, page1 = page.split("#")
		page = page + "?label=gen173nr-1FCAEoggJCAlhYSDNYBGhiiAEBmAEuuAEKyAEF2AEB6AEB-AELkgIBeagCAw;sid=e572dfa99282705b4ee13a3f56c7a702;checkin=" + checkin[n] + ";checkout=" + checkout[n] + ";ucfs=1;srpvid=45542c48dc470139;srepoch=1524550674;highlighted_blocks=33254906_92852093_2_33_0;all_sr_blocks=33254906_92852093_2_33_0;bshb=2;room1=A%2CA;hpos=1;hapos=1;dest_type=city;dest_id=900039080;srfid=74d31266b708ab07c34010a2fbcb7fcccce3d058X1;from=searchresults;selected_currency=JPY;highlight_room=#hotelTmpl"
		driver.get(page)
		time.sleep(5)
		
		data_sheet.write(0, 0, "Accommodation No.")
		data_sheet.write(0, 1, "Accommodation Name")
		data_sheet.write(0, 2, "Booking.com Rating")
		data_sheet.write(0, 3, "Booking.com No. Reviews")
		data_sheet.write(0, 4, "No. Days")

		data_sheet.write(row, 0, row)
		
		getElement("hotel name", "#hp_hotel_name")
		hotel_name = element
		data_sheet.write(row, 1, element)
		print(element[:30])
		element = ""
		
		# Restart if hotel name cant be found
		if(hotel_name == ""):
			error_count += 1
			if(error_count > 3):
				row += 1
			continue

		getElement("rating", "#js--hp-gallery-scorecard > a > span > span.review-score-badge")
		data_sheet.write(row, 2, element)
		print(element)
		element = ""

		getElement("num of reviews", "#js--hp-gallery-scorecard > a > span > span.review-score-widget__body > span.review-score-widget__subtext")
		data_sheet.write(row, 3, element)
		print(element)
		element = ""
		
		data_sheet.write(row, 4, "8")

		
		getElements("all max people", "div.hprt-occupancy-occupancy-info")
		all_max_people = [x.get_attribute("data-title") for x in elements]
		all_max_people = [re.sub("\D", "", x) for x in all_max_people]
		all_max_people = [int(x) for x in all_max_people]
		print(all_max_people)
		elements = ""

		# Go to next hotel if it cant find max people
		if not all_max_people:
			# For some reason, Booking.com doesnt show suggested dates (Wait now it does! For some reason it started working once I got a new computer)
			getElement("suggested dates", "div.availability_price")
			try:
				suggested_nights, suggested_price = element.split(" nights from ")
				data_sheet.write(row, 5, suggested_nights)
				data_sheet.write(row, 6, suggested_price)
				print(element)
			except:
				pass
			element = ""
			row = row + 1
			continue
		
		getElements("all prices", "span.hprt-price-price-standard.jq_tooltip")
		elements = [x.text for x in elements]
		elements = [re.sub("\D", "", x) for x in elements]
		elements = [float(x) for x in elements]
		all_prices = elements
		print(all_prices)
		elements = ""
		
		getElements("all descriptions", "a.hprt-roomtype-link")
		all_descriptions = [x.text.replace("\n", "") for x in elements]
		print(all_descriptions)
		elements = ""
		
		num_of_rooms = len(all_prices)
		num_of_descriptions = len(all_descriptions)
		if(num_of_rooms > max_num_of_rooms):
			for a in range(0, num_of_rooms):
				data_sheet.write(0, (a * 3) + 7, "Price " + str(a))
				data_sheet.write(0, (a * 3) + 8, "Max People " + str(a))
				data_sheet.write(0, (a * 3) + 9, "Description " + str(a))
			max_num_of_rooms = num_of_rooms
		for a in range(0, num_of_rooms):
			data_sheet.write(row, (a * 3) + 7, all_prices[a])
			data_sheet.write(row, (a * 3) + 8, all_max_people[a])
			if(a < num_of_descriptions):
				data_sheet.write(row, (a * 3) + 9, all_descriptions[a])
			else:
				data_sheet.write(row, (a * 3) + 9, all_descriptions[num_of_descriptions-1])

		

		element = ""
		elements = ""
		min_price = ""
		max_price = ""
		num_of_rooms = ""
		page = ""
		last_hotel_name = hotel_name
		hotel_name = ""
		all_max_people = ""
		all_prices = ""
		all_descriptions = ""
		num_of_rooms = ""
		num_of_descriptions = ""
		row = row + 1
		error_count = 0
		print(row)
		print("\n")
		wb.save("/home/j_blrd/webscraping/spreadsheets/WebScrapingPropertyPricing" + str(n) + ".xls")
