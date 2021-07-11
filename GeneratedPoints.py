import math
import csv

def generateRandomPoints(latitude, longitude, i, j): 
    x = i/111111
    print(x)
    lat = math.radians(float(latitude))
    long = math.radians(float(longitude))
    y = math.radians(j)
    latRadians = math.asin(math.sin(lat) * math.cos(x) + math.cos(lat) * math.sin(x) * math.cos(y))
    longRadians = long + math.atan2(math.sin(y) * math.sin(x) * math.cos(lat), math.cos(x) - math.sin(lat) * math.sin(latRadians))
    latitude = math.degrees(latRadians)
    longitude = math.degrees(longRadians)
    address = [latitude, longitude]
    print(str(latitude) + ', ' + str(longitude) + ', ' + 'Print')
    return address

def testRandomPoints(address, i, j): 
    x = i/111111
    lat = math.radians(float(address[0]))
    long = math.radians(float(address[1]))
    y = math.radians(j)
    latRadians = math.asin(math.sin(lat) * math.cos(x) + math.cos(lat) * math.sin(x) * math.cos(y))
    longRadians = long + math.atan2(math.sin(y) * math.sin(x) * math.cos(lat), math.cos(x) - math.sin(lat) * math.sin(latRadians))
    address[0] = math.degrees(latRadians)
    address[1] = math.degrees(longRadians)
    return address

	
def run():
    writer = csv.writer(open('K:/Book1.csv', 'w+', newline=''))
    lat = 53.63804698 
    long = -1.77954088
    writer.writerow(['latitude', 'longitude', 'method'])
    writer.writerow([lat, long, 'start'])
    for j in range(0, 360, int(30)):
        string = generateRandomPoints(lat, long, 1, j)
        string.append("Wut")
        writer.writerow(string)
        string = generateRandomPoints(lat, long, 5, j)
        string.append("second")
        writer.writerow(string)
        
    for y in range(0, 360, int(30)):
        string = testRandomPoints([lat,long], 5, y)
        string.append('Test')
        writer.writerow(string)
    #for x in range(0, 360, int(30)):
     #   address = [lat,long]
      #  string = testRandomPoints(address, 5, x)
       # string.append('X')
        #writer.writerow(string)

if __name__ == '__main__':
    run()
