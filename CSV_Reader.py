import csv
import itertools
import sys
import math
import requests
import postcodes_io_api
import urllib.request as req
import json
import time
import operator
from mapbox import Geocoder as geo 

lineCount = 0
streetName = None

##Sets the global line count variable so it is only accessed here
def setLineCount(totalLineCount):
    global lineCount
    lineCount = totalLineCount

def getLineCount():
    return lineCount

def getStreetName():
    return streetName


##Gets the total number of lines in the file.  Used to loop through the data
##file
def count_lines(filename):
    with open(filename) as openFile:
        row_count = sum(1 for row in openFile)

    setLineCount(row_count)

## Reads the .csv file selected on the webpage to be read in and returns it the
## chosen line
def load_data(filename, lineNumber): 
    if(lineNumber <= getLineCount()):
        with open(filename) as openFile:
            csv_reader = csv.reader(openFile, delimiter=',')  
            if(getLineCount() is 0): ##Checks for dividing by zero
                string = next(itertools.islice(csv_reader, lineNumber, None))
            else:
                string = next(itertools.islice(csv_reader, lineNumber % getLineCount(), None))
           
            return string
    else:
        return None

def save_data(filename, data, imagename):
    reader = csv.reader(open(filename, 'r'))
    writer = csv.writer(open('testfile.csv', 'a', newline=''))
    string = next(itertools.islice(reader, data, None))
    string.append(imagename)
    writer.writerow(string)

def processData(dataFile):

    count_lines(dataFile)
    reader = csv.reader(open(dataFile, 'r'))

    with open('File Path', 'w+', newline='') as file:
        areaFile = csv.writer(file)
        areaFile.writerow(['Crime ID','Month','Latitude','Longitude','Location','Category','Area'])
    
        #Gets the 'admin_ward' of the entry and appends it to the string before writing it to the CSV
        #If no ward is found, calls findWard() which checks neaby locations to see if they have a ward
        a = 1
        while(a < getLineCount()):
            entry = getString(dataFile, a)
            crimeArea = checkArea(entry)
            if(crimeArea is None):
                for i in range(1, 5):
                    crimeArea = findWard(entry, i)
                    if(crimeArea is not None):
                        break
            entry.append(crimeArea)
            areaFile.writerow(entry)
            a+=1
    

    generateData()


def generateData():
    #Loads Areas.csv, gets the first entry, reads the Area as areaName and creates a CSV file using areaName
    count_lines('Areas.csv')
    dataFile = 'Areas.csv'
    reader = csv.reader(open(dataFile, 'r')) 
    
    sortData(reader)

    reader = csv.reader(open('CrimeData/Sorted.csv', 'r'))
    writer = csv.writer(open('CSV To Write To', 'w+', newline=''))

    count = 0
    a = 0
    while(a < getLineCount()):
        crimeAddress = getString(dataFile, a)
        address = getString(dataFile, a)
        
        #If area of current address has changed, then open the file for the area           
        if(address[6] == 'Newsome'):
            setStreetName(address)
            for i in range(0,4):
                address.append(90*i)
                writer.writerow(address)
                address.remove(90*i)
 
            for j in range(0, 360, int(30)):
                #Sleep needed as MapBox has a limit of 600 requests 
                time.sleep(0.1)
                string = generateRandomPoints(address, 1, j) 
                if(checkStreet(crimeAddress, string)):
                    k = 0
                    #Generates 4 points at 90 degree intervals for a 360 degree view of the area
                    while(k < 4):
                        string.append(90 * k)
                        writer.writerow(string) 
                        string.remove(90 * k)
                        count += 1
                        k+=1
        a+=1
 
def getString(file, line):
    reader = csv.reader(open(file, 'r'))
    string = next(itertools.islice(reader, line, None))
    return string

def sortData(reader):
    writer = csv.writer(open('CrimeData/Sorted.csv', 'w+', newline=''))    
    sortedlist = sorted(reader, key=lambda row: row[6], reverse=False)
    writer.writerows(sortedlist)

def findWard(entry, i):   
    for j in range(0, 360, int(30)):
        string = generateRandomPoints(entry, i, j)
        crimeArea = checkArea(string)
        if(crimeArea is not None):
            return crimeArea    
    

def generateRandomPoints(address, i, j): 
    x = i/111111
    lat = math.radians(float(address[2]))
    long = math.radians(float(address[3]))
    y = math.radians(j)
    latRadians = math.asin(math.sin(lat) * math.cos(x) + math.cos(lat) * math.sin(x) * math.cos(y))
    longRadians = long + math.atan2(math.sin(y) * math.sin(x) * math.cos(lat), math.cos(x) - math.sin(lat) * math.sin(latRadians))
    address[2] = math.degrees(latRadians)
    address[3] = math.degrees(longRadians)

    return address

def checkArea(address):
    
    api  = postcodes_io_api.Api(debug_http=True)
   
    payload_data = payload_data = {
    "geolocations":
        [{
            "longitude": address[3],
            "latitude": address[2]
        }]
    }
    try:
        return api.get_bulk_reverse_geocode(payload_data).get('result')[0].get('result')[0].get('admin_ward')
    except:
        return None

def setStreetName(address):
    global streetName
    geocode = geo(access_token="Access_Token")
    response = geo.reverse(geocode, lon=address[3], lat=address[2])

    streetName = (response.json().get('features')[0].get('text'))


def checkStreet(start, address):

    geocode = geo(access_token="Access_Token")
    response = geo.reverse(geocode, lon=address[3], lat=address[2])

    if(getStreetName() == response.json().get('features')[0].get('text')):        
        return True
    else:
        return False    