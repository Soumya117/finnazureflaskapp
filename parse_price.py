from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import sys
import io
import geocode

def addGeocodesPris():
    old_data = {}
    with open("json/pris.json") as input:
        old_data = json.load(input)
        for item in old_data['links']:
            item['details']['geocode'] = {}
            item['details']['geocode'] = geocode.getMarkers(item['details']['address'])

    with open("json/pris.json", "w") as output:
        json.dump(old_data, output)

def addGeocodesMultiple():
    old_data = {}
    with open("json/multiplePris.json") as input:
        old_data = json.load(input)
        for item in old_data['links']:
            item['details']['geocode'] = {}
            item['details']['geocode'] = geocode.getMarkers(item['details']['address'])

    with open("json/multiplePris.json", "w") as output:
        json.dump(old_data, output)

def add_pris(result):
    pris_data = {}
    with open('json/pris.json') as output:
        pris_data = json.load(output)
        exists = False
        for price in pris_data['links']:
            if result['link'] in price['link']:
                exists = True

        if not exists:
            #new link
            current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            price = {}
            price['link'] = result['link']
            price['details'] = {}
            price['details']['text'] =  result['text']
            price['details']['area'] = result['area']
            price['details']['address'] = result['address']
            price['details']['geocode'] = result['geocode']

            #now price list
            price['price_list'] = []
            new_price = {}
            new_price['price'] = result['price']
            new_price['time'] = current
            price['price_list'].append(new_price)
            pris_data['links'].append(price)

        if exists:
            #just add the price, rest exists at the correct place
            #look for the link
            pris_exists = False
            for p in pris_data['links']:
                if result['link'] in p['link']:
                    for pris in p['price_list']:
                        if result['price'] in pris['price']:
                            pris_exists = True
                            break
                    if not pris_exists:
                        current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                        price = {}
                        price['price'] = result['price']
                        price['time'] = current
                        p['price_list'].append(price)

    with io.open('json/pris.json', 'w', encoding='utf8') as outfile:
        json.dump(pris_data, outfile, ensure_ascii=False)

def cleanupSold():
    sold_links = []
    with open('json/sold.json') as input:
        sold = json.load(input)
        for link in sold['links']:
            sold_links.append(link['link'])

    price_data = {}
    with open('json/pris.json') as input:
        price_data = json.load(input)
        count = 0
        for item in list(price_data['links']):
            if item['link'] in sold_links:
                print("Deleting link from price: ", item['link'])
                del price_data['links'][count]
            count+=1

    with io.open('json/pris.json', 'w', encoding='utf8') as output:
        json.dump(price_data, output, ensure_ascii=False)

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
          result['text'] = str(link['text'])
          result['address'] = str(link['address'])
          result['geocode'] = str(link['geocode'])
          result['price'] = uniString
          result['area'] = str(link['area'])
          add_pris(result)
    print("Parsing price finished..!")
    sys.stdout.flush()

def multiplePriceLinks():

    multipleData = {}
    with open("json/multiplePris.json") as input:
        multipleData = json.load(input)

    with open ('json/pris.json') as output:
        data = json.load(output)
        for item in data['links']:
            #Check if the link is already present in multiplePris.json

            count = 0
            for mul in multipleData['links']:
                if item['link'] in mul['link']:
                    del multipleData['links'][count]
                count = count + 1

            item_list = item['price_list']
            if len(item_list) > 1:
                price = {}
                price['link'] = item['link']
                price['details'] = item['details']
                price['price_list'] = []
                price['price_list'] = item['price_list']
                multipleData['links'].append(price)

    with io.open ('json/multiplePris.json','w',  encoding='utf8') as output:
        json.dump(multipleData, output, ensure_ascii=False)
