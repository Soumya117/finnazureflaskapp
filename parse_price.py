from urllib import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import libHtml
import json
import sys

def add_pris(link, pris):
    with open('json/pris.json') as output:
        pris_data = json.load(output)
        exists = False
        if link not in pris_data:
            pris_data[link] = []
            current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            price = {}
            price['pris'] = {}
            price['time'] = {}
            price['pris'] = pris
            price['time'] = current
            pris_data[link].append(price)
            exists = True
        else:
            for p in pris_data[link]:
                if pris in p['pris']:
                    exists = True
                    break
    if not exists:
        current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        price = {}
        price['pris'] = {}
        price['time'] = {}
        price['pris'] = pris
        price['time'] = current
        pris_data[link].append(price)
        
    with open('json/pris.json', 'w') as outfile:
        json.dump(pris_data, outfile)

def parsePrice():    
    with open('json/links.json') as input:
       data = json.load(input)
       print("Number of links to scan: ", len(data['links']))
       sys.stdout.flush()
       for link in data['links']:
          url = link['link']
          #print("Scanning URL: ", url)
          #sys.stdout.flush()
          html = urlopen(url)
          soup = BeautifulSoup(html, 'lxml')
          rows = soup.find_all('span')
          i = 0
          for row in rows:
              i = i + 1
              if "Prisantydning" in row:
                  break
          pris = rows[i].get_text().strip()
          uniString = str(pris)
          uniString = uniString.replace(u"\u00A0", " ")
          add_pris(url, uniString)

def priceHtml():
    with open ('json/pris.json') as output:
        data = json.load(output)
        libHtml.html(data, "finn_price")

def filterWeek():
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = datetime.today() - timedelta(days=7)
    start_date = start_date.strftime('%Y-%m-%d')
    with open('json/links_week.json') as input:
        data = json.load(input)
        pris_data = {}
        for link in data['links']:
            url = link['link']
            with open("json/pris.json") as input:
                pris = json.load(input)
                for item in pris:
                   if item == url:
                       pris_data[item]= []
                       for prices in pris[item]:
                           new_item = {}
                           new_item['time'] = {}
                           new_item['pris'] = {}
                           new_item['time'] = prices['time']
                           new_item['pris'] = prices['pris']
                           pris_data[item].append(new_item)
    with open('json/price_weeks.json', 'w') as output:
        json.dump(pris_data, output)

def filterJson():
    with open('json/filtered_links.json') as input:
       data = json.load(input)
       pris_data = {}
       for link in data['links']:
          url = link['link']
          with open("json/pris.json") as input:
              pris = json.load(input)
              for item in pris:
                  if item == url:
                      pris_data[item]= []
                      for prices in pris[item]:
                          new_item = {}
                          new_item['time'] = {}
                          new_item['pris'] = {}
                          new_item['time'] = prices['time']
                          new_item['pris'] = prices['pris']
                          pris_data[item].append(new_item)

def priceWithFinnId(finnId):
    with open('json/pris.json') as input:
        data = json.load(input)
        pris_data = {}
        for item in data:
            if finnId in item:
                pris_data[item] = []
                for prices in data[item]:
                    new_item = {}
                    new_item['pris'] = prices['pris']
                    new_item['time'] = prices['time']
                    pris_data[item].append(new_item)
    libHtml.html(pris_data, "finn_price")

def multiplePriceLinks():
    with open ('json/pris.json') as output:
        data = json.load(output)
        pris_data = {}
        for item in data:
            item_list = data[item]
            if len(item_list) > 1:
                pris_data[item] = []
                for pris in data[item]:
                    new_item = {}
                    new_item['pris'] = pris['pris']
                    new_item['time'] = pris['time']
                    pris_data[item].append(new_item)
    with open ('json/multiplePris.json','w') as output:
        json.dump(pris_data, output)
