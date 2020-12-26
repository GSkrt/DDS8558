# DDS8558 smart meter Python Modbus RS485 module and some simple code to make a modbus->postgresql service (examples) 


Simple module for Modbus data connection to DDS8558 smart meters. What you need is a serial RS485 interface. You can get "cheap" USB->RS485 dongles online. 
Just be carefull, cheap is sometimes too cheap. Some USB dongles can't provide voltage levels to pass voltage logical treshold
for RS485! 

I've provided minimal example for testing meter pulling. Check debug option if something doesn't work. 


To use this module you need to  install **minimalmodbus** if you want to use minimalmodbus version  and **serial** or **pymodbus** 
library for pymodbus version using pip.

I didn't go trough packaging and pip yet since this is a simple module just holding modbus configuration information.
If you came here you probably know what you are doing. 

If you have problems with reading data from modbus you might try to change self.instrument.serial.timeout = 0.1 to something bigger or playing with  baud speeds. 
Check example file for more explanation, in general I recommend using pymodbus module.

There is also example of modbus->postgresql python module that I run on raspberry pi as a service.




