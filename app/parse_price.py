import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
from logger import log
from helpers.util import link_exists


def add_pris(result, pris_data):
    exists = link_exists(result['link'], pris_data)
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


def cleanup_sold(sold_blob, pris_blob):
    sold_links = []
    sold = json.loads(sold_blob)
    for link in sold['links']:
        sold_links.append(link['link'])

    price_data = json.loads(pris_blob)
    count = 0
    for item in list(price_data['links']):
        if item['link'] in sold_links:
            if len(item['price_list']) < 2:
                log("Deleting link from pris: {}".format(link['link']))
                del price_data['links'][count]
            else:
                count = count + 1
    data = json.dumps(price_data, indent=4, sort_keys=True, ensure_ascii=False)
    return data


def parse_price(link_blob, price_blob):
    data = json.loads(link_blob)
    price_blob = json.loads(price_blob)
    log("Number of links to scan: {}".format(len(data['links'])))
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
            add_pris(result, price_blob)
        except Exception as e:
            log("Bad URL {url}: {e}".format(e=e, url=url))

    log("Parsing price finished..!")

    data = json.dumps(price_blob, indent=4, sort_keys=True, ensure_ascii=False)
    return data


def multiple_price_links(multiple_blob, pris_blob):
    multiple_data = json.loads(multiple_blob)
    data = json.loads(pris_blob)
    for item in data['links']:
        # Check if the link is already present in multiplePris.json
        count = 0
        for mul in multiple_data['links']:
            if item['link'] in mul['link']:
                del multiple_data['links'][count]
            count = count + 1

        item_list = item['price_list']
        if len(item_list) > 1:
            price = {}
            price['link'] = item['link']
            price['details'] = item['details']
            price['price_list'] = []
            price['price_list'] = item['price_list']
            multiple_data['links'].append(price)
    data = json.dumps(multiple_data, indent=4, sort_keys=True, ensure_ascii=False)
    return data
