import hashlib


class Sensor:
    client = None
    device = None
    sensor = None
    s_type = None
    state_topic = None
    command_topic = None
    availability_topic = None
    unique_id = None
    identifier = None
    id_calc = False
    config_topic = None

    def __init__(self, client: str, device: str, sensor: str, s_type: str, pref=''):
        self.client = client
        self.device = device
        self.sensor = sensor
        self.s_type = s_type
        prefix = pref + '/' + client + '/' + device + '/'
        self.state_topic = prefix + s_type + '/' + sensor + '/state'
        self.command_topic = prefix + s_type + '/' + sensor + '/command'
        self.availability_topic = prefix + 'LWT'
        self.unique_id = 'ESP' + client + device + s_type + sensor
        if not self.id_calc:
            self.identifier = hashlib.md5(bytes(client + device, 'utf-8')).hexdigest()[:12]
            self.id_calc = True
        self.config_topic = 'homeassistant/' + s_type + '/' + device + '/' + sensor + '/config'

    def get_hass_sensor(self):
        return Sensor(self.client, self.device, self.sensor, self.s_type, pref='homeassistant')

    def get_dev_sensor(self):
        return Sensor(self.client, self.device, self.sensor, self.s_type, pref='mqtt/ytd61h9zk4jb')

    def __str__(self):
        return "client: " + self.client + "; device: " + self.device + "; sensor: " + self.sensor + "; s_type: " + \
               self.s_type + ";\nstate_topic: " + self.state_topic + "\ncommand_topic: " + \
                self.command_topic + "\navailability_topic: " + self.availability_topic + "\nunique_id: " + \
                self.unique_id + "; identifier: " + self.identifier + ";\nconfig_topic: " + self.config_topic
