import requests as req
from bs4 import BeautifulSoup as BS


class Scraper:
    def __init__(self, data):
        if type(data) is str:
            self.data = BS(req.get(data).text, features="lxml")
        elif type(data) == list and len(data) == 1:
            self.data = data[0]
        else:
            self.data = data
        
    def do(self, f, g):
        return Scraper([f(Scraper(x)) for x in self.data] if type(self.data) == list else g(self.data))
        
    def __call__(self, query):
        return self.do(lambda x: x(query).data, lambda x: list(x.select(query)))
        
    def text(self):
        return self.do(lambda x: x.text(), lambda x: [x.text.strip()]).data
    
    def get(self, attr):
        return self.do(lambda x: x.get(attr), lambda x: [x.get(attr).strip()]).data