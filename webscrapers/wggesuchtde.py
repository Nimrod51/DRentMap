# -*- coding: utf-8 -*-"""

"""
A web scraper for the german flat search engine website
wg-gesucht.de implementing the Scraper API.
"""

from __future__ import print_function
from .api import Scraper
from .data import Datapoint, Location
import requests
from lxml import html
import unicodedata
import json
import os
from builtins import str
# from umlaut import replace_german_umlaute


class WGGesuchtDE(Scraper):
    def __init__(self, pages=[]):
        Scraper.__init__(self, name="WGGesuchtDE")
        self.pages = pages
        self.gendir()

    def check(self):
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
            i = 1
            for link in links:
                if "wg-gesucht.de" not in link:
                    link = "http://www.wg-gesucht.de/" + link
                # extract ID and create dict
                pageID = int(link.split(".")[-2])
                # does parsed JSON file already exist?
                if os.path.exists(os.path.join(self.datadir, str(pageID)+".json")):
                    continue
                # load ad page HTML
                r = requests.get(link)
                r.encoding = 'utf-8'
                # save raw HTML for future use
                with open(os.path.join(self.datadir, "raw/", str(pageID)+".html"), "w+") as f:
                    print(r.content, file=f)
                detailsTree = html.fromstring(r.content)
                # create new datapoint and save url
                data = Datapoint()
                data.url = link
                # extract adress
                adress = detailsTree.xpath(
                    "//a[contains(@onclick,'map_tab')]/text()")
                adress = [str(s.encode('utf-8'), 'utf-8') for s in adress]
                adress = " ".join((" ".join(adress)).split())
                data.location = Location(adress)
                # extract price
                keyfacts = detailsTree.xpath("//h2/text()")
                data.size = int(keyfacts[0].split("m")[0].split(" ")[-1])
                data.price = int(
                    "".join(_ for _ in keyfacts[1].split("\u20ac")[0] if _ in "1234567890"))
                # output of datapoint
                data.save(os.path.join(self.datadir, str(pageID)))
                # except Exception as e:
                #     print("Flat", i, "failed:", e)
                # wait to prevent over-polling and print status
                self.sleep()
                self.printStatus(i, len(links))
                i += 1

        # call parent to update lastChecked timestamp
        Scraper.check(self)
