def link_exists(url, links):
    data = [x['link'] for x in links['links']]
    return (lambda item, elements: item in elements)(url, data)
