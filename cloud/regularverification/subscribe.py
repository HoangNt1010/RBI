import os
from django.core.wsgi import get_wsgi_application
os.environ['DJANGO_SETTINGS_MODULE'] = 'RbiCloud.settings'
application = get_wsgi_application()
import datetime
import time
import json
import paho.mqtt.client as mqtt
from cloud import models

# THINGSBOARD_HOST = "127.0.0.1"
THINGSBOARD_HOST = "demo.thingsboard.io"

def SubDATA():
    try:
        print("go SubDATA")
        client = mqtt.Client()
        # client.username_pw_set("$K6BEkJp2NbDSNjq87VVe")
        client.username_pw_set("Xl3AXEbRsuAvctwHLzFA")
        client.connect(THINGSBOARD_HOST, 1883)
        client.on_connect = on_connect
        client.on_message = on_message
        rc = 0
        while rc == 0:
            rc = client.loop()
        print('Result code: ' + str(rc))
    except Exception as e:
        print(e)

def PushData():
    try:
        data1 = {"send_data = json.dumps(data1)":12}
        # THINGSBOARD_HOST = "demo.thingsboard.io"
        client = mqtt.Client()
        # client.username_pw_set("$K6BEkJp2NbDSNjq87VVe")
        client.username_pw_set("Xl3AXEbRsuAvctwHLzFA")
        client.connect(THINGSBOARD_HOST, 1883)
        client.publish('v1/devices/me/attributes', json.dumps(data1))
        time.sleep(5)
    except Exception as e:
        print(e)


def on_connect(client, userdata, flags, rc):

    try:
        print("on_connect")
        client.subscribe('v1/devices/me/attributes', 0)
        print("Result code " + str(rc))
        if(rc == 0):
            print("Result code " + str(rc) + ": good connection")
        else:
            print("Result code " + str(rc) + ": authentication error")
    except Exception as e:
        print(e)



def on_message(client, userdata, msg):
    try:
        print("on_message")
        payload = msg.payload.decode()
        data = json.loads(payload)
        print(data)
        print(data['TOKEN'])
        sensor = models.ZSensor.objects.filter(Token=data['TOKEN'])[0].idsensor
        print(sensor)
        package = models.PackageSensor(idsensor_id=sensor,package=json.dumps(data['Value']))
        package.save()
    except Exception as e:
        print(e)
        print("No sensor")


if __name__=="__main__":
    print ("go main")
    SubDATA()
    # PushData()