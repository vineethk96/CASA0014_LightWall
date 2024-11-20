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
topic = "student/CASA0014/light/"
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
    "leaves": [12, 15, 16, 19, 20, 22, 23, 27, 28, 29, 32, 33, 38, 39, 42, 43, 47],
    "ornaments": [],
    "star": [26],
    "snow": [1, 4, 6, 9, 18, 36, 41, 44, 49, 52] # Only half the snow is listed
}

clearMsg = {"method": "clear"}
trunkNode = [
            {"pixelid":0,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            },
            {"pixelid":1,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            },
            {"pixelid":2,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            },
            {"pixelid":3,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            },
            {"pixelid":4,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            },
            {"pixelid":5,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            },
            {"pixelid":6,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            },
            {"pixelid":7,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            },
            {"pixelid":8,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            },
            {"pixelid":9,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            },
            {"pixelid":10,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            },
            {"pixelid":11,
             "R": 150,
             "G": 75,
             "B": 0,
             "W": 0
            }
        ]
leafNode = [
            {"pixelid":0,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            },
            {"pixelid":1,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            },
            {"pixelid":2,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            },
            {"pixelid":3,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            },
            {"pixelid":4,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            },
            {"pixelid":5,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            },
            {"pixelid":6,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            },
            {"pixelid":7,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            },
            {"pixelid":8,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            },
            {"pixelid":9,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            },
            {"pixelid":10,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            },
            {"pixelid":11,
             "R": 66,
             "G": 205,
             "B": 47,
             "W": 0
            }
        ]
starNode = [
            {"pixelid":0,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            },
            {"pixelid":1,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            },
            {"pixelid":2,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            },
            {"pixelid":3,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            },
            {"pixelid":4,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            },
            {"pixelid":5,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            },
            {"pixelid":6,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            },
            {"pixelid":7,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            },
            {"pixelid":8,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            },
            {"pixelid":9,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            },
            {"pixelid":10,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            },
            {"pixelid":11,
             "R": 255,
             "G": 255,
             "B": 0,
             "W": 0
            }
        ]
snowNode = [
            {"pixelid":0,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            },
            {"pixelid":1,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            },
            {"pixelid":2,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            },
            {"pixelid":3,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            },
            {"pixelid":4,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            },
            {"pixelid":5,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            },
            {"pixelid":6,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            },
            {"pixelid":7,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            },
            {"pixelid":8,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            },
            {"pixelid":9,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            },
            {"pixelid":10,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            },
            {"pixelid":11,
             "R": 255,
             "G": 250,
             "B": 250,
             "W": 0
            }
        ]

delay = 0.5

def run():
    client = connect_mqtt()
    client.loop_start()
    christmasTree(client)
    client.loop_stop()

def christmasTree(client):
    print("Building the Christmas Tree...")

    # Clear all Lights
    for i in range(1, 54, 1):
        newTopic = topic + f"{i}/all/"
        publish(client, newTopic, clearMsg)
        time.sleep(delay)

    # Light up the basic Tree Trunk
    for i in range(len(tree["trunk"])):
        newTopic = topic + f"{tree['trunk'][i]}/all/"
        newMsg = {"allLEDs": trunkNode}
        publish(client, newTopic, newMsg)
        time.sleep(delay)

    # Light up the basic Tree Leaves
    for i in range(len(tree["leaves"])):
        newTopic = topic + f"{tree["leaves"][i]}/all/"
        newMsg = {"allLEDs": leafNode}
        publish(client, newTopic, newMsg)
        time.sleep(delay)

    # Light up the snow
    for i in range(len(tree["snow"])):
        newTopic = topic + f"{tree["snow"][i]}/all/"
        newMsg = {"allLEDs": snowNode}
        publish(client, newTopic, newMsg)
        time.sleep(delay)

    # Light up the Star
    newTopic = topic + f"{tree['star'][0]}/all/"
    newMsg = {"allLEDs": starNode}
    publish(client, newTopic, newMsg)
    time.sleep(delay)


    while True:
        time.sleep(delay)

        

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
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
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

def publish(client, newTopic, newMsg):
    result = client.publish(newTopic, f"{newMsg}")
    status = result[0]
    if status == 0:
        print(f"Send `{newMsg}` to topic `{newTopic}`")
    else:
        print(f"Failed to send message to topic {newTopic}")

if __name__ == '__main__':
    print("Starting LightWall App...")

    # Pull MQTT username and password
    doc = open(file, "r")
    username = doc.readline().strip()
    password = doc.readline().strip()
    print("username: " + username)
    print("password: " + password)
    doc.close()
    run()