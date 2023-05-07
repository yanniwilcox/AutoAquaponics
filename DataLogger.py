from getData import getData
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import numpy as np

all_we_got_now = ('unix_time', 'pH', 'TDS', 'humidity', 'air_temp', 'water_temp', 'distance')
cred = credentials.Certificate("./serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()
print(db)
LOG_EVERY = 15

ref = db.collection(u'tolerances').document(u'pH')

def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        docDict = doc.to_dict()
        print(docDict)
        
doc_watch = ref.on_snapshot(on_snapshot)

def find_next_log_time(x, base):
    maybe = base * round(x/base)
    if maybe < x:
        return maybe + base
    return maybe

def DataLogger():
    distance = np.nan #to give an arbitrary initial value to getData for the first time the distance sensor fails
    wtemp = 21 #arbitrary initial value
    hum = np.nan
    atemp = np.nan
    curr_time = round(time.time())
    time_to_log = find_next_log_time(curr_time, LOG_EVERY * 60)
    
    while True:
        pH, TDS, hum, atemp, wtemp, distance = np.round(getData(distance, wtemp, hum, atemp), 2)
        curr_time = round(time.time())
        if curr_time <= time_to_log:
            continue
        data_tuple = (curr_time, pH, TDS, hum, atemp, wtemp, distance)
        
        data_dict = {}
        for i in range(len(data_tuple)):
            data_dict[all_we_got_now[i]] = data_tuple[i]
        db.collection(u'stats').add(data_dict)
        time_to_log = find_next_log_time(curr_time, LOG_EVERY * 60)
       
DataLogger()