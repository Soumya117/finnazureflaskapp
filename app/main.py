import parsers.parse_link as link
import parsers.parse_price as price
import parsers.parse_sold as sold
import parsers.parse_visning as visning
import helpers.blob as blob
import datetime
from flask import Flask
from helpers.logger import log
from helpers.middleware import setup_metrics
import sys

sys.path.append('/usr/local/lib/python3.6/dist-packages/')

app = Flask(__name__)
setup_metrics(app)


@app.route('/links')
def render_links():
    log("Request received for links at {}".format(datetime.datetime.now()))

    links_blob = blob.read_blob('links.json')
    links_data = link.parse_title(links_blob)
    blob.write_blob("links.json", links_data)

    log("Request finished for links at {}".format(datetime.datetime.now()))
    return ""


@app.route('/price')
def render_price():
    log("Request received for price at {}".format(datetime.datetime.now()))

    link_blob = blob.read_blob('links.json')
    pris_blob = blob.read_blob('pris.json')
    multiple_blob = blob.read_blob('multiplePris.json')
    pris = price.parse_price(link_blob, pris_blob)
    multiple = price.multiple_price_links(multiple_blob, pris_blob)

    blob.write_blob("multiplePris.json", multiple)
    blob.write_blob("pris.json", pris)

    log("Request finished for price at {}".format(datetime.datetime.now()))
    return ""


@app.route('/visning')
def render_visning():
    log("Request received for visnings at {}".format(datetime.datetime.now()))

    link_blob = blob.read_blob('links.json')
    visning_blob = blob.read_blob('visning.json')
    visnings = visning.parse_visning(link_blob, visning_blob)
    blob.write_blob("visning.json", visnings)

    log("Request finished for visnings at {}".format(datetime.datetime.now()))
    return ""


@app.route('/clean')
def remove_sold_data():
    log("Request received for cleanup at {}".format(datetime.datetime.now()))

    link_blob = blob.read_blob('links.json')
    pris_blob = blob.read_blob('pris.json')
    visning_blob = blob.read_blob('visning.json')
    sold_blob = blob.read_blob('sold.json')

    link_data = link.cleanup_sold(sold_blob, link_blob)
    pris_data = price.cleanup_sold(sold_blob, pris_blob)
    visning_data = visning.cleanup_sold(sold_blob, visning_blob)

    blob.write_blob("links.json", link_data)
    blob.write_blob("pris.json", pris_data)
    blob.write_blob("visning.json", visning_data)

    log("Request finished for cleanup at {}".format(datetime.datetime.now()))
    return ""


@app.route('/sold')
def render_sold():
    log("Request received for sold at {}".format(datetime.datetime.now()))

    link_blob = blob.read_blob('links.json')
    sold_blob = blob.read_blob('sold.json')
    sold_data = sold.parse_sold(link_blob, sold_blob)

    blob.write_blob("sold.json", sold_data)

    log("Request finished for sold at {}".format(datetime.datetime.now()))
    return ""
