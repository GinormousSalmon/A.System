from sensor import Sensor
import hashlib

s = Sensor('test_client', 'device1', 'bin_sensor1', 'switch')
s1 = s.get_hass_sensor()
s2 = s.get_dev_sensor()
print()
print(s1)
print("\n")
print(s2)
