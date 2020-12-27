from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import logging
# initialize a serial RTU client instance
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian



class DDS8558_Modbus_pymodbus:
    """Simple method for reading DDS8558 over serial Modbus interface"""
    def __init__(self, serial_device='/dev/ttyUSB0', modbus_address=0x001, baudrate=9600, debug=False):
        self.voltage = 0x0000
        self.current = 0x0008
        self.activePower = 0x0012
        self.reactivePower = 0x001A # TODO: figure out why I can't read reactive power
        self.PowerFactor = 0x002A
        self.Frequency = 0x0036
        self.totalActiveEnergy = 0x0100
        self.totalReactiveEnergy = 0x0400 # TODO: again, no reactive energy
        self.modbus_address = modbus_address
        self.client = ModbusClient(method='rtu', port=serial_device, baudrate=baudrate, retries=1000, timeout=0.1,
                                   parity='E', stopbits=1)
        self.client.connect()

        if debug:
            logging.basicConfig()
            log = logging.getLogger()
            log.setLevel(logging.DEBUG)

    def read_voltage(self):
        """Read voltages from meter"""
        result = self.client.read_input_registers(address=self.voltage, count=2, unit=self.modbus_address)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
        value = decoder.decode_32bit_float()
        return value

    def read_current(self):
        """Read smart meter current"""
        result = self.client.read_input_registers(address=self.current, count=2, unit=self.modbus_address)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
        value = decoder.decode_32bit_float()
        return value

    def read_reactive_power(self):
        """Data register Address"""
        result = self.client.read_input_registers(address=self.reactivePower, count=2, unit=self.modbus_address)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
        value = decoder.decode_32bit_float()
        return value

    def read_active_power(self):
        result = self.client.read_input_registers(address=self.activePower, count=2, unit=self.modbus_address)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
        value = decoder.decode_32bit_float()
        return value

    def read_power_factor(self):
        result = self.client.read_input_registers(address=self.PowerFactor, count=2, unit=self.modbus_address)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
        value = decoder.decode_32bit_float()
        return value

    def read_total_active_energy(self):
        """Read total active energy"""
        result = self.client.read_input_registers(address=self.totalActiveEnergy, count=2, unit=self.modbus_address)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
        value = decoder.decode_32bit_float()
        return value

    def read_total_reactive_energy(self):
        """Read total active energy"""
        result = self.client.read_input_registers(address=self.totalReactiveEnergy, count=2, unit=self.modbus_address)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
        value = decoder.decode_32bit_float()
        return value

    def read_frequency(self):
        """Read system frequency (not sure why would you need that though) """
        result = self.client.read_input_registers(address=self.Frequency, count=2, unit=self.modbus_address)
        decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
        value = decoder.decode_32bit_float()
        return value
