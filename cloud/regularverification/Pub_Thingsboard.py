
import datetime
import time
import json
import paho.mqtt.client as mqtt


def PushDataThingsBoard():
    try:
        data = ReadsonFile()
        THINGSBOARD_HOST = "demo.thingsboard.io"
        client = mqtt.Client()
        client.username_pw_set(data['TOKEN'])
        client.connect(THINGSBOARD_HOST, 1883)
        client.publish('v1/devices/me/attributes', json.dumps(data['Value']))
        time.sleep(5)
    except Exception as e:
        print(e)

def PushDataRBI():
    try:
        # data = ReadsonFile()
        # THINGSBOARD_HOST = "demo.thingsboard.io"
        THINGSBOARD_HOST = "127.0.0.1"
        client = mqtt.Client()
        # client.username_pw_set("$K6BEkJp2NbDSNjq87VVe")
        client.connect(THINGSBOARD_HOST, 1883)
        client.publish('v1/devices/me/attributes', json.dumps(ReadsonFile()))
        time.sleep(5)
    except Exception as e:
        print(e)


def on_connect(client, userdata, flags, rc):
    client.subscribe('v1/devices/me/attributes', 0)
    print("Result code " + str(rc))
    if(rc == 0):
        print("Result code " + str(rc) + ": good connection")
    else:
        print("Result code " + str(rc) + ": authentication error")



def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(payload)
    print(msg.topic)

def ReadsonFile():
    with open('datajson/data1.txt') as f:
        data = json.load(f)
    # data1 = data['attribute1']
    # print(data1)
    return data

if __name__=="__main__":
    PushDataRBI()
    PushDataThingsBoard()
    ReadsonFile()