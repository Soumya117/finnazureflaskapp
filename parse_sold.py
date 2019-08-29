from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import sys
import requests

# def addGeocodes():
#     old_data = {}
#     with open("json/sold.json") as input:
#         old_data = json.load(input)
#         for item in old_data['links']:
#             item['geocode'] = {}
#             item['geocode'] = geocode.getMarkers(item['address'])
#
#     with open("json/sold.json", "w") as output:
#         json.dump(old_data, output)

def add_sold(result, data):
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
        new_item['geocode'] = result['geocode']
        new_item['price'] = result['price']
        new_item['area'] = result['area']
        data['links'].append(new_item)

def parseSold(linksBlob, soldBlob):
    data = json.loads(linksBlob)
    soldData = json.loads(soldBlob)
    print("Number of links to scan: ", len(data['links']))
    sys.stdout.flush()
    url = None
    try:
        result = {}
        for link in data['links']:
            url = link['link']
            html = requests.get(url)

            soup = BeautifulSoup(html.text, 'lxml')
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
                result['geocode'] = link['geocode']
                result['price'] = uniString
                result['area'] = link['area']
                add_sold(result, soldData)
    except Exception as e:
        print("Bad URL {url}: {e}".format(e=e, url=url))
        sys.stdout.flush()

    print("Parsing sold finished..!")
    sys.stdout.flush()
    data = json.dumps(soldData, indent=4, sort_keys=True, ensure_ascii=False)
    return data