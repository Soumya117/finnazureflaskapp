from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import libHtml
import json
import sys

def add_sold(link, status):
    with open('json/sold.json') as input:
        data = json.load(input)
        exists = False
        for item in data['links']:
            if link in item['link']:
                exists = True
                break
        if not exists:
            current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            new_item = {}
            new_item['link'] = {}
            new_item['status'] = {}
            new_item['time'] = {}
            new_item['link'] = link
            new_item['status'] = status
            new_item['time'] = current
            data['links'].append(new_item)

        with open('json/sold.json', 'w') as output:
            json.dump(data, output)

def parseSold():
    with open('json/links.json') as input:
       data = json.load(input)
       print("Number of links to scan: ", len(data['links']))
       sys.stdout.flush()
       for link in data['links']:
          url = link['link']
          #print("Scanning link: ", url)
          #sys.stdout.flush()
          html = urlopen(url)
          soup = BeautifulSoup(html, 'lxml')
          rows = soup.findAll("span", {"class": "u-capitalize status status--warning u-mb0"})
          if rows:
              status = rows[0].get_text().strip()
              add_sold(url, status)
    print("Parsing sold finished..!")
    sys.stdout.flush()

def soldHtml():
    with open ('json/sold.json') as output:
        data = json.load(output)
        libHtml.html(data, "finn_sold")

def filterWeek():
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = datetime.today() - timedelta(days=1)
    start_date = start_date.strftime('%Y-%m-%d')
    with open('json/links_week.json') as input:
       data = json.load(input)
       sold_data = {}
       sold_data["links"]= []
       for link in data['links']:
          url = link['link']
          with open("json/sold.json") as input:
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
    print("Sold Data: ", sold_data)
    sys.stdout.flush()
    with open('json/sold_weeks.json', 'w') as output:
        json.dump(sold_data, output)

def filterJson():
    with open('json/filtered_links.json') as input:
       data = json.load(input)
       sold_data = {}
       sold_data["links"]= []
       for link in data['links']:
          url = link['link']
          with open("json/sold.json") as input:
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
