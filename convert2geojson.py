# -*- coding: utf-8 -*-
import json, geojson
import glob
from geopy.geocoders import Nominatim

source_dir=".\data\WGGesuchtDE\\"


result = []
for f in glob.glob(source_dir + "*.json"):
    with open(f, "rb") as infile:
        result.append(json.load(infile))

#Create merged JSON file (optional)
#with open(source_dir + "\\merged_file.json", "wb") as outfile:
#     json.dump(result, outfile)

def formatAddress(address):
    fullAddress=address.split(' ')
    simpleAddress=fullAddress[:len(fullAddress)-1]
    return ' '.join(simpleAddress)


#Iterate over each result and geocode the address
geolocator = Nominatim(timeout=3)
features=[]
count=1

for r in result:
    address = r['location']
    xy = geolocator.geocode(formatAddress(address))
    
    if xy is not None:
        feat = Feature(geometry=Point((xy.point[1],xy.point[0])))
        feat.properties = r
        features.append(feat)
    else:
        print ("No result for: ", r['location'])
        count+=1
print ('total NOT geocoded: ', count)

#Write result to geojson file
fc = FeatureCollection(features)
with open(source_dir + "\\result.geojson", "w") as outfile:
     geojson.dump(fc, outfile)
