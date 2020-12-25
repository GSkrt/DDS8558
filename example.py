#!/usr/bin/env python3

# Minimal example without graphs and other stuff
import time
from datetime import datetime
# import dds8558
import DDS8558_pymodbus

PS_Spodaj = DDS8558_pymodbus.DDS8558_Modbus_pymodbus(serial_device='/dev/ttyUSB0', modbus_address=0x01, baudrate=9600)

PS_Spodaj.read_frequency()

try:
    while True:
        print(datetime.now(),' ', PS_Spodaj.read_active_power(), 'kW ',
              PS_Spodaj.read_voltage(), 'V ',
              PS_Spodaj.read_current(), ' A ',
              PS_Spodaj.read_frequency(), ' Hz ',
              PS_Spodaj.read_total_active_energy(), ' kWh ',
              PS_Spodaj.read_total_reactive_energy(), ' kVAr ',
              'cos(fi)=', PS_Spodaj.read_power_factor()
              )
        time.sleep(0.1)  # sleep for 1 second and then read data again

except KeyboardInterrupt:
    pass
