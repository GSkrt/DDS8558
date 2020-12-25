#!/usr/bin/env python3

# Make this run as a service on raspberry pi... (check systemctl functionality if running Linux OS)

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
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

create_table_sql = """create table if not exists public.meritve_stevec
(t timestamp,
ident text,
voltage float,
current float,
frequency float,
energy float,
reactive_energy float,
cosfi float )"""

sql_insert = """
INSERT INTO public.meritve_stevec
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
        print("PostgreSQL connection is closed")