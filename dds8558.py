import minimalmodbus
import serial

class DDS8558_Modbus():
    """Functions impmented from document SINGLE-PHASE TWO-WIRE DIN-RAIL ENERGY METER"""

    def __init__(self, serial_device='/dev/ttyUSB0',modbus_address=125, baudrate=9600, debug=False):
        self.instrument = minimalmodbus.Instrument(serial_device, modbus_address, minimalmodbus.MODE_RTU)
        self.instrument.serial.baudrate = baudrate
        self.instrument.serial.parity = serial.PARITY_EVEN
        self.instrument.close_port_after_each_call = True
        self.instrument.serial.bytesize = 8
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout = 0.1
        self.instrument.debug = debug
        self.instrument.clear_buffers_before_each_transaction = True

        #actutal adresses of the individual registers
        self.Voltage = "0x0000"
        self.Current = "0x0008"


    def read_voltage(self):
        "Data register Address in hex is below in hex"

        value = self.instrument.read_float(int(self.Voltage, 0), functioncode=4, number_of_registers=2, byteorder=0)
        return value

    def read_current(self):
        "Data register Address"

        value = self.instrument.read_float(int(self.Current, 0), functioncode=4, number_of_registers=2, byteorder=0)
        return value

    def read_reactive_power(self):
        "Data register Address"
        Current = "0x0008"
        value = self.instrument.read_float(int(Current, 0), functioncode=4, number_of_registers=2, byteorder=0)
        return value

    def read_active_power(self):
        ActivePower = "0x0012"
        value = self.instrument.read_float(int(ActivePower, 0), functioncode=4, number_of_registers=2, byteorder=0)
        return value

    def read_power_factor(self):
        PowerFactor = "0x002A"
        value = self.instrument.read_float(int(PowerFactor, 0), functioncode=4, number_of_registers=2, byteorder=0)
        return value

    def read_total_active_energy(self):
        TotalActiveEnergy = "0x0100"
        value = self.instrument.read_float(int(TotalActiveEnergy, 0), functioncode=4, number_of_registers=2,
                                           byteorder=0)
        return value

    def read_total_reactive_energy(self):
        TotalReactiveEnergy = "0x0400"
        value = self.instrument.read_float(int(TotalReactiveEnergy, 0), functioncode=4, number_of_registers=2,
                                           byteorder=0)
        return value

    def read_frequency(self):
        Frequency = "0x0036"
        value = self.instrument.read_float(int(Frequency, 0), functioncode=4, number_of_registers=2, byteorder=0)
        return value

    def reset_energy_values(self):
        #didnt test it yet..usefull for resseting values now and then...
        TotalActiveEnergy = "0x0100"
        TotalReactiveEnergy = "0x0400"
        self.instrument.write_float(int(TotalActiveEnergy, 0), 0, number_of_registers=2, byteorder=0)
        self.instrument.write_float(int(TotalReactiveEnergy, 0), 0, number_of_registers=2, byteorder=0)