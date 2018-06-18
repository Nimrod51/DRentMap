"""
A web scraper for the german flat search engine website
wg-gesucht.de implementing the Scraper API.
"""

from api import Scraper


class WGGesuchtDE(Scraper):
    def __init__(self):
        self.name = "WGGesuchtDE"

    def check(self):
        Scraper.check(self)
