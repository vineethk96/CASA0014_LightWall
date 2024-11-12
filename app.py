'''
LightWall Application
Description: Used to control the animations for the lightwall in the CE Lab
Name: Vineeth Kirandumkara
Date: 9/11/24

Notes:
Connect and Disconnect code provided by:
https://www.emqx.com/en/blog/how-to-use-mqtt-in-python
'''

import logging
import random
import time
import json
from paho.mqtt import client as mqtt_client

broker = "mqtt.cetools.org"
port = 1884
topic = "UCL/student/CASA0014/light/"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
file = "./cred.txt"
username = ""
password = ""
FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60


# LED Node map for the Christmas Tree
tree = {
    "trunk": [24, 25, 30, 34, 35], 
    "leaves": [16, 19, 20, 22, 23, 28, 29, 32, 33, 36, 37, 41],
    "ornaments": [],
    "star": [26],
    "snow": [3, 5, 7, 9, 11, 14, 17] # Only half the snow is listed
}

pixID_key = "pixelid"
R_key = "R"
G_key = "G"
B_key = "B"
W_key = "W"
bright_key = "brightness"
method_key = "method"
allLed_key = "allLEDs"

class AbcClass:
    def __init__(self, in_object):
        self.obj = in_object

    def dictionary(self):
        obj = self.obj
        return dict(a = obj['id'], b = obj['foo'], c = obj['bar'])

def main():

    christmasTree()
    # user_input = input("Action:")

    # if(user_input.lower() == "christmas tree"):
    #     christmasTree()
    # else:
    #     print("Unknown Input")    

def christmasTree():
    print("Building the Christmas Tree...")

    trunkPixel = {
        pixID_key:0,
        R_key:150,
        G_key:75,
        B_key:0,
        W_key:0
    }

    trunkNode = {
        allLed_key:[trunkPixel]
    }

    for i in range(12):
        trunkPixel.update({pixID_key, i})
        trunkNode[allLed_key].append(trunkPixel)

    print(trunkNode)
        

    # Create JSON items for each LED node
    # Throw them all in an array
    # Have a function to update the tree leaves
    # Have a funtion to update the Ornament Colors
    # Have a function to animate the snow fall
    # Have a function to animate the star (maybe falls under ornament)

    # while(1):
    #     # Update every 500ms
    #     time.sleep(0.5)

        

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
    # For paho-mqtt 2.0.0, you need to add the properties parameter.
    # def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)

    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.on_disconnect = on_disconnect
    return client

def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)

if __name__ == "__main__":
    print("Starting LightWall App...")

    # Pull MQTT username and password
    doc = open(file, "r")
    username = doc.readline()
    password = doc.readline()
    doc.close()
    main()