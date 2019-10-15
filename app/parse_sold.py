from bs4 import BeautifulSoup
from datetime import datetime
import json
import requests
from logger import log
from helpers.util import link_exists


def add_sold(result, data):
    exists = link_exists(result['link'], data)
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


def parse_sold(links_blob, sold_blob):
    data = json.loads(links_blob)
    sold_data = json.loads(sold_blob)
    log("Number of links to scan: {}".format(len(data['links'])))
    result = {}
    url = None
    for link in data['links']:
        try:
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
            pris = pris.replace(u"\u00A0", " ")

            rows = soup.findAll("span", {"class": "u-capitalize status status--warning u-mb0"})
            if rows:
                status = rows[0].get_text().strip()
                result['status'] = status
                result['link'] = url
                result['text'] = link['text']
                result['address'] = link['address']
                result['geocode'] = link['geocode']
                result['price'] = pris
                result['area'] = link['area']
                add_sold(result, sold_data)
        except Exception as e:
            log("Bad URL {url}: {e}".format(e=e, url=url))

    log("Parsing sold finished..!")
    data = json.dumps(sold_data, indent=4, sort_keys=True, ensure_ascii=False)
    return data
