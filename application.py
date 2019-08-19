#!/usr/bin/python3.5

from flask import Flask, render_template
app = Flask(__name__)
import parse_link as link
import parse_price as price
import parse_sold as sold
import parse_visning as visning
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
        link.addGeocodes()
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
        price.addGeocodesPris()
        price.addGeocodesMultiple()
        price.parsePrice()
        price.multiplePriceLinks()

    blob.upload("multiplePris.json", "json/multiplePris.json")
    blob.upload("pris.json", "json/pris.json")
    return ""

@app.route('/visning')
def renderVisning():
    print("Request received for visning.")
    sys.stdout.flush()
    scan = request.args.get('scan')

    if scan:
        print("Scanning visnings..")
        sys.stdout.flush()
        visning.addGeocodes()
        visning.parseVisning()

    blob.upload("visning.json", "json/visning.json")
    return ""

@app.route('/clean')
def removeSoldData():
    print("Running cleanup..")
    sys.stdout.flush()

    link.cleanupSold()
    # price.cleanupSold()
    # visning.cleanupSold()

    blob.upload("links.json", "json/links.json")
    # blob.upload("pris.json", "json/pris.json")
    # blob.upload("visning.json", "json/visning.json")
    return ""

@app.route('/sold')
def renderSold(): 
    print("Request receieved for sold..")
    sys.stdout.flush()
    scan = request.args.get('scan')
    if scan:
        print("Scanning sold..")
        sys.stdout.flush()
        sold.addGeocodes()
        sold.parseSold()

    blob.upload("sold.json", "json/sold.json")
    return ""
