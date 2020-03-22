import paho.mqtt.client as mqtt
import json
import uuid
import os
import sys


fileout_json = open("mqtt.txt","a")
clnt_id = uuid.uuid4()
target = 'ipgoeshere'#sys.argv[1]



def on_connect(client, userdata, flags, rc):
    print ("[+] Connection successful")
    client.subscribe('#', qos = 1)        # Subscribe to all topics
    client.subscribe('$SYS/#')   # Broker Status (Mosquitto)

def on_message(client, userdata, msg):
    try:
       if "$SYS" not in msg.topic:
           print ('[+] Topic: %s - Message: %s' % (msg.topic, msg.payload))
           topic = {}
           topic['topic']= msg.topic
           topic['payload']= msg.payload
           final_info = json.dumps(topic)
           fileout_json.write(final_info+"\n")
       else:
           pass
    except:
       pass

def dump_mqtt(host):
    client = mqtt.Client(client_id =str(clnt_id))
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, 1883, 60)
    client.loop_forever()

def main():
    try:
       dump_mqtt(target)
    except:
       pass

main()
