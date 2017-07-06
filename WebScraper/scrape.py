from bs4 import BeautifulSoup
from decimal import Decimal
import requests
import json

import urllib2, sys



states = [
         'Alabama','Alaska'
         ,'Arizona','Arkansas','California','Colorado',
         'Connecticut','Delaware','District of Columbia','Florida','Georgia',
         'Hawaii','Idaho', 'Illinois','Indiana','Iowa','Kansas','Kentucky',
         'Louisiana', 'Maine', 'Maryland','Massachusetts','Michigan',
         'Minnesota', 'Mississippi', 'Missouri','Montana','Nebraska','Nevada',
         'New Hampshire','New Jersey','New Mexico','New York',
         'North Carolina','North Dakota','Ohio',
         'Oklahoma','Oregon','Pennsylvania','Rhode Island',
         'South Carolina','South Dakota','Tennessee','Texas','Utah',
         'Vermont','Virginia','Washington','West Virginia',
         'Wisconsin','Wyoming'
    ]

usDict = {}
for state in states:

    # print(" ")
    # print(" ")
    # print("-------------------------")
    # print(" ")
    # print(state)

    newState = '-'.join(state.split(" "))
    site= "http://www.newamericaneconomy.org/locations/"+newState+"/"
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(site,headers=hdr)
    page = urllib2.urlopen(req)

    #url = raw_input("Enter a state to extract info from: ")
    #r  = requests.get("http://www.newamericaneconomy.org/locations/"+url)
    #r  = requests.get("http://www.newamericaneconomy.org/locations/pennsylvania/")
    #data = r.text


    soup = BeautifulSoup(page, "html.parser")

    stateDict = {}


    for intro in soup.find_all("p", { "class" : "district__intro-text" }):
        stateDict["info"] = intro.text
        # print(intro.text)

    for listStats in soup.find_all("li", { "class" : "district__stats-grid-item" }):
        stats = listStats.text.split("\n")
        key = stats[2]
        if "Employees at Immigrant-Owned Firms" in key:
            key = "Employees at Immigrant-Owned Firms"
        stateDict[key] = stats[3]
        # print(stats[2])
        # print(stats[3])


    #Scrapping demographics information
    for demographics in soup.find_all("section", {"id" : "demographics"}):

        title = demographics.find_all("h2", {"class" : "district__section-h"})
        # print title[0].text
        text = demographics.find_all("p", {"class" : "district__text"})
        # print text[0].text

        '''tableHead = demographics.find_all("thead", {"class" : "table__head"})
        heads = tableHead[0].text.split("\n")
        print heads[2]
        print heads[3]
        print heads[4]'''

        stats = {}
        secondColumn = ""
        thirdColumn = ""
        demoInfo = demographics.find_all("tr", {"class" : "table__row"})
        for info in demoInfo:
            elements = info.text.split("\n")

            if (secondColumn == ""):
                secondColumn = elements[2]
                thirdColumn = elements[3]
            else:
                stats[elements[1]] = {secondColumn: elements[2], thirdColumn: elements[3]}

            # print elements[1]
            # print elements[2]
            # print elements[3]

        demo = {}
        demo["info"] = text[0].text
        demo["stats"] = stats
        stateDict[title[0].text] = demo


    #Scrapping Entrepreneurship information
    for entrepreneurship in soup.find_all("section", {"id" : "entrepreneurship"}):

        title = entrepreneurship.find_all("h2", {"class" : "district__section-h"})
        # print title[0].text
        text = entrepreneurship.find_all("p", {"class" : "district__text"})
        # print text[0].text

        '''tableHead = demographics.find_all("thead", {"class" : "table__head"})
        heads = tableHead[0].text.split("\n")
        print heads[2]
        print heads[3]
        print heads[4]'''

        entre = {}
        entreInfo = entrepreneurship.find_all("tr", {"class" : "table__row"})
        for info in entreInfo:
            elements = info.text.split("\n")
            if len(elements) > 2:
                # print elements[1]
                # print elements[2]
                entre[elements[1]] = elements[2]

        entre["info"] = text[0].text
        stateDict[title[0].text] = entre

    #Scrapping Tax Spending information
    for tax_spending in soup.find_all("section", {"id" : "taxes-&-spending-power"}):
        title = tax_spending.find_all("h2", {"class" : "district__section-h"})
        # print title[0].text
        text = tax_spending.find_all("p", {"class" : "district__text"})
        # print text[0].text

        '''tableHead = demographics.find_all("thead", {"class" : "table__head"})
        heads = tableHead[0].text.split("\n")
        print heads[2]
        print heads[3]
        print heads[4]'''

        taxSpend = {}
        taxInfo = tax_spending.find_all("tr", {"class" : "table__row"})
        for info in taxInfo:
            elements = info.text.split("\n")
            if len(elements) > 2:
                # print elements[1].replace(u" \u2014 ",u"")
                # print elements[2]
                taxSpend[elements[1].replace(u" \u2014 ",u"")] = elements[2]

        taxSpend["info"] = text[0].text
        stateDict[title[0].text] = taxSpend

    #Scrapping workforce information
    for workforce in soup.find_all("section", {"id" : "workforce"}):
        title = workforce.find_all("h2", {"class" : "district__section-h"})
        # print title[0].text
        text = workforce.find_all("p", {"class" : "district__text"})
        # print text[0].text

        '''tableHead = demographics.find_all("thead", {"class" : "table__head"})
        heads = tableHead[0].text.split("\n")
        print heads[2]
        print heads[3]
        print heads[4]'''

        stats = {}
        secondColumn = ""
        thirdColumn = ""
        workforceInfo = workforce.find_all("tr", {"class" : "table__row"})
        for info in workforceInfo:
            elements = info.text.split("\n")
            if elements[1] == "Top Industries with Highest Share of Foreign-Born Workers":
                break;

            if (secondColumn == ""):
                secondColumn = elements[2]
                thirdColumn = elements[3]
            else:
                stats[elements[1]] = {secondColumn: elements[2], thirdColumn: elements[3]}
            # print elements[1]
            # print elements[2]
            # print elements[3]

        work = {}
        work["info"] = text[0].text
        work["stats"] = stats
        stateDict[title[0].text] = work



    #Scrapping undocummented immigrants information
    for und_immigrants in soup.find_all("section", {"id" : "undocumented-immigrants"}):
        title = und_immigrants.find_all("h2", {"class" : "district__section-h"})
        # print title[0].text
        text = und_immigrants.find_all("p", {"class" : "district__text"})
        # print text[0].text

        '''tableHead = demographics.find_all("thead", {"class" : "table__head"})
        heads = tableHead[0].text.split("\n")
        print heads[2]
        print heads[3]
        print heads[4]'''

        uImm = {}
        uImmInfo = und_immigrants.find_all("tr", {"class" : "table__row"})
        for info in uImmInfo:
            elements = info.text.split("\n")
            if len(elements) > 2:
                # print elements[1].replace(u" \u2014 ",u"")
                # print elements[2]
                uImm[elements[1].replace(u" \u2014 ",u"")] = elements[2]

        uImm["info"] = text[0].text
        stateDict[title[0].text] = uImm

    usDict[state] = stateDict



