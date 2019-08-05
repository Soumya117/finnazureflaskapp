from flask import Flask, render_template
app = Flask(__name__)
import parse_link as link
import parse_price as price
import parse_sold as sold
from flask import request
import parseDate
import sys
import blob

@app.route('/links')
def renderLinks():
    print("Request received for links..")
    sys.stdout.flush()
    filterDate = request.args.get('date')
    scan = request.args.get('scan')

    # if scan:
    #     print("Scanning links..")
    #     sys.stdout.flush()
    #     link.parseLink()
    #
    # if filterDate:
    #     valid = parseDate.validate(filterDate)
    #     if not "success" in valid:
    #         return "Error: " + valid + "\nUsage: 2019-02-12:2019-03-11"
    #     date = parseDate.splitDate(filterDate)
    #     link.filterJson(date)
    #
    link.parseTitle()
    # link.filterWeek()
    # blob.upload("links_week.json", "json/links_week.json")
    # blob.upload("links.json", "json/links.json")
    return ""

@app.route('/price')
def renderPrice():
    print("Request receieved for price.")
    sys.stdout.flush()
    filterDate = request.args.get('date')
    finnId = request.args.get('finnId')
    multiplePrice = request.args.get('multiple')
    scan = request.args.get('scan')

    if scan:
        print("Scanning price..")
        sys.stdout.flush()
        price.parsePrice()

    if multiplePrice:
        print("Scanning for price changes..!")
        sys.stdout.flush()
        price.multiplePriceLinks()

    if finnId:
        price.priceWithFinnId(finnId)

    if filterDate:
        valid = parseDate.validate(filterDate)
        if not "success" in valid:
            return "Error: " + valid + "\nUsage: 2019-02-12:2019-03-11"
        date = parseDate.splitDate(filterDate)
        link.filterJson(date)
        price.filterJson()

    price.multiplePriceLinks()
    blob.upload("multiplePris.json", "json/multiplePris.json")    
    blob.upload("pris.json", "json/pris.json")
    return ""

@app.route('/sold')
def renderSold(): 
    print("Request receieved for sold..")
    sys.stdout.flush()
    filterDate = request.args.get('date')
    scan = request.args.get('scan')
    if scan:
        print("Scanning sold..")
        sys.stdout.flush()
        sold.parseSold()

    if filterDate:
        valid = parseDate.validate(filterDate)
        if not "success" in valid:
            return "Error: " + valid + "\nUsage: 2019-02-12:2019-03-11"
        date = parseDate.splitDate(filterDate)
        link.filterJson(date)
        sold.filterJson()

    blob.upload("sold.json", "json/sold.json")

    return ""
