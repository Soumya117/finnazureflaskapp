import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import toHtml

def add_link(search):
    with open('links.json') as input:
        data = json.load(input)
        exists = False
        for item in data['links']:
            if search in item['link']:
                exists = True
                break
        if not exists:
            current = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            new_item = {}
            new_item['link'] = {}
            new_item['time'] = {}
            new_item['link'] = search
            new_item['time'] = current
            data['links'].append(new_item)
        
        with open('links.json', 'w') as output:
            json.dump(data, output)

def parseLink():        
    url = "https://www.finn.no/realestate/homes/search.html?location=0.20061"
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    type(soup)
    all_links = soup.find_all("a")
    all_ads = list()
    for link in all_links:
        if "ad.html" in link.get('href', ''):
           all_ads.append("https://www.finn.no"+link.get("href"))

    print("Total Ads: ", len(all_ads))
    for ad in all_ads:
       sample_url = ad
       if "newbuildings" in sample_url:
           continue
       #add url to the links.json
       add_link(sample_url)

def linkHtml():
    with open ('links.json') as output:
        data = json.load(output)
        toHtml.html(data, "finn_links")

def filterJson(date):
    start_date = date[0]
    end_date = date[1]
    filterData = {}
    filterData['links'] = []
    with open ('links.json') as output:
       data = json.load(output)
       count = 0
       for item in data['links']:
           time = item['time'].split('T')
           if start_date <= time[0] and time[0] <= end_date:
               new_item = {}
               new_item['link'] = {}
               new_item['time'] = {}
               count = count + 1
               new_item['link'] = item['link']
               new_item['time'] = item['time']
               filterData['links'].append(new_item)
    toHtml.html(filterData, "finn_links")

