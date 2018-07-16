# -*- coding: utf-8 -*-"""
from __future__ import print_function
from webscrapers import WGGesuchtDE, Location


scraper = WGGesuchtDE(["http://www.wg-gesucht.de/wg-zimmer-in-Muenster.91.0.1."
                       + str(i)+".html" for i in range(0, 5)])

ms = Location("Münster")

scraper.setLocation(ms)

scraper.check()

# scraper.reparseRawHTML()

print(scraper.lastChecked)
