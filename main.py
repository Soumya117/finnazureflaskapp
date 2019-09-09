#!/usr/bin/python3.5

from flask import Flask, render_template
app = Flask(__name__)
import parse_link as link
import parse_price as price
import parse_sold as sold
import parse_visning as visning
import sys
import blob
import datetime

@app.route('/links')
def renderLinks():
    print("Request received for links at {}".format(datetime.datetime.now()))
    sys.stdout.flush()
    linksBlob = blob.readBlob('links.json')
    linksData = link.parseTitle(linksBlob)
    blob.writeBlob("links.json", linksData)
    print("Request finished for links at {}".format(datetime.datetime.now()))
    return ""

@app.route('/price')
def renderPrice():
    print("Request received for price at {}".format(datetime.datetime.now()))
    sys.stdout.flush()
    linkBlob = blob.readBlob('links.json')
    prisBlob = blob.readBlob('pris.json')
    multipleBlob = blob.readBlob('multiplePris.json')
    pris = price.parsePrice(linkBlob, prisBlob)
    multiple = price.multiplePriceLinks(multipleBlob, prisBlob)

    blob.writeBlob("multiplePris.json", multiple)
    blob.writeBlob("pris.json", pris)
    print("Request finished for price at {}".format(datetime.datetime.now()))
    return ""

@app.route('/visning')
def renderVisning():
    print("Request received for visnings at {}".format(datetime.datetime.now()))
    sys.stdout.flush()
    print("Scanning visnings..")
    sys.stdout.flush()
    linkBlob = blob.readBlob('links.json')
    visningBlob = blob.readBlob('visning.json')
    visnings = visning.parseVisning(linkBlob, visningBlob)

    blob.writeBlob("visning.json", visnings)
    print("Request finished for visnings at {}".format(datetime.datetime.now()))
    return ""

@app.route('/clean')
def removeSoldData():
    print("Request received for cleanup at {}".format(datetime.datetime.now()))
    sys.stdout.flush()
    linkBlob = blob.readBlob('links.json')
    prisBlob = blob.readBlob('pris.json')
    soldBlob = blob.readBlob('sold.json')

    linkData = link.cleanupSold(soldBlob, linkBlob)
    prisData = price.cleanupSold(soldBlob, prisBlob)

    blob.writeBlob("links.json", linkData)
    blob.writeBlob("pris.json", prisData)
    print("Request finished for cleanup at {}".format(datetime.datetime.now()))
    return ""

@app.route('/sold')
def renderSold():
    print("Request received for sold at {}".format(datetime.datetime.now()))
    sys.stdout.flush()
    print("Scanning sold..")
    sys.stdout.flush()
    linkBlob = blob.readBlob('links.json')
    soldBlob = blob.readBlob('sold.json')
    soldData = sold.parseSold(linkBlob, soldBlob)

    blob.writeBlob("sold.json", soldData)
    print("Request finished for sold at {}".format(datetime.datetime.now()))
    return ""

def request():
    print("Sending requests at {}: ".format(datetime.datetime.now()))
    # threading.Timer(1200.0, request).start()
    renderLinks()
    renderPrice()
    renderSold()
    renderVisning()
    removeSoldData()
    print("Finished at: {}!".format(datetime.datetime.now()))

# if __name__== "__main__":
#     print("Running main!!")
    # request()