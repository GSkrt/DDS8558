#!/usr/bin/env python3

# Make this run as a service on raspberry pi... (check systemctl functionality if running Linux OS)
# this version is for those who want to access database with typical t,valu,value, value,... visualisation app for example
# spreadsheets. If you have multiple measurements this format is not suitable for storing time series !!!

from systemd import journal
import psycopg2
import time
from datetime import datetime
# import dds8558
import DDS8558_pymodbus

PS_Spodaj = DDS8558_pymodbus.DDS8558_Modbus_pymodbus(serial_device='/dev/ttyUSB0', modbus_address=0x01, baudrate=9600)

PS_Spodaj.read_frequency()

try:
    # Connect to an existing database (or install a new one)
    connection = psycopg2.connect(user="postgres",
                                  password="your_pass",
                                  host="127.0.0.1", #address of the local pg_database
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()
except Exception as error:

    journal.write("Oops! An exception has occured:", error)
    journal.write("Exception TYPE:", type(error))

#paralel data insert version

create_table_sql = """create table if not exists public.mesurements_sm
(t timestamp,
ident text,
voltage float,
current float,
frequency float,
energy float,
reactive_energy float,
cosfi float )"""

sql_insert = """
INSERT INTO public.measurements_sm
(t, ident, voltage, current, frequency, energy, reactive_energy, cosfi)
VALUES(%s, %s , %s, %s, %s, %s, %s, %s);
"""

cursor.execute(create_table_sql)

try:
    while True:
        datum = datetime.now()
        moc = PS_Spodaj.read_active_power()
        v = PS_Spodaj.read_voltage()
        tok = PS_Spodaj.read_current()
        frekvenca = PS_Spodaj.read_frequency()
        energija = PS_Spodaj.read_total_active_energy()
        jalova_energija = PS_Spodaj.read_total_reactive_energy()
        cosfi = PS_Spodaj.read_power_factor()

        #dump data to postgresql database
        cursor.execute(sql_insert, (datum,'meritve 1', v, tok, frekvenca, energija, jalova_energija, cosfi))
        connection.commit()
        time.sleep(1)  # sleep for 1 second and then read data again


except KeyboardInterrupt:
    # close the connection...
    if connection:
        cursor.close()
        connection.close()
        journal.write("PostgreSQL connection is closed")
