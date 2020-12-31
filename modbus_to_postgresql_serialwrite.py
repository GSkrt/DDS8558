#!/usr/bin/env python3

# Make this run as a service on raspberry pi... (check systemctl functionality if running Linux OS)
# this script writes time series into database in so coled LONG FORMAT for time series
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
SmartMeter = DDS8558_pymodbus.DDS8558_Modbus_pymodbus(serial_device='/dev/ttyUSB0', modbus_address=mb_address,
                                                      baudrate=9600)

try:
    # Connect to an existing database (or install a new one)
    connection = psycopg2.connect(user="postgres",  # postgresql user with write, create database, insert
                                  password="your postgresql password",
                                  host="127.0.0.1",  # address of the local pg_database (currently localhost)
                                  port="5432",  # port of your database server
                                  database="postgres")  # database
    cursor = connection.cursor()
except Exception as error:

    journal.write("Oops! An exception has occured:", error)
    journal.write("Exception TYPE:", type(error))


# make sure you choose right database schema and table  to write and rewrite queries below !!

create_table_sql = """create table if not exists public.measurements_serial
(t timestamp,
txtid text,
value float
)"""

create_materialized_view_energy_monthly = """
create materialized view if not exists public.monthly_energy as 
select month_date , max(value)- min(value) as w_month_kwh
from 
(
select
	date(date_trunc('month',t)) as month_date,
	value
from
	public.measurements_serial ms
where
	txtid like '%energy_kWh%'
)t
group by 
month_date"""


create_materialized_view_energy_daily = """
create materialized view if not exists public.daily_energy as 
select day , max(value)- min(value) as w_day_kwh
from 
(
select
	date(t) as day,
	--txtid,
	value
from
	public.measurements_serial ms
where
	txtid like '%energy_kWh%'
)t
group by 
day
"""

create_materialized_view_energy_hourly = """
create materialized view if not exists public.hourly_energy as 
select datetime_hour , max(value)- min(value) as w_hour_kwh
from 
(
select
	date_trunc('hour',t) as datetime_hour,
	--txtid,
	value
from
	public.measurements_serial ms
where
	txtid like '%energy_kWh%'
)t
group by 
datetime_hour
"""

create_materialized_view_energy_15_min = """
create materialized view if not exists public.fifteenm_energy as 
select
	tabela.datetime_hour,
	max(tabela.value)-min(tabela.value) as W_15min 
from
	(
	select
		--t,
		date_trunc('hour', t) + date_part('minute', t)::int / 15 * interval '15 min' as datetime_hour,
		value
	from
		public.measurements_serial ms
	where
		txtid like '%energy_kWh%'
	 ) as tabela
group by
	tabela.datetime_hour
"""


sql_insert = """
INSERT INTO public.measurements_serial
(t, txtid, value)
VALUES(%s, %s , %s);
"""

# make aggregation materialized views if you need them for monitoring consumption
# comment out lines below if you don't want this materialized views in the database

cursor.execute(create_table_sql)
cursor.execute(create_materialized_view_energy_monthly)
cursor.execute(create_materialized_view_energy_daily)
cursor.execute(create_materialized_view_energy_15_min)


try:
    while True:
        # get ative power
        power = SmartMeter.read_active_power()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + ' power_W', power))

        # get reactive power
        power = SmartMeter.read_reactive_power()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + '_power_reactive_VAr', power))

        # we read time again to make it a bit more accurate tho, system time is a bad way to get a
        # timing for measurements...
        v = SmartMeter.read_voltage()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + '_voltage_V', v))
        # current
        current = SmartMeter.read_current()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + '_current_A', current))
        # frequency
        frequency = SmartMeter.read_frequency()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + '_frequency_Hz', frequency))
        # energy
        energy = SmartMeter.read_total_active_energy()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + '_energy_kWh', energy))
        # reactive_energy
        reactive_energy = SmartMeter.read_total_reactive_energy()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + '_reactive_energy_kVAr', reactive_energy))
        # power factor
        cosfi = SmartMeter.read_power_factor()
        datetime_var = datetime.now()
        cursor.execute(sql_insert, (datetime_var, str(mb_address) + '_cosfi', cosfi))

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
