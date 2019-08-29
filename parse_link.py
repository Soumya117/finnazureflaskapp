import sys
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import geocode

# def addGeocodes():
#     old_data = {}
#     with open("json/links.json") as input:
#         old_data = json.load(input)
#         for item in old_data['links']:
#             item['geocode'] = {}
#             item['geocode'] = geocode.getMarkers(item['address'])
#
#     with open("json/links.json", "w") as output:
#         json.dump(old_data, output)

def add_title(result, data):
    current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    exists = False
    for item in data['links']:
        if result['link'] in item['link']:
            exists = True
            break
    if not exists:
        new_item = {}
        new_item['link'] = result['link']
        new_item['address'] = result['address']
        new_item['geocode'] = result['geocode']
        new_item['area'] = result['area']
        new_item['price'] = result['price']
        new_item['text'] = result['text']
        new_item['time'] = current

        data['links'].append(new_item)

def parseTitle(jsonData):
    data = json.loads(jsonData)
    url = "https://www.finn.no/realestate/homes/search.html?location=0.20061"
    html = None
    try:
        html = urlopen(url)
    except Exception as e:
        print("Bad URL {url}: {e}".format(e=e, url=url))
        sys.stdout.flush()

    soup = BeautifulSoup(html, "lxml")
    type(soup)
    all_div = soup.find_all("div", {"class": "ads__unit__content"})
    for div in all_div:
        result = {}
        link_class = div.find_all('a', {"class": "ads__unit__link"})
        link = link_class[0].get('href', '')
        link_text = link_class[0].get_text().strip()
        if "realestate/homes/" in link:
            add_span = div.find_all("span", {"class": "ads__unit__content__details"})
            add_text = add_span[0].find_all('span')
            add_value = add_text[0].get_text().strip()
            p = div.find_all("p",{"class": "ads__unit__content__keys"})
            p_span = p[0].find_all('span')
            if len(p_span) < 2:
                continue
            area = p_span[0].get_text().strip()
            price = p_span[1].get_text().strip()
            finn_link = str("https://www.finn.no")
            result['link'] = finn_link + link
            result['text'] = str(link_text)
            result['address'] = str(add_value)
            result['geocode'] = geocode.getMarkers(add_value)
            result['area'] = str(area)
            result['price'] = price.encode('ascii','ignore').decode('utf-8')
            add_title(result, data)
        else:
            continue
    print("Parsing links finished..!")
    sys.stdout.flush()
    data = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
    return data

def cleanupSold(soldBlob, linksBlob):

    sold_links = []
    sold = json.loads(soldBlob)
    for link in sold['links']:
        sold_links.append(link['link'])

    links_data = json.loads(linksBlob)
    count=0
    for link in links_data['links']:
        if link['link'] in sold_links:
            print("Deleting link: ", link['link'])
            del links_data['links'][count]
        count+=1
    links_data = json.dumps(links_data, indent=4, sort_keys=True, ensure_ascii=False)
    return links_data