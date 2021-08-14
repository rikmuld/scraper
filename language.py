from itertools import takewhile
from scraper import Scraper


class Program():
    def __init__(self, line=None):
        self.childs = []
        self.level = -1

        if line is not None:
            line_clean = line.lstrip()
            line_split = line_clean.split(":")
            line_scrape_split = ":".join(line_split[1:]).split(" << ")
            line_data = line_scrape_split[0].split(" >> ")

            self.level = (len(line) - len(line_clean))//4
            self.variable = line_split[0]
            self.selector = line_data[0].strip()
            self.fns = self.selector.split(" ")[0]
            self.fns_ext = " ".join(self.selector.split(" ")[1:])
            self.action = line_data[1] if len(line_data) > 1 else None
            self.scrape = len(line_scrape_split) > 1
            
    @staticmethod
    def create_program(lines):
        lines = [Program(line=line) for line in lines]
        root = Program().add_children(lines)[0]
        fns = {child.variable: child for child in root.childs}

        for line in lines:
            if line.fns in fns:
                fn = fns[line.fns]
                line.childs = fn.childs + line.childs
                line.action = line.action if fn.action is None else fn.action
                line.scrape = fn.scrape
                line.selector = fn.selector + line.fns_ext

        return root.childs[-1]

    def add_children(self, lines):
        childs = list(takewhile(lambda x: x.level > self.level, lines))
        tail = lines[len(childs):]

        while len(childs) > 0:
            child, childs = childs[0].add_children(childs[1:])
            self.childs.append(child)

        return self, tail
       
    def __call__(self, scraper=None):
        if scraper is not None:
            scraper = scraper(self.selector)
            if self.action is not None:
                scraper = scraper.text() if self.action == "text" else scraper.get(self.action)

        if self.scrape:
            scraper = Scraper(scraper if scraper is not None else self.selector, True)

        if len(self.childs) > 0:
            result = {child.variable: child(scraper) for child in self.childs}
            if type(scraper) is list or type(scraper.data) is list:
                return [dict(zip(*[result.keys(), x])) for x in list(zip(*result.values()))]    
            return result

        return scraper