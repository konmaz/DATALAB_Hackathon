import json
import requests
import time
import paho.mqtt.client as paho


def manhattan(a, b):
    return abs(a-b)

# return a dictionary with the results
def get_values():
    fog_type = 'badger'  # beetle, badger #TODO Edo
    url = 'http://' + fog_type + '.rainbow-project.online:50000/get'
    ts = int(time.time())
    window = 60
    value = ts - window
    payload = {'metricID': ['Voltage'], 'from': str(ts - window)}

    fog1_json = requests.post(url, json=payload)

    x = json.loads(fog1_json.text)['monitoring'][0]['data'][0]['values']

    min_val = x[0]['val']
    max_val = x[0]['val']
    sum = 0
    for item in x:
        sum += item['val']

        if min_val >= item['val']:
            min_val = item['val']

        if max_val <= item['val']:
            max_val = item['val']

    avg = sum / len(x)
    R = 150
    outliers = []

    for item in x:
        if manhattan(item['val'], avg) >= R:
            outliers.append(item)

    result = {'min_val' : min_val,
              'max_val': max_val,
              'avg' : avg,
              'outliers':outliers,
    }

    return result
