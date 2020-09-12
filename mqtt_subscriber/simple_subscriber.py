import paho.mqtt.client as mqtt

topic1 = "mqtt/switch/testdevice/example_binary_sensor/command"
topic2 = "mqtt/switch/testdevice/example_binary_sensor/state"
# topic = "lock/LWT"
# topic = "smartlock/status"
user = "test1"
pw = "oVTo~7?km1yv"
host = "45.143.137.138"
port = 1883


def on_connect(client, userdata, flags, rc):
    global subscriber
    print('connected...rc=' + str(rc))
    subscriber.subscribe(topic1)
    subscriber.subscribe(topic2)


def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))


def on_message(mqttc, userdata, msg):
    print('message received...')
    print('topic: ' + msg.topic + ', qos: ' + str(msg.qos) + ', message: ' + str(msg.payload))


def on_subscribe(mqttc, userdata, mid, granted_qos):
    print('subscribed (qos=' + str(granted_qos) + ')')


def on_unsubscribe(mqttc, userdata, mid, granted_qos):
    print('unsubscribed (qos=' + str(granted_qos) + ')')


subscriber = mqtt.Client()
subscriber.on_connect = on_connect
subscriber.on_disconnect = on_disconnect
subscriber.on_message = on_message
subscriber.on_subscribe = on_subscribe
subscriber.on_unsubscribe = on_unsubscribe
subscriber.username_pw_set(user, pw)
subscriber.connect(host, port)
subscriber.loop_forever()
