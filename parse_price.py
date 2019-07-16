from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import json

def add_pris(link, pris):
    with open('pris.json') as output:
        pris_data = json.load(output)
        exists = False
        if link not in pris_data:
            pris_data[link] = []
            current = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
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
        current = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        price = {}
        price['pris'] = {}
        price['time'] = {}
        price['pris'] = pris
        price['time'] = current
        pris_data[link].append(price)
        
    with open('pris.json', 'w') as outfile:
        json.dump(pris_data, outfile)

def parsePrice():    
    with open('links.json') as input:
       data = json.load(input)
       for link in data['links']:
          url = link['link']
          html = urlopen(url)
          soup = BeautifulSoup(html, 'lxml')
          title = soup.title
          print(title)
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
