from datetime import datetime
import json
from logger import log
from helpers.util import link_exists
from helpers.htmlutil import HtmlUtil
from helpers.jsonutil import JsonUtil


def add_sold(result, data):
    exists = link_exists(result['link'], data)
    if not exists:
        current = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        new_item = dict()
        new_item['status'] = result['status']
        new_item['time'] = current
        JsonUtil(new_item, result).prepare_json(price=result['price'])
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
            html = HtmlUtil(url)
            soup = html.get_soup()
            pris = html.get_price()
            rows = soup.findAll("span", {"class": "u-capitalize status status--warning u-mb0"})
            if rows:
                status = rows[0].get_text().strip()
                result['status'] = status
                JsonUtil(result, link).prepare_json(price=pris)
                add_sold(result, sold_data)
        except Exception as e:
            log("Bad URL {url}: {e}".format(e=e, url=url))

    log("Parsing sold finished..!")
    data = json.dumps(sold_data, indent=4, sort_keys=True, ensure_ascii=False)
    return data
