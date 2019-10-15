import sys
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import geocode as geocode
from logger import log


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


def parse_title(json_data):
    data = json.loads(json_data)
    url = "https://www.finn.no/realestate/homes/search.html?location=0.20061"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "lxml")
    try:
        all_div = soup.find_all("div", {"class": "ads__unit__content"})
    except Exception as e:
        log("Failed to find divs in {}".format(url))

    for div in all_div:
        result = {}
        try:
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
                result['text'] = link_text
                result['address'] = add_value
                result['geocode'] = geocode.get_markers(add_value)
                result['area'] = area
                result['price'] = price.encode('ascii','ignore').decode('utf-8')
                add_title(result, data)
            else:
                continue
        except Exception as e:
                log("Bad URL {url}: {e}".format(e=e, url=link))

    log("Parsing links finished..!")
    data = json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
    return data


def cleanup_sold(sold_blob, links_blob):

    sold_links = []
    sold = json.loads(sold_blob)
    for link in sold['links']:
        sold_links.append(link['link'])

    links_data = json.loads(links_blob)
    count=0
    for link in links_data['links']:
        if link['link'] in sold_links:
            log("Deleting link: {}".format(link['link']))
            del links_data['links'][count]
        else:
            count += 1
    links_data = json.dumps(links_data, indent=4, sort_keys=True, ensure_ascii=False)
    return links_data
