import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    global cw, notl
    if (msg.topic == "/detect/cw"):
        cw = int(msg.payload.decode('utf-8'))
    if (msg.topic == "/nodetect/tl"):
        notl = int(msg.payload.decode('utf-8'))

    print(msg.topic+" " +str(msg.payload))


global cw
cw = 0
notl = 0
client = mqtt.Client()
client.on_message = on_message

client.connect("163.180.117.43")
client.subscribe("/detect/cw",0)

while (client.loop()==0):
    if(cw==1):
        cw = 0
        break

print("subscribed cw")

client.subscribe("/nodetect/tl",0)

while (client.loop()==0):
    if(notl==1):
        notl = 0
        break

print("subscribed notl")
