from selenium import webdriver as wd
from datetime import date
# from mailmerge import MailMerge as mm
from bs4 import BeautifulSoup as bs
import urllib.request as urlR
import urllib.parse as urlP
import time
import re
import math

def initialize():
    driver = wd.Chrome()

def primes():
    k = 0
    run = True
    primeList = [2,3]
    startTime = time.time()
    max = int(input("Max number: "))
    while run < max:
        k += 1
        a = 6*k-1
        b = 6*k+1
        addA =True
        addB =True
        for num in primeList:
            if a%num == 0:
                addA=False
                break
            if b%num == 0:
                addB=False
                break
        if a > max or b > max:
            break
        if addA:
            primeList.append(a)
        if addB:
            primeList.append(b)
    print("Time: " + str(time.time()-startTime))    
    return primeList    
    
    
        
        
