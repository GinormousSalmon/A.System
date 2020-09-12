import paho.mqtt.client as mqtt
from paho.mqtt import publish
from sensor import Sensor

user = "test1"
password = "oVTo~7?km1yv"
# auth = {'username': user, 'password': password}
host = "45.143.137.138"
port = 1883

payload_available = "Online"
payload_not_available = "Offline"

device_topics = ['mqtt/test_client/room1/device1/bin_sensor1/command',
                 'mqtt/test_client/room1/device1/bin_sensor1/state',
                 'mqtt/test_client/room1/device1/LWT']
hass_topics = []

# client, device name, sensor name, sensor type
sensors = [Sensor('test_client', 'device1', 'bin_sensor1', 'switch')]


def calc_topic(topic: str):
    if topic[:17].__eq__('mqtt/ytd61h9zk4jb'):
        return 'homeassistant' + topic[17:]
    elif topic[:13].__eq__('homeassistant'):
        return 'mqtt/ytd61h9zk4jb' + topic[13:]
    else:
        print('invalid topic??')
        return "error/"


# subscriber -----------------------------------------

def on_connect(client, userdata, flags, rc):
    global subscriber
    print('connected...rc=' + str(rc))
    # virtual devices initialization
    for sensor in sensors:
        s = sensor.get_hass_sensor()
        config = '{"name":"' + s.sensor + \
                 '","state_topic":"' + s.state_topic + \
                 '","command_topic":"' + s.command_topic + \
                 '","availability_topic":"' + s.availability_topic + \
                 '","payload_available":"' + payload_available + \
                 '","payload_not_available":"' + payload_not_available + \
                 '","unique_id":"' + s.unique_id + \
                 '","device":{"identifiers":"' + s.identifier + \
                 '","name":"' + s.device + \
                 '","sw_version":"esphome v1.14.5 Sep  9 2020, 14:56:40",' \
                 '"model":"PLATFORMIO_D1_MINI","manufacturer":"espressif"}} '
        subscriber.publish(s.config_topic, payload=config, qos=1, retain=True)
        subscriber.publish(s.availability_topic, payload="Online", qos=1, retain=True)

    for sensor in sensors:
        sh = sensor.get_hass_sensor()
        sd = sensor.get_dev_sensor()

        # subscriber.subscribe(sh.availability_topic)
        # subscriber.subscribe(sh.state_topic)
        subscriber.subscribe(sh.command_topic)

        subscriber.subscribe(sd.availability_topic)
        subscriber.subscribe(sd.state_topic)
        # subscriber.subscribe(sd.command_topic)


def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))


def on_message(mqttc, userdata, msg):
    print('topic: ' + msg.topic + ', qos: ' + str(msg.qos) + ', message: ' + str(msg.payload))
    subscriber.publish(calc_topic(msg.topic), payload=msg.payload, qos=1, retain=True)

    # if msg.payload == bytes(b'OFF'):
    #     publish.single('smartlock/switch/en/state', "OFF", hostname=host, auth={'username': user, 'password': pw})
    #     print("off")
    # elif msg.payload == bytes(b'ON'):
    #     publish.single('smartlock/switch/en/state', "ON", hostname=host, auth={'username': user, 'password': pw})
    #     print("on")


def on_subscribe(mqttc, userdata, mid, granted_qos):
    print('subscribed (qos=' + str(granted_qos) + ')')


def on_unsubscribe(mqttc, userdata, mid, granted_qos):
    print('unsubscribed (qos=' + str(granted_qos) + ')')


# subscriber -----------------------------------------


subscriber = mqtt.Client()
subscriber.on_connect = on_connect
subscriber.on_disconnect = on_disconnect
subscriber.on_message = on_message
subscriber.on_subscribe = on_subscribe
subscriber.on_unsubscribe = on_unsubscribe
subscriber.username_pw_set(user, password)
subscriber.connect(host, port)
subscriber.loop_forever()
