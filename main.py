from flask import Flask, render_template
app = Flask(__name__)
import parse_link as link
import parse_price as price
import parse_sold as sold
import parse_visning as visning
import sys
import blob
import datetime
from logger import log

@app.route('/links')
def renderLinks():

    log("Request received for links at {}".format(datetime.datetime.now()))

    linksBlob = blob.readBlob('links.json')
    linksData = link.parseTitle(linksBlob)
    blob.writeBlob("links.json", linksData)

    log("Request finished for links at {}".format(datetime.datetime.now()))
    return ""

@app.route('/price')
def renderPrice():
    log("Request received for price at {}".format(datetime.datetime.now()))

    linkBlob = blob.readBlob('links.json')
    prisBlob = blob.readBlob('pris.json')
    multipleBlob = blob.readBlob('multiplePris.json')
    pris = price.parsePrice(linkBlob, prisBlob)
    multiple = price.multiplePriceLinks(multipleBlob, prisBlob)

    blob.writeBlob("multiplePris.json", multiple)
    blob.writeBlob("pris.json", pris)

    log("Request finished for price at {}".format(datetime.datetime.now()))
    return ""

@app.route('/visning')
def renderVisning():
    log("Request received for visnings at {}".format(datetime.datetime.now()))

    linkBlob = blob.readBlob('links.json')
    visningBlob = blob.readBlob('visning.json')
    visnings = visning.parseVisning(linkBlob, visningBlob)
    blob.writeBlob("visning.json", visnings)

    log("Request finished for visnings at {}".format(datetime.datetime.now()))
    return ""

@app.route('/clean')
def removeSoldData():
    log("Request received for cleanup at {}".format(datetime.datetime.now()))

    linkBlob = blob.readBlob('links.json')
    prisBlob = blob.readBlob('pris.json')
    soldBlob = blob.readBlob('sold.json')

    linkData = link.cleanupSold(soldBlob, linkBlob)
    prisData = price.cleanupSold(soldBlob, prisBlob)

    blob.writeBlob("links.json", linkData)
    blob.writeBlob("pris.json", prisData)

    log("Request finished for cleanup at {}".format(datetime.datetime.now()))
    return ""

@app.route('/sold')
def renderSold():
    log("Request received for sold at {}".format(datetime.datetime.now()))

    sys.stdout.flush()
    linkBlob = blob.readBlob('links.json')
    soldBlob = blob.readBlob('sold.json')
    soldData = sold.parseSold(linkBlob, soldBlob)

    blob.writeBlob("sold.json", soldData)

    log("Request finished for sold at {}".format(datetime.datetime.now()))
    return ""

if __name__ == "__main__":
    app.run()
# def request():
#     log("Sending requests at {}: ".format(datetime.datetime.now()))
#     # threading.Timer(1200.0, request).start()
#     renderLinks()
#     renderPrice()
#     renderSold()
#     renderVisning()
#     removeSoldData()
#     log("Finished at: {}!".format(datetime.datetime.now()))
#
# # if __name__== "__main__":
# #     print("Running main!!")
#     # request()
