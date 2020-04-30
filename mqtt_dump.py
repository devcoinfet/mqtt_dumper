import paho.mqtt.client as mqtt
import json
from signal import signal, SIGINT
from sys import exit
import codecs

results_file = open("new.txt","w")



def handler(signum, frame):
    print('Ctrl+C pressed exiting gracefully still')
    results_file.flush()
    results_file.close()
    exit(0)

def on_connect(client, userdata, flags, rc):
   print("[+] Connection successful")
   client.subscribe('#', qos = 1)        # Subscribe to all topics
   client.subscribe('$SYS/#')            # Broker Status (Mosquitto)

def on_message(client, userdata, msg):
   #print('[+] Topic: %s - Message: %s' % (msg.topic, msg.payload))
   msg_out = {}
   msg_out['msg_topic'] = str(msg.topic)
   msg_out['msg_payload'] = str(msg.payload)
   print(json.dumps(repr(msg_out)))
   results_file.write(json.dumps(msg_out)+"\n")
   results_file.flush()
   
   

if __name__ == '__main__':
   signal(SIGINT, handler)
  
   client = mqtt.Client(client_id = "MqttClient")
   client.on_connect = on_connect
   client.on_message = on_message
   client.connect('ipaddress', 1883, 60)
 
   
   client.loop_forever()
