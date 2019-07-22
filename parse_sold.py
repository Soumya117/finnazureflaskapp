from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import toHtml
import json

def add_sold(link, status):
    with open('sold.json') as input:
        data = json.load(input)
        exists = False
        for item in data['links']:
            if link in item['link']:
                exists = True
                break
        if not exists:
            current = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            new_item = {}
            new_item['link'] = {}
            new_item['status'] = {}
            new_item['time'] = {}
            new_item['link'] = link
            new_item['status'] = status
            new_item['time'] = current
            data['links'].append(new_item)

        with open('sold.json', 'w') as output:
            json.dump(data, output)

def parseSold():
    with open('links.json') as input:
       data = json.load(input)
       for link in data['links']:
          url = link['link']
          html = urlopen(url)
          soup = BeautifulSoup(html, 'lxml')
          rows = soup.findAll("span", {"class": "u-capitalize status status--warning u-mb0"})
          if rows:
              status = rows[0].get_text().strip()
              add_sold(url, status)

def soldHtml():
    with open ('sold.json') as output:
        data = json.load(output)
        toHtml.html(data, "finn_sold")

def filterJson():
    with open('filtered_links.json') as input:
       data = json.load(input)
       sold_data = {}
       sold_data["links"]= []
       for link in data['links']:
          url = link['link']
          with open("sold.json") as input:
              sold = json.load(input)
              for item in sold['links']:
                  if item['link'] == url:
                    new_item = {}
                    new_item['link'] = {}
                    new_item['status'] = {}
                    new_item['time'] = {}
                    new_item['link'] = item['link']
                    new_item['status'] = item['status']
                    new_item['time'] = item['time']
                    sold_data['links'].append(new_item)
       toHtml.html(sold_data, "finn_sold")