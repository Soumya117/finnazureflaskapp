from flask import Flask, render_template
app = Flask(__name__)

import json
from json2html import *
import pandas as pd
from pandas.io.json import json_normalize
import parse_link as link
import parse_price as price
from flask import request
import parseDate

def linkHtml():
    with open ('links.json') as output:
        data = json.load(output)
        f_table = json2html.convert(json = data)
        finn_html= open("templates/finn_links.html","w")
        finn_html.write(f_table)
        finn_html.close()

def priceHtml():
    with open ('pris.json') as output:
        data = json.load(output)
        f_table = json2html.convert(json = data)
        finn_html= open("templates/finn_price.html","w")
        finn_html.write(f_table)
        finn_html.close()

@app.route('/links')
def renderLinks():
    link.parseLink()
    linkHtml()
    return render_template('finn_links.html')

@app.route('/price')
def renderPrice():
    link.parseLink()
    price.parsePrice()
    priceHtml()
    return render_template('finn_price.html')

@app.route('/dataFrame')
def dataframe():
    link.parseLink()
    with open('links.json') as output:
        data  = json.load(output)
        df = pd.DataFrame.from_dict(data)
        df
        return str(df)
@app.route('/date')
def dateParse():
    entryDate = request.args.get('date')
    valid = parseDate.validate(entryDate)
    if "success" in valid:
       return "You entered: " + entryDate
    else:
       return "Error: " + valid + "\nUsage: 2019-02-12:2019-03-11"
