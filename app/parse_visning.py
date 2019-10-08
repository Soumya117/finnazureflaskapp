import requests
from bs4 import BeautifulSoup
import json
import sys
from logger import log

# def addGeocodes():
#     old_data = {}
#     with open("json/visning.json") as input:
#         old_data = json.load(input)
#         for item in old_data['links']:
#             item['details']['geocode'] = {}
#             item['details']['geocode'] = geocode.getMarkers(item['details']['address'])
#
#     with open("json/visning.json", "w") as output:
#         json.dump(old_data, output)

def add_visning(result, visning_data):
    exists = False
    for item in visning_data['links']:
        if result['link'] in item['link']:
            exists = True

    if not exists:
        # new link
        visning = {}
        visning['link'] = result['link']
        visning['details'] = {}
        visning['details']['text'] = result['text']
        visning['details']['price'] = result['price']
        visning['details']['area'] = result['area']
        visning['details']['address'] = result['address']
        visning['details']['geocode'] = result['geocode']

        # now price list
        visning['visnings'] = []
        new_visning = result['time']
        visning['visnings'].append(new_visning)
        visning_data['links'].append(visning)

    if exists:
        #just add the price, rest exists at the correct place
        #look for the link
        for p in visning_data['links']:
            if result['link'] in p['link']:
                if not result['time'] in p['visnings']:
                    new_visning = result['time']
                    p['visnings'].append(new_visning)

def cleanupSold(soldBlob, viewBlob):
    sold_links = []
    sold = json.loads(soldBlob)
    for link in sold['links']:
        sold_links.append(link['link'])

    visning_data = json.loads(viewBlob)
    count = 0
    for item in list(visning_data['links']):
        if item['link'] in sold_links:
            log("Deleting link from visnings: {}".format(item['link']))
            del visning_data['links'][count]
        else:
            count += 1

    data = json.dumps(visning_data, indent=4, sort_keys=True, ensure_ascii=False)
    return data


def parseVisning(linkBlob, visningBlob):
    visning_data = json.loads(visningBlob)
    data = json.loads(linkBlob)
    log("Number of links to scan: {}".format(len(data['links'])))
    sys.stdout.flush()
    result = {}
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
                result['price'] = pris
                result['area'] = link['area']
                add_visning(result, visning_data)
        except Exception as e:
            log("Bad URL {url}: {e}".format(e=e, url=url))
            sys.stdout.flush()

    log("Parsing visnings finished..!")
    sys.stdout.flush()
    data = json.dumps(visning_data, indent=4, sort_keys=True, ensure_ascii=False)
    return data