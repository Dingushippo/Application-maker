from selenium import webdriver as wd
from selenium.webdriver.support.ui import Select
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import keys
from mailmerge import MailMerge as mm
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

#Testing standard values
nameStr = "Daniel Bjørge"
numStr = "94471045"
emailStr = "danbjo23@gmail.com"

def init(test):
    url_string = 'https://www.finn.no/job/fulltime/search.html?extent=3942&location=1.20001.20012&location=2.20001.20012.20196'
    driver.get(url_string)
    if not test:
        global nameStr
        nameStr = input('Full name: ')
        global numStr
        numStr = input('Phone number: ')
        global emailStr
        emailStr = input('E-mail: ')
    

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
    application = make_application()
    handledPages.append(driver.current_url)
    time.sleep(DELAY)
    driver.find_element_by_id('job-apply-button').click()
    time.sleep(DELAY)
    global window
    window += 1
    try:
        driver.switch_to_window(driver.window_handles[window])
    except:
        driver.switch_to_window(driver.window_handles[0])
    try:
        time.sleep(DELAY)
        driver.find_element_by_id('username').send_keys(secret.email)
        driver.find_element_by_id('password').send_keys(secret.password)
        driver.find_element_by_id('ActionButton_0').click()
        time.sleep(DELAY)
    except:
        pass
    driver.find_element_by_name('attachment.file').send_keys(os.getcwd() + "/cv.docx") # File upload, use for application
    
    Select(driver.find_element_by_name('education')).select_by_value('37')
    #driver.find_element_by_name('currentTitle').clear():
    driver.find_element_by_name('currentTitle').send_keys('Student')
    part = application.split("/")
    openFile = part[0] + '\\' + part[1]
    os.startfile(openFile)
    input('Review application, and press enter to continue')
    driver.find_element_by_name('attachment.file').send_keys(os.getcwd() + "/" + application)
    input('Press enter to apply (close tab to cancel)')
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

def make_application():
    document = mm("application_template.docx")
    infoList = driver.find_elements_by_class_name("definition-list")
    mainInfoDic = {}
    for entry in infoList:
        info = entry.text.split('\n')
        for i in range(0, len(info), 2):
            try:
                mainInfoDic.update({info[i]: info[i + 1]})
            except:
                pass
    print(mainInfoDic)
    if '/' in mainInfoDic.get('Arbeidsgiver'):
        sub = mainInfoDic.get('Arbeidsgiver')[0: mainInfoDic.get('Arbeidsgiver').index('/')-1]
        mainInfoDic['Arbeidsgiver'] = sub
    docName = f"applications/{mainInfoDic.get('Arbeidsgiver')}.docx"
    document.merge(
        date='{:%d-%b-%Y}'.format(date.today()),
        location=mainInfoDic.get("Sted"),
        company=mainInfoDic.get("Arbeidsgiver"),  
        name=nameStr, 
        email=emailStr, 
        number=numStr)
    document.write(docName)
    return docName


def main(test=False):
    init(test)
    while True:
        entries = find_easy_applications()
        if len(entries) <= 0:
            break
        enter_easy_application(entries[0])
        if test:
            break
    print('Finished')