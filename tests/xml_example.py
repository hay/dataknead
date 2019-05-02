from _context import dataknead
from dataknead import Knead

def parse(data):
    books = data["catalog"]["book"]
    data["catalog"]["book"] = [b for b in books if b["author"] == "O'Brien, Tim"]
    return data

Knead("input/books.xml").apply(parse).write("output/obrien-books.xml")