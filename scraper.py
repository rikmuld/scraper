import requests as req
import validators
from bs4 import BeautifulSoup as BS


class Scraper:
    def __init__(self, data, maybe_url=False):
        if type(data) is not list:
            data = [data]
        if maybe_url:
            data = [Scraper.scrape(x) for x in data]
        if len(data) == 1:
            data = data[0]
        
        self.data = data
        
    def do(self, f, g):
        return Scraper([f(Scraper(x)) for x in self.data] if type(self.data) == list else g(self.data))
        
    def __call__(self, query):
        return self.do(lambda x: x(query).data, lambda x: list(x.select(query)))
        
    def text(self):
        return self.do(lambda x: x.text(), lambda x: [x.text.strip()]).data
    
    def get(self, attr):
        return self.do(lambda x: x.get(attr), lambda x: [x.get(attr).strip()]).data

    @staticmethod
    def scrape(url):
        print(f"Scrapping {url}...")
        return BS(req.get(url).text, features="lxml")