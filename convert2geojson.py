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
successCount=0
errorCount=0

try:

    for r in result:
        address = r['location']
        xy = geolocator.geocode(formatAddress(address))
        
        if xy is not None:
            feat = geojson.Feature(geometry=geojson.Point((xy.point[1],xy.point[0])))
            feat.properties = r
            features.append(feat)
            successCount+=1
        else:
            print ("No result for: ", r['location'])
            errorCount+=1

    print ('total SUCCESSFULY geocoded: ', successCount)        
    print ('total NOT geocoded: ', errorCount)

except:
    "Too many requests to Nominatim, try again later"


#Write result to geojson file
fc = geojson.FeatureCollection(features)
variableStr='var locations='.strip('"')
with open(source_dir + "\\result.geojson", "w") as outfile:
    json.dump(variableStr,outfile)
    geojson.dump(fc, outfile)
