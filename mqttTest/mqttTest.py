
import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    f = open('record.txt', 'a')
    f.write(time.strftime('%Y-%m-%d %H:%M:%S') + " Connected with result code "+str(rc) + '\n')
    f.close()
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    f = open('record.txt', 'a')
    f.write(time.strftime('%Y-%m-%d %H:%M:%S') + ' ' + msg.topic+" " + msg.payload.decode('utf-8') + '\n')
    f.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set('smartcar', 'smartcar')
client.connect("mqtt.gycis.me", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()