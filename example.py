#!/usr/bin/env python3

# Minimal example without graphs and other stuff
import time

import dds8558

PS_Spodaj = dds8558.DDS8558_Modbus(modbus_address=1)

try:
    while True:
        print(PS_Spodaj.read_active_power(), 'kW\n',
              PS_Spodaj.read_voltage(), 'V \n',
              PS_Spodaj.read_current(), ' A\n',
              PS_Spodaj.read_frequency(), ' Hz\n',
              PS_Spodaj.read_total_active_energy(), ' kWh\n',
              PS_Spodaj.read_total_reactive_energy(), ' kVAr\n',
              'cos(fi)=',PS_Spodaj.read_power_factor()
              )
        time.sleep(1) #sleep for 1 second and then read data again

except KeyboardInterrupt:
    pass
