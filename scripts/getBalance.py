# pip install google-cloud-datastore
from google.cloud import datastore
import sys
import time
import json

datastore_client = datastore.Client.from_service_account_json('gc.json')

rfid1 = sys.argv[1]
outf = sys.argv[2]

##usage python getBalance.py <rfid> <output format>

if outf == "winspeech":
    import pyttsx3
    engine = pyttsx3.init()

if outf == "linuxspeech":
    import os

if outf == "json":
    outf = ''

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

    ##print('Saved {}: {} {}'.format(user.key.name, user['rfid'], user['balance']))

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




key = datastore_client.key(kind, rfid1)
task = datastore_client.get(key)


balance = task["balance"]

sentence = "your current balance is " + str(balance) + " dollars" 

if outf == "winspeech":
    engine.say(sentence)
    engine.runAndWait()
if outf == "linuxspeech":
    command = 'google_speech "' + sentence + '"' 
    os.system(command)

st = {}
st["balance"] = balance

print (json.dumps(st))

##with open("tstatus.json","w") as f:
##    f.write(json.dumps(st))
