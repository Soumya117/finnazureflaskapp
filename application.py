#!/usr/bin/python3.5

from flask import Flask, render_template
app = Flask(__name__)
import parse_link as link
import parse_price as price
import parse_sold as sold
from flask import request
import sys
import blob

@app.route('/links')
def renderLinks():
    print("Request received for links..")
    sys.stdout.flush()
    scan = request.args.get('scan')

    if scan:
        print("Scanning links..")
        sys.stdout.flush()
        link.parseTitle()

    blob.upload("links.json", "json/links.json")
    return ""

@app.route('/price')
def renderPrice():
    print("Request receieved for price.")
    sys.stdout.flush()
    scan = request.args.get('scan')

    if scan:
        print("Scanning price..")
        sys.stdout.flush()
        price.parsePrice()
        price.multiplePriceLinks()

    blob.upload("multiplePris.json", "json/multiplePris.json")
    blob.upload("pris.json", "json/pris.json")
    return ""

@app.route('/clean')
def removeSoldData():
    print("Running cleanup..")
    sys.stdout.flush()

    link.cleanupSold()
    price.cleanupSold()

    blob.upload("links.json", "json/links.json")
    blob.upload("pris.json", "json/pris.json")
    return ""

@app.route('/sold')
def renderSold(): 
    print("Request receieved for sold..")
    sys.stdout.flush()
    scan = request.args.get('scan')
    if scan:
        print("Scanning sold..")
        sys.stdout.flush()
        sold.parseSold()

    blob.upload("sold.json", "json/sold.json")

    return ""
