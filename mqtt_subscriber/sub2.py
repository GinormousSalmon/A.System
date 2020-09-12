import paho.mqtt.client as mqtt
from paho.mqtt import publish

topic = "smartlock/switch/en/command"
# topic = "lock/debug/uid"
# topic = "smartlock/status"
user = "test1"
pw = "oVTo~7?km1yv"
host = "45.143.137.138"
port = 1883


def on_connect(client, userdata, flags, rc):
    global subscriber
    print('connected...rc=' + str(rc))
    subscriber.subscribe(topic)


def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))


def on_message(mqttc, userdata, msg):
    print('message received...')
    print('topic: ' + msg.topic + ', qos: ' + str(msg.qos) + ', message: ' + str(msg.payload))
    if msg.payload == bytes(b'OFF'):
        publish.single('smartlock/switch/en/state', "OFF", hostname=host, auth={'username': user, 'password': pw})
        print("off")
    elif msg.payload == bytes(b'ON'):
        publish.single('smartlock/switch/en/state', "ON", hostname=host, auth={'username': user, 'password': pw})
        print("on")


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
