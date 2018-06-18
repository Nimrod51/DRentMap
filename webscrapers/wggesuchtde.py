# -*- coding: utf-8 -*-"""

"""
A web scraper for the german flat search engine website
wg-gesucht.de implementing the Scraper API.
"""

from __future__ import print_function
from api import Scraper
import requests
from lxml import html
import unicodedata
import json
import os


class WGGesuchtDE(Scraper):
    def __init__(self, location=None):
        Scraper.__init__(self, location)
        self.name = "WGGesuchtDE"
        # TODO: Münster is hard-coded. Make general to every location
        self.pages = ["http://www.wg-gesucht.de/wg-zimmer-in-Muenster.91.0.1."
                      + str(i)+".html" for i in range(0, 5)]
        self.gendir()

        # TODO: deal with all that unicde...

    def check(self):
        Scraper.check(self)
        for page in self.pages:
            # load main page (result list) HTML
            mainPage = requests.get(page)
            mainTree = html.fromstring(mainPage.content)
            # filter for interesting links
            links = mainTree.xpath("//a[@class='detailansicht']/@href")
            # filter advertising
            links = [link for link in links if "affiliate" not in link]
            links = [link for link in links if "airbnb" not in link]
            # remove duplicates in list
            links = list(set(links))
            # open links and get their info
            i = 0
            for link in links:
                if "wg-gesucht.de" not in link:
                    link = "http://www.wg-gesucht.de/" + link
                # extract ID and save to dict
                details = {}
                pageID = int(link.split(".")[-2])
                details["id"] = pageID
                # does parsed JSON file already exist?
                if os.path.exists(os.path.join(self.datadir, str(pageID)+".json")):
                    continue
                # load ad page HTML
                detailsPage = requests.get(link).content
                detailsTree = html.fromstring(detailsPage)
                self.sleep()
                self.printStatus(i, len(links))
                i += 1
                # extract price
                try:
                    keyfacts = detailsTree.xpath("//h2/text()")
                    details["price"] = int(
                        "".join(_ for _ in keyfacts[1].split("\u20ac")[0] if _ in "1234567890"))
                except Exception:
                    pass
                # extract adress
                try:
                    adress = detailsTree.xpath(
                        "//a[contains(@onclick,'map_tab')]/text()")
                    adress = [s.encode('utf-8') for s in adress]
                    adress = " ".join(adress)
                    adress = " ".join(adress.split())
                    details["adress"] = adress
                except Exception:
                    pass
                self.output(details, pageID)
