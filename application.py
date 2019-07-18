from flask import Flask, render_template
app = Flask(__name__)

import parse_link as link
import parse_price as price
from flask import request
import parseDate

@app.route('/links')
def renderLinks():
    filterDate = request.args.get('date')
    valid = parseDate.validate(filterDate)
    if not "success" in valid:
        return "Error: " + valid + "\nUsage: 2019-02-12:2019-03-11" 
    date = parseDate.splitDate(filterDate)
    start_date = date[0]
    end_date = date[1]
    print("Start date: ", start_date)
    print("End date: ", end_date)
    
    link.parseLink()
    link.linkHtml()
    return render_template('finn_links.html')

@app.route('/price')
def renderPrice():
    link.parseLink()
    price.parsePrice()
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