d = {
    'M': 6,
    'B': 9}
def text_to_num(text):
    if text[-1] in d:
        num, magnitude = text[:-1], text[-1]
        return Decimal(num) * 10 ** d[magnitude]
    else:
        return Decimal(text)

import math

millnames = ['',' Th',' M',' B',' Tr']
def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

totalImmigrants = 0
totalPopulation = 0
totalImmigrantsEntrepeneurs = 0
totalEmployees = 0
totalTaxesPaid = 0
totalSpendingPower = 0
for stateInfo in usDict:
    totalTaxesPaid += text_to_num(usDict[stateInfo]["Immigrant Taxes Paid (2014)"].replace("$",""))
    totalSpendingPower += text_to_num(usDict[stateInfo]["Immigrant Spending Power (2014)"].replace("$",""))
    totalImmigrants += int(usDict[stateInfo]["Immigrant Residents"].replace(",",""))
    totalPopulation += (int(usDict[stateInfo]["Immigrant Residents"].replace(",",""))/float(usDict[stateInfo]["Immigrant Share of Population"].replace("%","")))*100
    totalImmigrantsEntrepeneurs += int(usDict[stateInfo]["Immigrant Entrepreneurs"].replace(",",""))
    if "Employees at Immigrant-Owned Firms" in usDict[stateInfo]:
        totalEmployees += int(usDict[stateInfo]["Employees at Immigrant-Owned Firms"].replace(",",""))




# print totalImmigrants
# print totalPopulation
# print totalImmigrantsEntrepeneurs
# print totalEmployees
# print totalTaxesPaid
# print totalSpendingPower

us = {}
us["Immigrant Residents"] = totalImmigrants
us["Total population"] = int(totalPopulation)
us["Immigrant Share of Population"] = str(round((totalImmigrants/totalPopulation)*100,2))+"%"
us["Immigrant Entrepreneurs"] = totalImmigrantsEntrepeneurs
us["Employees at Immigrant-Owned Firms"] = totalEmployees
us["Immigrant Taxes Paid (2014)"] = "$"+millify(totalTaxesPaid)
us["Immigrant Spending Power (2014)"] = "$"+millify(totalSpendingPower)

usDict["US"] = us

jsonUS = json.dumps(usDict)
print jsonUS
