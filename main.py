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
    linksData = {}
    if scan:
        print("Scanning links..")
        sys.stdout.flush()
        linksBlob = blob.readBlob('links.json')
        linksData = link.parseTitle(linksBlob)
    blob.writeBlob("links.json", linksData)
    return ""

@app.route('/price')
def renderPrice():
    print("Request receieved for price.")
    sys.stdout.flush()
    scan = request.args.get('scan')
    pris = None
    multiple = None
    if scan:
        print("Scanning price..")
        sys.stdout.flush()
        linkBlob = blob.readBlob('links.json')
        prisBlob = blob.readBlob('pris.json')
        multipleBlob = blob.readBlob('multiplePris.json')
        pris = price.parsePrice(linkBlob, prisBlob)
        multiple = price.multiplePriceLinks(multipleBlob, prisBlob)

    blob.writeBlob("multiplePris.json", multiple)
    blob.writeBlob("pris.json", pris)
    return ""

@app.route('/visning')
def renderVisning():
    print("Request received for visning.")
    sys.stdout.flush()
    scan = request.args.get('scan')
    visnings = None
    if scan:
        print("Scanning visnings..")
        sys.stdout.flush()
        linkBlob = blob.readBlob('links.json')
        visningBlob = blob.readBlob('visning.json')
        visnings = visning.parseVisning(linkBlob, visningBlob)

    blob.writeBlob("visning.json", visnings)
    return ""

@app.route('/clean')
def removeSoldData():
    print("Running cleanup..")
    sys.stdout.flush()
    linkBlob = blob.readBlob('links.json')
    prisBlob = blob.readBlob('pris.json')
    soldBlob = blob.readBlob('sold.json')

    linkData = link.cleanupSold(soldBlob, linkBlob)
    prisData = price.cleanupSold(soldBlob, prisBlob)

    blob.writeBlob("links.json", linkData)
    blob.writeBlob("pris.json", prisData)
    return ""

@app.route('/sold')
def renderSold(): 
    print("Request receieved for sold..")
    sys.stdout.flush()
    scan = request.args.get('scan')
    soldData = None
    if scan:
        print("Scanning sold..")
        sys.stdout.flush()
        linkBlob = blob.readBlob('links.json')
        soldBlob = blob.readBlob('sold.json')
        soldData = sold.parseSold(linkBlob, soldBlob)

    blob.writeBlob("sold.json", soldData)
    return ""
