import urllib.request
import urllib.parse
import re
import time
from datetime import date
from mailmerge import MailMerge
from bs4 import BeautifulSoup


template = "mainFolder/application_template.docx"
search_url = "https://no.jooble.org/jobb-ekstrahjelper%2Fbutikkselger-deltid/Stavanger?p="  # plus pagenumber
target_string = "ckey=ekstrahjelper%2fbutikkselger+deltid"
numOfLinks = 0
numOfPagesSearched = int(input("Number of pages you want searched (max 41 atm): "))
linkRecurrence = {}
start_time = time.time()
for i in range(numOfPagesSearched):
    links = []
    html_page = urllib.request.urlopen(search_url + str(i))
    soup_main = BeautifulSoup(html_page, features="lxml")
    for link in soup_main.findAll('a', attrs={'href': re.compile("^https://")}):
        if target_string in link.get('href'):
            numOfLinks += 1
            links.append(link.get('href'))

    for link in links:
        valueList = []
        html_page = urllib.request.urlopen(link)
        soup_page = BeautifulSoup(html_page, features="lxml")
        values = soup_page.findAll(attrs={'class' : 'value-column'})
        for value in values:
            valueList.append(value.text.strip())
        company = valueList[0]
        if company == "Stavanger" or company == "Sandnes" or "/" in company or "|" in company:
            continue
        if company not in linkRecurrence:
            linkRecurrence[company] = 0
            name = company
        else:
            linkRecurrence[company] = linkRecurrence.get(company) + 1
            name = f"{company}_{linkRecurrence.get(company)}"


        print(f"Handling: {company}")
        location = valueList[1]
        document = MailMerge(template)
        document.merge(date='{:%d-%b-%Y}'.format(date.today()), company=company, link=link)
        document.write(f"mainFolder/applications/{name}.docx")

print(f"Number of links handled: {numOfLinks}, time elapsed: {int(time.time()-start_time)}s")
print(f"Efficiency: {numOfLinks/int(time.time()-start_time)} applications per second")
