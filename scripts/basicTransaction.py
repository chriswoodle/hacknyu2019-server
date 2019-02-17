from google.cloud import datastore
import sys
import time
import json

datastore_client = datastore.Client.from_service_account_json('gc.json')

rfid1 = sys.argv[1]

kind = 'accounts'

##econrows = numrows - numfirst

##disability: 0 = none, 1 = wheelchair, 2 = low vision, 3 = both


def init_account(name, username, rfid, disability, imgurl):
    user_key = datastore_client.key(kind, name)

    user = datastore.Entity(key = user_key)
    user['name'] = username
    user['rfid'] = rfid
    user['balance'] = 50.0
    user['disability'] = disability
    user['concurrent'] = 0
    user['chargeTo'] = rfid
    user['timelastcharged'] = 0
    user['pic'] = imgurl

    datastore_client.put(user)

    print('Saved {}: {} {}'.format(user.key.name, user['rfid'], user['balance']))

def upsert_user(name, username, rfid, disability, imgurl, balance, concurrent, chargeTo, timelast):
    complete_key = datastore_client.key(kind, name)

    user = datastore.Entity(key = complete_key)

    user.update({
        'name': username,
        'rfid': rfid,
        'balance': balance,
        'disability': disability,
        'concurrent': concurrent,
        'chargeTo': chargeTo,
        'timelastcharged': timelast,
        'pic': imgurl
        
    })

    datastore_client.put(user)
    



project_id = 'aiot-fit-xlab'


##init_account('chris', 'chris', '8D0BA00B', 1, 'https://storage.googleapis.com/hacknyu2019/chris.jpg')
##init_account('cara', 'cara', 'DD14A10B', 0, 'https://storage.googleapis.com/hacknyu2019/cara.jpg')
##init_account('muntaser', 'muntaser', 'FDDC930B', 2, 'https://storage.googleapis.com/hacknyu2019/muntaser.jpg')
##


##upsert_seat('24A', 'mr tubes', 'tubesrox', 'yes')


##query = datastore_client.query(kind=kind)
##
##query.add_filter('rfid', '=', rfid1)
##
##results = list(query.fetch())
##print ('here')
##for r in results:
##    print (r)


key = datastore_client.key(kind, rfid1)
task = datastore_client.get(key)

##print (task)
##print (type(task))
##print (task["balance"])

##test valid transaction
newbalance = task["balance"]
balance = task["balance"]
if int(task['disability']) > 0 :
    multiplier = 0.5
else:
    multiplier = 1.0

okflag = 0
concurrent = task['concurrent']
timelast = task['timelastcharged']

if task['rfid'] == task ['chargeTo']:
    newbalance = balance - (2.7 * multiplier)
    newbalance = round(newbalance, 2)
    t = int(time.time())
    difft = t - task['timelastcharged']
    if  concurrent >3 and difft < 600:
        okflag = 1
    else:
        if concurrent > 3:
            if difft > 600:
                concurrent = concurrent - 1
            if difft > 900:
                concurrent = concurrent - 2
            if difft > 1200:
                concurrent = concurrent - 3
        concurrent = concurrent + 1
        timelast = t
    if newbalance < 0:
        okflag = 1
else:
    rfid2 = task['chargeTo']
    key2 = datastore_client.key(kind, rfid2)
    task2 = datastore_client.get(key2)
    balance2 = task2["balance"]
    newbalance2 = balance2
    concurrent2 = task2['concurrent']

    newbalance2 = balance2 - (2.7 * multiplier)
    newbalance2 = round(newbalance2, 2)
    t = int(time.time())
    difft = t - task2['timelastcharged']
    if  concurrent2 >3 and difft < 600:
        okflag = 1
    else:
        if concurrent2 > 3:
            if difft > 600:
                concurrent2 = concurrent2 - 1
            if difft > 900:
                concurrent2 = concurrent2 - 2
            if difft > 1200:
                concurrent2 = concurrent2 - 3
        concurrent2 = concurrent2 + 1
        timelast2 = t
    if newbalance2 < 0:
        okflag = 1

    if okflag == 0:
       upsert_user(rfid2, task2['name'], rfid2, task2['disability'], task2['pic'], newbalance2, concurrent2, rfid2, timelast2)
       t = int(time.time())
       difft = t - task['timelastcharged']
       if  concurrent >1 and difft > 600:
           concurrent = concurrent - 1

    
    
if okflag == 0:
    upsert_user(rfid1, task['name'], rfid1, task['disability'], task['pic'], newbalance, concurrent, rfid1, timelast)
    print ('updated')
    status = 'updated'
else: 
    print ('done')
    status = 'error'

st = {}
st["status"] = status


with open("tstatus.json","w") as f:
    f.write(json.dumps(st))




