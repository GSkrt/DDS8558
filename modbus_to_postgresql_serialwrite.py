#!/usr/bin/env python3

# Make this run as a service on raspberry pi... (check systemctl functionality if running Linux OS)
# this script writes time series into database in more natural way (t, txt_string, value) that is more
# common due to simplicity of managing multiple time series in a single table.

#  since we are acquiring time from systime and there is low baudrate it happens to be a bit more accurate in
# terms of sample time accuracy.

# this script is made for linux, you can start process using systemd library - you can't find it on windows machine
# (find online how to write a service from python script)

from systemd import journal
import psycopg2
import time
from datetime import datetime
import DDS8558_pymodbus

mb_address = 0x01
PS_Spodaj = DDS8558_pymodbus.DDS8558_Modbus_pymodbus(serial_device='/dev/ttyUSB0', modbus_address=mb_address,
                                                     baudrate=9600)

try:
    # Connect to an existing database (or install a new one)
    connection = psycopg2.connect(user="postgres", #postgresql user with write, create database, insert
                                  password="your postgresql password",
                                  host="127.0.0.1",  # address of the local pg_database
                                  port="5432", # port of your database server
                                  database="postgres") # database
    cursor = connection.cursor()
except Exception as error:

    journal.write("Oops! An exception has occured:", error)
    journal.write("Exception TYPE:", type(error))

# paralel data insert version

# make sure you choose right database schema and table  to write to !!
create_table_sql = """create table if not exists public.measurements_serial
(t timestamp,
txtid text,
value float
)"""

sql_insert = """
INSERT INTO public.measurements_serial
(t, txtid, value)
VALUES(%s, %s , %s);
"""

cursor.execute(create_table_sql)

try:
    while True:
        # get ative power
        power = PS_Spodaj.read_active_power()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + ' power_W', power))

        # get reactive power
        power = PS_Spodaj.read_reactive_power()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + ' power_reactive_VAr', power))

        # we read time again to make it a bit more accurate tho, system time is a bad way to get a
        # timing for measurements...
        v = PS_Spodaj.read_voltage()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + ' voltage_V', v))
        # current
        current = PS_Spodaj.read_current()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + ' current_A', current))
        # frequency
        frequency = PS_Spodaj.read_frequency()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + ' frequency_Hz', frequency))
        # energy
        energy = PS_Spodaj.read_total_active_energy()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + ' energy_kWh', energy))
        # reactive_energy
        reactive_energy = PS_Spodaj.read_total_reactive_energy()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + ' reactive_energy_kVAr', reactive_energy))
        # power factor
        cosfi = PS_Spodaj.read_power_factor()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + ' cosfi', cosfi))

        # commit transactions to database and then sleep
        connection.commit()
        time.sleep(1)  # sleep for 1 second

        # use line below only for debugging reasons
        # print(v, ' V\n')


except KeyboardInterrupt:
    # close the connection (good for testing...) 
    if connection:
        cursor.close()
        connection.close()
        journal.write("PostgreSQL connection is closed")
