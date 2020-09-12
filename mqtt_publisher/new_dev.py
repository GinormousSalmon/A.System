from paho.mqtt import publish


msg = '{"name":"kok","state_topic":"smartkok/switch/kok/state","command_topic":"smartkok/switch/kok/command",' \
        '"availability_topic":"smartkok/LWT","payload_available":"Online","payload_not_available":"Offline",' \
        '"unique_id":"ESPswitchkok","device":{"identifiers":"2cf5231d1bee","name":"smartkok","sw_version":"esphome ' \
        'v1.14.5 Sep  9 2020, 14:56:40","model":"PLATFORMIO_D1_MINI","manufacturer":"espressif"}} '
topic = 'homeassistant/switch/smartkok/kok/config'
auth = {'username': "test1", 'password': "oVTo~7?km1yv"}

publish.single(topic, msg, qos=2, hostname='45.143.137.138', auth=auth, retain=True)
