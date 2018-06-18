"""
A wrapper class for the target location
including geo information about the city center and more.

To be used by the Scraper API.
"""
# TODO: should this class be moved somewhere else for reusage?


class Location():

    # constructor with flexible arguments
    def __init__(self, **args):
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
