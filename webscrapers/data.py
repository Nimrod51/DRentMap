"""
Wrapper classes for the data.
"""
# TODO: should these classes be moved somewhere else for reusage?

from __future__ import print_function
import time
import json

# directory where all data will be stored
DATADIR = "data/"


class Datapoint():
    """
    A wrapper class for data points on rent pricings and locations
    """

    def __init__(self, location=None, price=None, date=None):
        self.location = location
        self.price = price
        self.date = int(time.time()) if date is None else date

    # return Datapoint as dict
    def asDict(self):
        return {
            "location": self.location.name,
            "price": self.price,
            "date": self.date
        }

    # store Datapoint as JSON file
    def save(self, filepath):
        if filepath[:-5] != ".json" and filepath[:-5] != ".JSON":
            filepath += ".json"
        with open(filepath, "w+") as outf:
            print(json.dumps(self.asDict()), file=outf)

    # make Datapoint form dict
    @staticmethod
    def fromDict(data):
        result = Datapoint()
        result.location = Location(data["location"])
        result.price = float(data["price"])
        result.date = int(data["date"])
        return result

    # load Datapoint form JSON file
    @staticmethod
    def load(filepath):
        with open(filepath) as inf:
            data = json.loads(inf.read())
        return Datapoint.fromDict(data)


class Location():
    """
    A wrapper class for the target location
    including geo information about the city center and more.
    To be used by the Scraper API.
    """

    # constructor with flexible arguments
    def __init__(self, *args):
        # TODO: can information be fetched from a geo API?
        # TODO: which information is the most relevant to scrapers
        self.name = None
        self.longitude = None
        self.latitude = None
        if len(args) == 1:
            # if there is only one argument, it's the name
            self.name = args[0]
        if len(args) == 2:
            # if there is two arguments, it's longitude and latitude
            self.longitude = args[0]
            self.latitude = args[1]
