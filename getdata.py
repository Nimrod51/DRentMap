# -*- coding: utf-8 -*-"""
from __future__ import print_function
from webscrapers import WGGesuchtDE, Location


scraper = WGGesuchtDE(["http://www.wg-gesucht.de/wohnungen-in-Duisburg.28.2.1."
                       + str(i)+".html" for i in range(0, 1)])

du = Location("Duisburg")

scraper.setLocation(du)

scraper.check()

# scraper.reparseRawHTML()

print(scraper.lastChecked)
