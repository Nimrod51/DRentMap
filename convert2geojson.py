# -*- coding: utf-8 -*-
import json, geojson
import os
from geopy.geocoders import Nominatim

script_dir = os.path.dirname(os.path.abspath(__file__))
rel_path1 = "data"
rel_path2 = "WGGesuchtDE"
source_dir = os.path.join(script_dir, rel_path1, rel_path2)

result = []
for f in os.listdir(source_dir):
    if f.endswith(".json"):
        with open(os.path.join(source_dir,f), "rb") as infile:
            result.append(json.load(infile))


#Create merged JSON file (optional)
#with open(source_dir + "\\merged_file.json", "wb") as outfile:
#     json.dump(result, outfile)

def formatAddress(address):
    fullAddress=address.split(' ')
    simpleAddress=fullAddress[:len(fullAddress)-1]
    return ' '.join(simpleAddress)


#Iterate over each result and geocode the address
geolocator = Nominatim(user_agent="rent-application",timeout=3)
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
with open(os.path.join(source_dir,"result.geojson"), "w") as outfile:
    outfile.write(variableStr)
    geojson.dump(fc, outfile)
