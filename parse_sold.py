from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import sys

def add_sold(result):
    with open('json/sold.json') as input:
        data = json.load(input)
        exists = False
        for item in data['links']:
            if result['link'] in item['link']:
                exists = True
                break
        if not exists:
            current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            new_item = {}
            new_item['link'] = result['link']
            new_item['status'] = result['status']
            new_item['time'] = current
            new_item['text'] = result['text']
            new_item['address'] = result['address']
            new_item['price'] = result['price']
            new_item['area'] = result['area']
            data['links'].append(new_item)

        with open('json/sold.json', 'w') as output:
            json.dump(data, output)

def parseSold():
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

          rows = soup.findAll("span", {"class": "u-capitalize status status--warning u-mb0"})
          if rows:
              status = rows[0].get_text().strip()
              result['status'] = status
              result['link'] = url
              result['text'] = link['text']
              result['address'] = link['address']
              result['price'] = uniString
              result['area'] = link['area']
              add_sold(result)
    print("Parsing sold finished..!")
    sys.stdout.flush()