# DDS8558 smart meter Python Modbus RS485 module and some simple code to make a modbus >>> postgresql service (examples) 


Simple module for Modbus data connection to DDS8558 smart meters. What you need is a serial RS485 interface. You can get "cheap" USB->RS485 dongles online. 
Just be carefull, cheap is sometimes too cheap. Some USB dongles can't provide voltage levels to pass voltage logical treshold
for RS485!

I've coded minimal example for testing. Check debug option if something doesn't work. 


To use this module you need to  install **minimalmodbus** if you want to use minimalmodbus version  and **serial** or **pymodbus**
library for pymodbus version using pip.

There are two different services: 
- parralel write (Wide format)
- serial write (Long format)


Parralel: 
*[time, value, value, value,..]*

The serial format is more common way of storing time series even though it's a bit more difficult to transpose values directly in database tables. 

Serial: 
*[time, text_id, value]*

I didn't go trough packaging and pip yet. Main idea was just to share modbus addres settings. 
If you came here you probably know what you are doing. 

If you have problems with reading data from modbus you might try to change self.instrument.serial.timeout = 0.1 to something bigger or playing with  baud speeds. 
Check example file for more explanation, in general I recommend using pymodbus module.

There is also example of modbus->postgresql python module that I run on raspberry pi as a service to capture data.

If you have some interesting Modbus devices lying around and want to have some python code around them contact me.




