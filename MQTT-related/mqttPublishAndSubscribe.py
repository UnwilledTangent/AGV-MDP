import paho.mqtt.client as mqtt
import time


def on_message(client, userdat, message):
    print("message received " + "\"" + str(message.payload.decode("utf-8")) + "\"")
    print("message topic = " + message.topic)
    print("message qos = " + str(message.qos))
    print("message retain flag = " + str(message.retain))


# broker_address = "192.168.100.100"
broker_address = "iot.eclipse.org"  # use external broker
print("creating new instance")
client = mqtt.Client("P1")  # create new instance
client.on_message = on_message  # attach function to callback
print("connecting to broker")
client.connect(broker_address)  # connect to broker
client.loop_start()  # start the loop
print("Subscribing to topic " + "house/bulbs/bulb1")
client.subscribe("house/bulbs/bulb1")
print("Publishing message to topic " + "house/bulbs/bulb1")
client.publish("house/bulbs/bulb1", "OFF")  # publish
time.sleep(2)  # wait
client.loop_stop()  # stop the loop
