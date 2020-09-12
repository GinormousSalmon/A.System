import paho.mqtt.client as mqtt
from threading import Thread
from aiohttp import web
import socketio
import asyncio
import time
import nest_asyncio
nest_asyncio.apply()

# socket_io = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins=['http://45.143.137.138'])
socket_io = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')
app = web.Application()
socket_io.attach(app)


queue = []


@socket_io.on('connect')
async def connect_handler(sid, environ):
    print("new connection")  # works as expected
    await socket_io.emit('msg', "connected")  # works as expected


@socket_io.on("msg")
async def message(sid, data):
    global queue
    print("new data: " + str(data))  # works as expected
    await socket_io.emit('msg', "response")  # works as expected
    for i in range(5):
        if len(queue) > 0:
            asyncio.get_event_loop().run_until_complete(socket_io.emit('msg', "got: " + queue.pop()))
            # asyncio.run(socket_io.emit('msg', "got: " + queue.pop()))


@socket_io.on("gimme")
def message(sid, data):
    global queue
    print("new data")  # works as expected
    if len(queue) > 0:
        asyncio.run(socket_io.emit('msg', "got: " + queue.pop()))


topic = "mqtt/esp/test"
user = "test1"
pw = "oVTo~7?km1yv"
host = "localhost"
# host = "45.143.137.138"
port = 1883


async def send():
    while True:
        await socket_io.emit('msg', "kok")
        time.sleep(0.5)


def start_send():
    asyncio.run(send())


def on_connect(client, userdata, flags, rc):
    global subscriber
    print('connected...rc=' + str(rc))
    subscriber.subscribe(topic)


def on_disconnect(mqttc, userdata, rc):
    print('disconnected...rc=' + str(rc))


def on_message(mqttc, userdata, msg):
    global queue
    print('message received...', end=" ")
    print('topic: ' + msg.topic + ', qos: ' + str(msg.qos) + ', message: ' + str(msg.payload))
    queue.append(str(msg.payload))
    if len(queue) > 3:
        queue.pop()

    # asyncio.get_event_loop().run_until_complete(socket_io.emit('msg', "got: " + str(msg.payload)))
    # asyncio.run(send(str(msg.payload)))
    # asyncio.run(socket_io.emit('msg', "got: " + str(msg.payload)))
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(socket_io.emit('msg', "got: " + str(msg.payload)))


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

    # asyncio.run(send())
    # send_thread = Thread(target=start_send)
    # send_thread.daemon = True
    # send_thread.start()
    web.run_app(app, host='45.143.137.138', port=5000)
    # web.run_app(app, host='localhost', port=5000)
    # eventlet.wsgi.server(eventlet.listen(('45.143.137.138', 5000)), app)
    # eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
    # uvicorn.run(app, host="45.143.137.138", port=5000)
    # uvicorn.run(app, host="localhost", port=5000)
