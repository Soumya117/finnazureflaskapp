from flask import Flask, render_template
app = Flask(__name__)
import parse_link as link
import parse_price as price
import parse_sold as sold
from flask import request
import parseDate
import sys

@app.route('/links')
def renderLinks():
    print("Request received for links..")
    sys.stdout.flush()
    filterDate = request.args.get('date')
    scan = request.args.get('scan')

    if scan:
        print("Scanning links..")
        sys.stdout.flush()
        link.parseLink()
        link.linkHtml()

    if filterDate:
        valid = parseDate.validate(filterDate)
        if not "success" in valid:
            return "Error: " + valid + "\nUsage: 2019-02-12:2019-03-11"
        date = parseDate.splitDate(filterDate)
        link.filterJson(date)

    if not filterDate and not scan:
        link.linkHtml()

    return render_template('finn_links.html')

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
        price.priceHtml()

    if multiplePrice:
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

    if not filterDate and not finnId and not multiplePrice and not scan:
        price.priceHtml()

    return render_template('finn_price.html')

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
        sold.soldHtml()

    if filterDate:
        valid = parseDate.validate(filterDate)
        if not "success" in valid:
            return "Error: " + valid + "\nUsage: 2019-02-12:2019-03-11"
        date = parseDate.splitDate(filterDate)
        link.filterJson(date)
        sold.filterJson()

    if not scan and not filterDate:
        sold.soldHtml()

    return render_template('finn_sold.html')
