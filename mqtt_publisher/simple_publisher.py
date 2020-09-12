from paho.mqtt import publish
import random
import time

# msgs = [{'topic': "mqtt/random", 'payload': "hello"}]

topic = 'smartkok/LWT'
msg = "Online"

auth = {'username': "test1", 'password': "oVTo~7?km1yv"}

# while True:
#     mes = str(random.random())
#     publish.single(topic, mes, qos=2, hostname='45.143.137.138', auth=auth)
#     time.sleep(1)

publish.single(topic, msg, qos=2, hostname='45.143.137.138', auth=auth, retain=True)
# publish.multiple(msgs, hostname="45.143.137.138", auth=auth)
