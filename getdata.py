from __future__ import print_function
from webscrapers import WGGesuchtDE, Location


scraper = WGGesuchtDE()

ms = Location("Münster")

scraper.setLocation(ms)

scraper.check()

print(scraper.lastChecked)
