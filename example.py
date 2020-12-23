#!/usr/bin/env python3

# Minimal example without graphs and other stuff
import time
# import dds8558
import DDS8558_pymodbus

PS_Spodaj = DDS8558_pymodbus.DDS8558_Modbus_pymodbus(serial_device='/dev/ttyUSB0', modbus_address=0x01, baudrate=9600)

PS_Spodaj.read_frequency()

try:
    while True:
        print(PS_Spodaj.read_active_power(), 'kW\n',
              PS_Spodaj.read_voltage(), 'V \n',
              PS_Spodaj.read_current(), ' A\n',
              PS_Spodaj.read_frequency(), ' Hz\n',
              PS_Spodaj.read_total_active_energy(), ' kWh\n',
              PS_Spodaj.read_total_reactive_energy(), ' kVAr\n',
              'cos(fi)=', PS_Spodaj.read_power_factor()
              )
        time.sleep(0.1)  # sleep for 1 second and then read data again

except KeyboardInterrupt:
    pass
