"""
A module with a common API for all web scrapers / crawlers for rental
data acquisition from popular sites.
"""

from .wggesuchtde import WGGesuchtDE
from .data import Location, Datapoint, DATADIR


__all__ = [
           "Location", "Datapoint", "DATADIR",
           "WGGesuchtDE"
           ]
