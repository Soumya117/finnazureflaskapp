from json2html import *

def html(data):
    f_table = json2html.convert(json = data)
    finn_html= open("templates/finn_links.html","w")
    finn_html.write(f_table)
    finn_html.close()
 
