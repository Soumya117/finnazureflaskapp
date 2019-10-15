import json
from logger import log
from helpers.util import link_exists
from helpers.htmlutil import HtmlUtil
from helpers.jsonutil import JsonUtil


def add_visning(result, visning_data):
    exists = link_exists(result['link'], visning_data)
    if not exists:
        # new link
        visning = {}
        visning['details'] = {}
        JsonUtil(visning, result).prepare_json(output=visning['details'])
        visning['details']['price'] = result['price']

        # now price list
        visning['visnings'] = []
        new_visning = result['time']
        visning['visnings'].append(new_visning)
        visning_data['links'].append(visning)

    if exists:
        for p in visning_data['links']:
            if result['link'] in p['link']:
                if not result['time'] in p['visnings']:
                    new_visning = result['time']
                    p['visnings'].append(new_visning)


def cleanup_sold(sold_blob, view_blob):
    sold_links = []
    sold = json.loads(sold_blob)
    for link in sold['links']:
        sold_links.append(link['link'])

    visning_data = json.loads(view_blob)
    count = 0
    for item in list(visning_data['links']):
        if item['link'] in sold_links:
            log("Deleting link from visnings: {}".format(item['link']))
            del visning_data['links'][count]
        else:
            count += 1

    data = json.dumps(visning_data, indent=4, sort_keys=True, ensure_ascii=False)
    return data


def parse_visning(link_blob, visning_blob):
    visning_data = json.loads(visning_blob)
    data = json.loads(link_blob)
    log("Number of links to scan: {}".format(len(data['links'])))
    result = {}
    for link in data['links']:
        try:
            url = link['link']
            html = HtmlUtil(url)
            soup = html.get_soup()
            rows = soup.findAll("time")
            for row in rows:
                time_txt = row.get_text().strip()
                result['time'] = time_txt
                JsonUtil(result, link).prepare_json(price=html.get_price())
                add_visning(result, visning_data)
        except Exception as e:
            log("Bad URL {url}: {e}".format(e=e, url=url))

    log("Parsing visnings finished..!")
    data = json.dumps(visning_data, indent=4, sort_keys=True, ensure_ascii=False)
    return data
