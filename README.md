# DDS8558 smart meter Python module


Simple module for reading Modbus data from DDS8558 smart meters. 

I've provided minimal example for testing.

install minimalmodbus and serial library using pip. 

If you have problems with reading you might try to change self.instrument.serial.timeout = 0.1 to something bigger. 

There is a method to reset meter energy readings, I didn't have time to test that yet.

