from __future__ import print_function
from output import DATADIR
import os


class Scraper():
    """
    An interface, that each web scraper implements
    """

    def __init__(self):
        self.name = "ScraperAPI"

    @property
    def lastChecked(self):
        # get date of last check of the website
        with open(os.path.join(DATADIR, self.name + ".lastcheck.ini")) as f:
            try:
                return int(f.read())
            except Exception:
                return -1

    def check(self):
        # check for new datapoints on the website
        import time
        with open(os.path.join(DATADIR, self.name
                               + ".lastcheck.ini"), "w+") as f:
            print(int(time.time()), file=f)
