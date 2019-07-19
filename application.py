from flask import Flask, render_template
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

import parse_link as link
import parse_price as price
from flask import request
import parseDate

@app.route('/links')
def renderLinks():
    filterDate = request.args.get('date')
    scan = request.args.get('scan')

    if scan:
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
    filterDate = request.args.get('date')
    finnId = request.args.get('finnId')
    multiplePrice = request.args.get('multiple')
    scan = request.args.get('scan')

    if scan:
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

@app.route('/date')
def dateParse():
    entryDate = request.args.get('date')
    valid = parseDate.validate(entryDate)
    if "success" in valid:
       return "You entered: " + entryDate
    else:
       return "Error: " + valid + "\nUsage: 2019-02-12:2019-03-11"
