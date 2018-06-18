from output import DATADIR
import os


class Scraper():
    """
    An interface, that each web scraper implements
    """

    def __init__(self):
        self.name = "ScraperAPI"

    def lastChecked(self):
        # get date of last check of the website
        pass
        with open(os.path.join(DATADIR, )) as f:
            try:
                return int(f.read())
            except Exception:
                return -1

    def check(self):
        # check for new datapoints on the website
        pass
