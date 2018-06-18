from __future__ import print_function
from output import DATADIR
import os


class Scraper():
    """
    An interface, that each web scraper implements
    """

    def __init__(self, location=None):
        self.name = "ScraperAPI"
        self.location = location

    def setLocation(self, location):
        self.location = location

    # get date of last check of the website
    @property
    def lastChecked(self):
        with open(os.path.join(DATADIR, self.name + ".lastcheck.ini")) as f:
            try:
                return int(f.read())
            except Exception:
                return -1

    # check for new datapoints on the website
    def check(self):
        # update lastChecked
        with open(os.path.join(DATADIR, self.name
                               + ".lastcheck.ini"), "w+") as f:
            import time
            print(int(time.time()), file=f)
