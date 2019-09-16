import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import sys

# def addGeocodesPris():
#     old_data = {}
#     with open("json/pris.json") as input:
#         old_data = json.load(input)
#         for item in old_data['links']:
#             item['details']['geocode'] = {}
#             item['details']['geocode'] = geocode.getMarkers(item['details']['address'])
#
#     with open("json/pris.json", "w") as output:
#         json.dump(old_data, output)
#
# def addGeocodesMultiple():
#     old_data = {}
#     with open("json/multiplePris.json") as input:
#         old_data = json.load(input)
#         for item in old_data['links']:
#             item['details']['geocode'] = {}
#             item['details']['geocode'] = geocode.getMarkers(item['details']['address'])
#
#     with open("json/multiplePris.json", "w") as output:
#         json.dump(old_data, output)


def add_pris(result, pris_data):
    exists = False
    for price in pris_data['links']:
        if result['link'] in price['link']:
            exists = True

    if not exists:
        # new link
        current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        price = {}
        price['link'] = result['link']
        price['details'] = {}
        price['details']['text'] = result['text']
        price['details']['area'] = result['area']
        price['details']['address'] = result['address']
        price['details']['geocode'] = result['geocode']

        # now price list
        price['price_list'] = []
        new_price = {}
        new_price['price'] = result['price']
        new_price['time'] = current
        price['price_list'].append(new_price)
        pris_data['links'].append(price)

    if exists:
        # just add the price, rest exists at the correct place
        # look for the link
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

def cleanupSold(soldBlob, prisBlob):
    sold_links = []
    sold = json.loads(soldBlob)
    for link in sold['links']:
        sold_links.append(link['link'])

    price_data = json.loads(prisBlob)
    count = 0
    for item in list(price_data['links']):
        if item['link'] in sold_links:
            if len(item['price_list']) < 2:
                del price_data['links'][count]
            else:
                count = count + 1
    data = json.dumps(price_data, indent=4, sort_keys=True, ensure_ascii=False)
    return data

def parsePrice(linkBlob, priceBlob):
    data = json.loads(linkBlob)
    priceBlob = json.loads(priceBlob)
    print("Number of links to scan: ", len(data['links']))
    sys.stdout.flush()
    for link in data['links']:
        try:
            result = {}
            url = link['link']
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'lxml')
            rows = soup.find_all('span')
            i = 0
            for row in rows:
                i = i + 1
                if "Prisantydning" in row:
                    break
            pris = rows[i].get_text().strip()
            pris = pris.replace(u"\u00A0", " ")
            result['link'] = url
            result['text'] = link['text']
            result['address'] = link['address']
            result['geocode'] = link['geocode']
            result['price'] = pris
            result['area'] = link['area']
            add_pris(result, priceBlob)
        except Exception as e:
            print("Bad URL {url}: {e}".format(e=e, url=url))
            sys.stdout.flush()

    print("Parsing price finished..!")
    sys.stdout.flush()

    data = json.dumps(priceBlob, indent=4, sort_keys=True, ensure_ascii=False)
    return data

def multiplePriceLinks(multipleBlob, prisBlob):
    multipleData = json.loads(multipleBlob)
    data = json.loads(prisBlob)
    for item in data['links']:
        # Check if the link is already present in multiplePris.json
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
    data = json.dumps(multipleData, indent=4, sort_keys=True, ensure_ascii=False)
    return data