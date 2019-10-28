import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

idx = 0

while True:
    print("send success")
    publish.single("paho",
                   payload="this is message:%s" % idx,
                   hostname="iot.eclipse.org",
                   client_id="lora1",
                   qos = 0,
                   port=1883,
                   protocol=mqtt.MQTTv311)
    idx += 1