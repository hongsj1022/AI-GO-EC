import paho.mqtt.publish as publish

MQTT_HOST = "163.180.117.43"

publish.single(topic="/detect/tl", payload="go", hostname=MQTT_HOST)

