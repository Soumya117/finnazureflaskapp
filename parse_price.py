from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import sys

def add_pris(result):
    with open('json/pris.json') as output:
        pris_data = json.load(output)
        exists = False
        if result['link'] not in pris_data:
            pris_data[result['link']] = []
            current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            price = {}
            price['text'] = result['text']
            price['address'] = result['address']
            price['area'] = result['area']
            price['price'] = result['price']
            price['time'] = current
            pris_data[result['link']].append(price)
            exists = True
        else:
            for p in pris_data[result['link']]:
                if result['price'] in p['price']:
                    exists = True
                    break
    if not exists:
        current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        price = {}
        price['text'] = result['text']
        price['address'] = result['address']
        price['area'] = result['area']
        price['price'] = result['price']
        price['time'] = current
        pris_data[result['link']].append(price)
        
    with open('json/pris.json', 'w') as outfile:
        json.dump(pris_data, outfile)

def cleanupSold():
    sold_links = []
    with open('json/sold.json') as input:
        sold = json.load(input)
        for link in sold['links']:
            sold_links.append(link['link'])

    price_data = {}
    with open('json/pris.json') as input:
        price_data = json.load(input)
        print("Total data: ", len(price_data))
        for link in list(price_data):
            if link in sold_links:
                print("Deleting link from price: ", link)
                del price_data[link]

    with open('json/pris.json', 'w') as output:
        json.dump(price_data, output)

def parsePrice():    
    with open('json/links.json') as input:
       data = json.load(input)
       print("Number of links to scan: ", len(data['links']))
       sys.stdout.flush()
       for link in data['links']:
          url = link['link']
          result = {}
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
          result['link'] = url
          result['text'] = link['text']
          result['address'] = link['address']
          result['price'] = uniString
          result['area'] = link['area']
          add_pris(result)

def multiplePriceLinks():
    multipleData = {}
    with open("json/multiplePris.json") as input:
        multipleData = json.load(input)

    with open ('json/pris.json') as output:
        data = json.load(output)
        for item in data:
            item_list = data[item]
            if len(item_list) > 1:
                multipleData[item] = []
                for pris in data[item]:
                    new_item = {}
                    new_item['price'] = pris['price']
                    new_item['time'] = pris['time']
                    new_item['text'] = pris['text']
                    new_item['address'] = pris['address']
                    new_item['area'] = pris['area']
                    multipleData[item].append(new_item)

    with open ('json/multiplePris.json','w') as output:
        json.dump(multipleData, output)
