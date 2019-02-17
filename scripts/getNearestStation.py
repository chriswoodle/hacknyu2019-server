# Setup:
# pip install mysql-connector-python 

##usage python getNearestStation.py <mylat> <mylong> <disability> <outputformat>
##disability 0 = none 1 = wheels 2 = eyes
import mysql.connector
from math import sin, cos, sqrt, atan2, radians
import sys

# approximate radius of earth in km
R = 6373.0

lat1 = float(sys.argv[1])
long1 = float(sys.argv[2])
disability = int(sys.argv[3])
outf = sys.argv[4]


def getDistance(lat1, lat2, lon1, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

server = '34.73.12.198'
db = 'rideable'
username = 'cara'
pw = 'carateamzer0'
cnx = mysql.connector.connect(user=username, password=pw,
                              host=server,
                              database=db)

cursor = cnx.cursor()     # get the cursor

tables = cursor.execute("show tables")    # execute 'SHOW TABLES' (but data is not returned

for (table_name,) in cursor:
        ##print(table_name)
    i = 0

cursor.execute("SELECT stop_name, latitude, longitude, accessibility_score FROM station_outages")

result = cursor.fetchall()

currmindist = 9999.5
minlat = 0.0
minlong = 0.0
closest = 'hell'
wflag = 0
vflag = 0

for x in result:
    ##print(x)
    ##print (x[0])
##    print (float(x[1]))
##    print (lat1)
##    print (long1)
##    print (float(x[2]))
    dist =  getDistance(lat1, float(x[1]), long1, float(x[2]))
    ##print (dist)
    if int(x[3]) == 1 or int(x[3]) == 3:
        wflag = 1
    if int(x[3]) == 2 or int(x[3]) == 3:
        vflag = 1
    
    
    if disability == 1 and wflag == 0:
        if dist < currmindist:
            currmindist = dist
            closest = str(x[0])
            ##print (int(x[3]))
            clat = float(x[1])
            clong = float(x[2])
            ##print (closest)
            ##print (dist)
            ##print ('match')
            
    if disability == 2 and vflag == 0:
        if dist < currmindist:
            currmindist = dist
            closest = str(x[0])
            clat = float(x[1])
            clong = float(x[2])
            ##print (closest)
            ##print (dist)
            ##print ('match')

    if disability == 0:
        if dist < currmindist:
            currmindist = dist
            closest = str(x[0])
            clat = float(x[1])
            clong = float(x[2])
            ##print (closest)
            ##print (dist)
            ##print ('match')
    wflag = 0
    vflag = 0
            
if outf == 'text':
    print (closest)

if outf == 'json':
    import json
    res={}
    res['station_name'] = closest
    res['lat'] = clat
    res['lng'] = clong
    print(json.dumps(res))

    with open("nearest.json","w") as f:
        f.write(json.dumps(res))