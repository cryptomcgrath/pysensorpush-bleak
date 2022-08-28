import sensor
import utils as ut
import numpy
import sensorpush
from datetime import datetime


epoch = datetime.utcfromtimestamp(0)

def unix_time_seconds(dt):
    return int((dt - epoch).total_seconds())

# either supply the mac addr of your sensor 
# as a parameter to connect here 
# or
# change the value of DEFAULT_SENSOR_ADDR in sensor.py
#
sensor.connect()

v,t = sensor.read_batt_info()
print("Battery info: volts={:>6.2f} raw temp={:>6.2f}".format(v,t))

rev_code_str = sensor.read_revision_code()
print("Revision code: {}".format(rev_code_str))

dev_id_int = sensor.read_device_id()
print("Device id: {}".format(dev_id_int))

samp_intv_secs = sensor.read_sample_interval()
print("Sample interval: {}".format(samp_intv_secs))

last_time = sensor.read_timestamp()
print("Last timestamp: {}".format(ut.intToTimeStr(last_time)))

#
# this is our callback function which we pass as a paramter to read_bulk_values
#
def read_bulk_values_callback(sample_time, samples, rawbytes):
  degree_sign = u"\N{DEGREE SIGN}"
  stamp=ut.intToTimeStr(sample_time)

  for j in range(0,len(samples)):
    s=""
    if j==0:
      s = stamp
    sample_hex = samples[j][0:8]
    if sample_hex == sensor.STOP_TOKEN:
        print("stop token")
        break
    sample_bytes = ut.hexStrToBytes(sample_hex)
    ## add dummy byte to beginning
    sample_bytes = bytearray([65])+sample_bytes
    vals = sensorpush.decode_values(sample_bytes, 65)
    temp_c = vals["temperature"]
    temp_f = ut.celsiusToFahrenheit(temp_c)
    hum = vals["humidity"]
    print("{:>20},{},temp: {:>7.3f}{}f ({:>7.3f}{}c) hum: {:>7.3f}%".format(s, samples[j], temp_f, degree_sign, temp_c, degree_sign, hum))


# we will be using a start time of 30 minutes prior to the last_time
current_time = unix_time_seconds(datetime.now())
print("current time {}".format(current_time))
print("last time {}".format(last_time))
exit
read_start_time_hex = ut.intToHexStr(last_time-120)

#
# here we read bulk values using the callback function above
#
sensor.read_bulk_values(read_start_time_hex, read_bulk_values_callback) 

