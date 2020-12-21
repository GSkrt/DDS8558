# DDS8558 smart meter Python Modbus RS485 module


Simple module for Modbus data connection to DDS8558 smart meters. 

I'm sharing this module since it's not easy to get all the parameters for this smart meter. I've provided minimal example for testing.

To use this module you need to  install **minimalmodbus** and **serial** library using pip.  
I will make a package when I get some time to do that. I didn't go trough packaging and pip yet since this is a simple module just holding modbus configuration information. 

If you have problems with reading data from modbus you might try to change self.instrument.serial.timeout = 0.1 to something bigger or playing with  baud speeds. 
Check example file for more explanation.

There is a method to reset meter energy readings, I didn't have time to test that yet.

