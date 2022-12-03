import json
import requests
import time
import paho.mqtt.client as paho
from paho import mqtt

def manhattan(a, b):
    return abs(a-b)

fog_type ='badger'    #beetle, badger
url = 'http://'+fog_type+'.rainbow-project.online:50000/get'
ts = int(time.time())
window = 60
value = ts - window
payload = {'metricID': ['Voltage'], 'from':str(ts - window)}

fog1_json = requests.post(url, json = payload)

print(fog1_json.text)

resp = json.loads(fog1_json.text)
x = json.loads(fog1_json.text)['monitoring'][0]['data'][0]['values']

min_val = x[0]['val']
max_val = x[0]['val']
sum = 0
for item in x:
    print(item['val'])
    sum+= item['val']

    if min_val >= item['val']:
        min_val = item['val']

    if max_val <= item['val']:
        max_val = item['val']

print(len(x))
avg = sum / len(x)
R = 150
outliers =[]


for item in x:
    if manhattan(item['val'],avg) >= R:
        outliers.append(item)


print(max_val, min_val, avg)
print(outliers)

results = [max_val, min_val, avg, outliers]

MQTT_SERVER = "zebra.rainbow-project.online"
MQTT_PATH = "teamB/fog1"

mqttc = paho.Client()
mqttc.connect(MQTT_SERVER, 1883, 60)

while True:
    MQTT_MESSAGE = json.dumps(results)
    mqttc.publish(MQTT_PATH, MQTT_MESSAGE)
    mqttc.loop()
    time.sleep(1)