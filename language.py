from itertools import takewhile
from scraper import Scraper


class Program():
    def __init__(self, lines=None, line=None):
        if line is None:
            line = lines[0]

        data = line.lstrip()
        self.level = (len(line) - len(data))//4
        data = data.split(":")
        self.variable = data[0]
        data = ":".join(data[1:]).split(" >> ")
        self.selector = data[0].strip()
        self.action = data[1] if len(data) > 1 else None
        self.childs = []
        
        if lines is not None:
            self.add_children([Program(line=line) for line in lines[1:]])

    def add_children(self, lines):
        childs = list(takewhile(lambda x: x.level > self.level, lines))
        tail = lines[len(childs):]

        while len(childs) > 0:
            child, childs = childs[0].add_children(childs[1:])
            self.childs.append(child)

        return self, tail
       
    def __call__(self, scraper=None):
        scraper = Scraper(self.selector) if scraper is None else scraper(self.selector)
        
        if len(self.childs) > 0:
            result = {child.variable: child(scraper) for child in self.childs}

            if len(result) > 1 and type(scraper.data) is list:
                return [dict(zip(*[result.keys(), x])) for x in list(zip(*result.values()))]
            
            return result
        else:
            return scraper.text() if self.action == "text" else scraper.get(self.action)