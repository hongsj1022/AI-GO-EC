import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/detect/tl")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global cw, notl, tts
    if (msg.topic == "/detect/tl"):
        tl = int(msg.payload.decode('utf-8'))
    if (msg.topic == "/detect/cw"):
        cw = int(msg.payload.decode('utf-8'))
    if (msg.topic == "/detect/notl"):
        notl = int(msg.payload.decode('utf-8'))
    if (msg.topic == "/endinform/tts"):
        tts = int(msg.payload.decode('utf-8'))

    print(msg.topic+" " +str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("163.180.117.43")
client.subscribe("/detect/tl")
client.subscribe("/detect/notl")
client.subscribe("/detect/nocar")
client.subscribe("/detect/cw")
client.subscribe("/endinform/tts")
client.subscribe("/detect/yestl")
client.loop_forever()
