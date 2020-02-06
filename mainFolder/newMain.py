from selenium import webdriver as wd
from selenium.webdriver.support.ui import Select
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import keys
# from mailmerge import MailMerge as mm
from bs4 import BeautifulSoup as bs
import urllib.request as urlR
import urllib.parse as urlP
import time
import re
import math
import secret # Secret.py file with email and password variable for finn.no
import os

window = 0
DELAY = 1
handledPages = []
driver = wd.Chrome()
actions = ActionChains(driver)


def init():
    url_string = 'https://www.finn.no/job/fulltime/search.html?extent=3942&location=1.20001.20012&location=2.20001.20012.20196'
    driver.get(url_string)

def find_easy_applications():
    divs = driver.find_elements_by_class_name('status.status--success.u-mb8')
    link_elements = []
    for entry in divs:
        parent = entry.find_element_by_xpath('..').find_element_by_xpath('..')
        parentLink = parent.find_element_by_class_name('ads__unit__link')
        href = parentLink.get_attribute('href')
        if href not in handledPages:
            link_elements.append(parent)
            print(href)
    return link_elements

def enter_easy_application(entry):
    entry.click()
    time.sleep(DELAY)
    handledPages.append(driver.current_url)
    driver.find_element_by_id('job-apply-button').click()
    time.sleep(DELAY)
    global window
    window += 1
    driver.switch_to_window(driver.window_handles[window])
    try:
        time.sleep(DELAY)
        driver.find_element_by_id('username').send_keys(secret.email)
        driver.find_element_by_id('password').send_keys(secret.password)
        driver.find_element_by_id('ActionButton_0').click()
        time.sleep(DELAY)
    except:
        pass
    driver.find_element_by_name('attachment.file').send_keys(os.getcwd()+"/cv.docx") # File upload, use for application
    Select(driver.find_element_by_name('education')).select_by_value('37')
    #driver.find_element_by_name('currentTitle').clear():
    driver.find_element_by_name('currentTitle').send_keys('Student')
    input('Press enter to continue')
    #######################################################################################
    #try:
    #    driver.find_element_by_class_name('button.primary').click() # Uncomment when ready
    #except:
    #    pass
    #######################################################################################
    time.sleep(DELAY)
    driver.switch_to_window(driver.window_handles[0])
    driver.back()
    time.sleep(DELAY)

def main():
    init()
    while True:
        entries = find_easy_applications()
        if len(entries) <= 0:
            break
        enter_easy_application(entries[0])
    print('Finished')