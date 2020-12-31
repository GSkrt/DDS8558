#!/usr/bin/env python3

# Minimal example without graphs, database capture and other stuff...

import time
from datetime import datetime
# import dds8558
import DDS8558_pymodbus

SmartMeter = DDS8558_pymodbus.DDS8558_Modbus_pymodbus(serial_device='/dev/ttyUSB0', modbus_address=0x01, baudrate=9600)

SmartMeter.read_frequency()

try:
    while True:
        print(datetime.now(),' ', SmartMeter.read_active_power(), 'kW ',
              SmartMeter.read_voltage(), 'V ',
              SmartMeter.read_current(), ' A ',
              SmartMeter.read_frequency(), ' Hz ',
              SmartMeter.read_total_active_energy(), ' kWh ',
              'cos(fi)=', SmartMeter.read_power_factor()
              )
        time.sleep(0.1)  # sleep for 1 second and then read data again

except KeyboardInterrupt:
    pass
