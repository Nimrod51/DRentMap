from __future__ import print_function
from webscrapers import WGGesuchtDE


scraper = WGGesuchtDE()

scraper.check()

print(scraper.lastChecked)
