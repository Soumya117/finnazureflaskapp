import sys
import json
from urllib import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import libHtml
import os

link = os.path.join("json","links.json")
def add_link(search):
    with open(link) as input:
        data = json.load(input)
        exists = False
        for item in data['links']:
            if search in item['link']:
                exists = True
                break
        if not exists:
            current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            new_item = {}
            new_item['link'] = {}
            new_item['time'] = {}
            new_item['link'] = search
            new_item['time'] = current
            data['links'].append(new_item)
        
        with open(link, 'w') as output:
            json.dump(data, output)

def add_title(result):
    with open("json/realestates.json") as input:
        data = json.load(input)
        current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        for item in data['links']:
            if result['link'] in item['link']:
                current = item['time']
                break

        new_item = {}
        new_item['link'] = {}
        new_item['text'] = {}
        new_item['time'] = {}
        new_item['address'] = {}
        new_item['area'] = {}
        new_item['price'] = {}

        new_item['link'] = result['link']
        new_item['address'] = result['address']
        new_item['area'] = result['area']
        new_item['price'] = result['price']
        new_item['text'] = result['text']
        new_item['time'] = current

        data['links'].append(new_item)

        with open("json/realestates.json", 'w') as output:
            json.dump(data, output)

def parseTitle():
    url = "https://www.finn.no/realestate/homes/search.html?location=0.20061"
    html = urlopen(url)
    soup = BeautifulSoup(html, "lxml")
    type(soup)
    all_div = soup.find_all("div", {"class": "ads__unit__content"})
    for div in all_div:
        result = {}
        result['link'] = {}
        result['text'] = {}
        result['address'] = {}
        result['area'] = {}
        result['price'] = {}
        link_class = div.find_all('a', {"class": "ads__unit__link"})
        link = link_class[0].get('href', '')
        link_text = link_class[0].get_text().strip()
        if not "newbuildings" in link:
            add_span = div.find_all("span", {"class": "ads__unit__content__details"})
            add_text = add_span[0].find_all('span')
            add_value = add_text[0].get_text().strip()
            p = div.find_all("p",{"class": "ads__unit__content__keys"})
            p_span = p[0].find_all('span')
            area = p_span[0].get_text().strip()
            price = p_span[1].get_text().strip()
            finn_link = str("https://www.finn.no")
            result['link'] = finn_link + link
            result['text'] = link_text.encode('ascii','ignore').decode('utf-8')
            result['address'] = add_value.encode('ascii','ignore').decode('utf-8')
            result['area'] = area.encode('ascii','ignore').decode('utf-8')
            result['price'] = price.encode('ascii','ignore').decode('utf-8')
            add_title(result)
        else:
            continue

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
    with open (link) as output:
        data = json.load(output)
        libHtml.html(data, "finn_links")

def filterWeek():
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = datetime.today() - timedelta(days=7)
    start_date = start_date.strftime('%Y-%m-%d')
    filterData = {}
    filterData['links'] = []
    with open (link) as output:
       data = json.load(output)
       for item in data['links']:
           time = item['time'].split('T')
           if start_date <= time[0] and time[0] <= end_date:
               new_item = {}
               new_item['link'] = {}
               new_item['time'] = {}
               new_item['link'] = item['link']
               new_item['time'] = item['time']
               filterData['links'].append(new_item)
    with open("json/links_week.json", "w") as output:
        json.dump(filterData, output)

def filterJson(date):
    start_date = date[0]
    end_date = date[1]
    filterData = {}
    filterData['links'] = []
    with open (link) as output:
       data = json.load(output)
       for item in data['links']:
           time = item['time'].split('T')
           if start_date <= time[0] and time[0] <= end_date:
               new_item = {}
               new_item['link'] = {}
               new_item['time'] = {}
               new_item['link'] = item['link']
               new_item['time'] = item['time']
               filterData['links'].append(new_item)
    with open("json/filtered_links.json", "w") as output:
        json.dump(filterData, output)

