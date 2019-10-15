import requests
from bs4 import BeautifulSoup


class HtmlUtil:
    def __init__(self, url, skip_prep_price=False):
        self.url = url
        self._prepare_soup()
        if not skip_prep_price:
            self._prepare_price()

    def _prepare_soup(self):
        html = requests.get(self.url)
        self.soup = BeautifulSoup(html.text, 'lxml')

    def _prepare_price(self):
        pris_rows = self.soup.find_all('span')
        i = 0
        for row in pris_rows:
            i = i + 1
            if "Prisantydning" in row:
                break
        pris = pris_rows[i].get_text().strip()
        self.price = pris.replace(u"\u00A0", " ")

    def get_soup(self):
        return self.soup

    def get_price(self):
        return self.price
