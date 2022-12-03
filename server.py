# python3.6

import random
import json
import time
import datetime

from paho.mqtt import client as mqtt_client




broker = 'zebra.rainbow-project.online'
port = 1883
topic = "teamB/#"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'teamB-cloud'
password = '77Jsf'

def compute(results1, results2):
    final = [(results1[0] + results2[0]) / 2,
             (results1[1] + results2[1]) / 2,
             (results1[2] + results2[2]) / 2,
             results1[3].update(results2[3])]

    return final

def show(final):
    print('time : ', datetime.datetime.now())
    print('combined Min value: ', final[0])
    print('combined Max value: ', final[1])
    print('combined Average value: ', final[2])
    print('combined Outliers: ', final[3])


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client



def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):# TODO add here the logic of the server
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        message = json.loads(msg.payload)

        print(msg.topic)
        show([message['min_val'],
             message['max_val'],
             message['avg'],
             message['outliers']])




    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
