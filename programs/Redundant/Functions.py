#Functions for "Comment Scraping" program
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
from CommentScraping import *

#Get element from page with css selector function
def getElement(name, css_selector):
    global driver
    global element
    global no_element
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        element = driver.find_element_by_css_selector(css_selector).text
    except:
        print("Failed to find " + name)
        no_element = True

#Get element from page with cpath function
def getElementXpath(name, xpath):
    global driver
    global element
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element_by_xpath(xpath).text
    except:
        print("Failed to find " + name)

#Get multiple elements from page with css selector function
def getElements(name, css_selector):
    global driver
    global elements
    global no_reviews
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
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
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        elements = driver.find_elements_by_xpath(xpath)
    except:
        print("Failed to find " + name)


