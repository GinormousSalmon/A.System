import socketio
import eventlet
import paho.mqtt.client as mqtt
from threading import Thread

sio = socketio.Server(cors_allowed_origins=['http://45.143.137.138'])
app = socketio.WSGIApp(sio)
sid_target = None


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)


@sio.on('msg')
def message(sid, data):
    global sid_target
    print('message ', data)
    sio.emit('msg', "got: " + str(sid), sid)
    sid_target = sid
    # await sio.emit('msg', "ur gayyy")


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


topic = "mqtt/esp/test"
user = "test1"
pw = "oVTo~7?km1yv"
host = "localhost"
# host = "45.143.137.138"
port = 1883


def on_connect(client, userdata, flags, rc):
    global subscriber
    print('connected...rc=' + str(rc))
    subscriber.subscribe(topic)


def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))


def on_message(mqttc, userdata, msg):
    global sid_target
    print('message received...', end=" ")
    print('topic: ' + msg.topic + ', qos: ' + str(msg.qos) + ', message: ' + str(msg.payload))
    if sid_target is not None:
        sio.emit('msg', "got: " + str(msg.payload), sid_target)


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


def start_sub():
    global subscriber
    subscriber.loop_forever()


if __name__ == '__main__':
    sub_thread = Thread(target=start_sub)
    sub_thread.daemon = True
    sub_thread.start()
    eventlet.wsgi.server(eventlet.listen(('45.143.137.138', 5000)), app)
    # eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
    # uvicorn.run(app, host="45.143.137.138", port=5000)
    # uvicorn.run(app, host="localhost", port=5000)
