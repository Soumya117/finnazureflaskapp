from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import sys
import io
import geocode

def addGeocodes():
    old_data = {}
    with open("json/visning.json") as input:
        old_data = json.load(input)
        for item in old_data['links']:
            item['details']['geocode'] = {}
            item['details']['geocode'] = geocode.getMarkers(item['details']['address'])

    with open("json/visning.json", "w") as output:
        json.dump(old_data, output)

def add_visning(result):
    with open('json/visning.json') as output:
        visning_data = json.load(output)
        exists = False
        for item in visning_data['links']:
            if result['link'] in item['link']:
                exists = True

        if not exists:
            #new link
            visning = {}
            visning['link'] = result['link']
            visning['details'] = {}
            visning['details']['text'] =  result['text']
            visning['details']['price'] =  result['price']
            visning['details']['area'] = result['area']
            visning['details']['address'] = result['address']
            visning['details']['geocode'] = result['geocode']

            #now price list
            visning['visnings'] = []
            new_visning = {}
            new_visning = result['time']
            visning['visnings'].append(new_visning)
            visning_data['links'].append(visning)

    if exists:
        #just add the price, rest exists at the correct place
        #look for the link
        for p in visning_data['links']:
            if result['link'] in p['link']:
                if not result['time'] in p['visnings']:
                    new_visning = {}
                    new_visning = result['time']
                    p['visnings'].append(new_visning)

    with io.open('json/visning.json', 'w', encoding='utf8') as outfile:
        json.dump(visning_data, outfile, ensure_ascii=False)

def cleanupSold():
    sold_links = []
    with open('json/sold.json') as input:
        sold = json.load(input)
        for link in sold['links']:
            sold_links.append(link['link'])

    visning_data = {}
    with open('json/visning.json') as input:
        visning_data = json.load(input)
        count = 0
        for item in list(visning_data['links']):
            if item['link'] in sold_links:
                print("Deleting link from visnings: ", item['link'])
                del visning_data['links'][count]
            count+=1

    with io.open('json/visning.json', 'w', encoding='utf8') as output:
        json.dump(visning_data, output, ensure_ascii=False)

def parseVisning():
    with open('json/links.json') as input:
       data = json.load(input)
       print("Number of links to scan: ", len(data['links']))
       sys.stdout.flush()
       result = {}
       for link in data['links']:
          url = link['link']
          #print("Scanning link: ", url)
          #sys.stdout.flush()
          html = urlopen(url)
          soup = BeautifulSoup(html, 'lxml')
          pris_rows = soup.find_all('span')
          i = 0
          for row in pris_rows:
              i = i + 1
              if "Prisantydning" in row:
                  break
          pris = pris_rows[i].get_text().strip()
          uniString = str(pris)
          uniString = uniString.replace(u"\u00A0", " ")

          rows = soup.findAll("div", {"class": "u-hide-gt768 u-no-print"})
          time_list = []
          if rows:
              time_list = rows[0].find_all('time')
          for time in time_list:
              time_txt = time.get_text().strip()
              result['time'] = time_txt
              result['link'] = url
              result['text'] = link['text']
              result['address'] = link['address']
              result['geocode'] = link['geocode']
              result['price'] = uniString
              result['area'] = link['area']
              add_visning(result)
    print("Parsing visnings finished..!")
    sys.stdout.flush()