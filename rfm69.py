# RFM69.py
#
# Ported to Micropython by Arko at EMFCAMP 2016 - HABVILLE
#
# Prior Art:
# rfm69-python : Copyright (C) 2016 Russ Garrett
# ukhasnet-rfm69: Copyright (C) 2014 Phil Crump, James Coxon
#
# Based on RF22 Copyright (C) 2011 Mike McCauley ported to mbed by Karl Zweimueller
# Based on RFM69 LowPowerLabs (https://github.com/LowPowerLab/RFM69/)

import pyb
from pyb import Pin, ExtInt
from pyb import SPI

from time import sleep, time

from RFM69Dict import registers, config

class RFM69:
	def __init__(self, reset_pin=None, dio0_pin=None, spi_channel=None, config=None):
		self.reset_pin = reset_pin
		self.nss = Pin('X5', Pin.OUT_PP)
		self.reset = self.reset()
		self.spi_channel = spi_channel
		self.spi = SPI(1, SPI.MASTER, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB, crc=None)
		self.dio0_pin = 'X3'
		self.conf = self.configure()
		self.mode = self.set_mode()
		self.bufLen = 0
		self.buf = bytearray(registers["RFM69_MAX_MESSAGE_LEN"])
		self.version = self.getVersion()
		self.lastRssi = -(self.spi_read(registers["RFM69_REG_24_RSSI_VALUE"])/2)
		self.paLevel = 15

	def configure(self):
		print ("Configuring...")
		for reg, value in config.items():
			self.spi_write(registers.get(reg), value)
		return True

	def getVersion(self):
		self.version = self.spi_read(registers["RFM69_REG_10_VERSION"])
		return self.version

	def set_mode(self, newMode=registers["RFM69_MODE_SLEEP"]):
		self.spi_write(registers["RFM69_REG_01_OPMODE"], (self.spi_read(registers["RFM69_REG_01_OPMODE"]) & 0xE3) | newMode)
		self.mode = newMode
		return newMode

	def get_mode(self):
		return self.mode

	def init_gpio(self):
		self.dio0_pin = Pin('X3', Pin.IN, Pin.PULL_DOWN)

	def init_spi(self):
		self.spi = SPI(1, SPI.MASTER, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB, crc=None)

	def reset(self):
		""" Reset the module, then check it's working. """
		print ("Initialising RFM...")

		self.nss.high()

		self.reset_pin = Pin('X4', Pin.OUT_PP)
		self.reset_pin.low()                
		sleep(0.1)
		self.reset_pin.high()
		sleep(0.1) 
		self.reset_pin.low()                
		sleep(0.1)

	def checkRx(self):
		if (self.spi_read(registers["RFM69_REG_28_IRQ_FLAGS2"]) & registers["RF_IRQFLAGS2_PAYLOADREADY"]):
			bufLen = self.spi_read(registers["RFM69_REG_00_FIFO"])+1
			self.buf = self.spi_burst_read(registers["RFM69_REG_00_FIFO"], registers["RFM69_FIFO_SIZE"])
			self.lastRssi = -(self.spi_read(registers["RFM69_REG_24_RSSI_VALUE"])/2)
			self.clearFifo()

	def recv(self):
		return (self.buf, self.bufLen, self.lastRssi)

	def send(self, data, length, power):
		if (power<2 or power > 20):
			return False	#Dangerous power levels

		oldMode = self.mode

		# Copy into TX buffer
		self.buf = data
		self.bufLen = length

		# Start Transmitter
		self.set_mode(registers["RFM69_MODE_TX"])

		#Setup PA
		if (power <= 17):
			# Set PA Level
			self.paLevel = power + 14
			self.spi_write(registers["RFM69_REG_11_PA_LEVEL"], registers["RF_PALEVEL_PA0_OFF"] | registers["RF_PALEVEL_PA1_ON"] | registers["RF_PALEVEL_PA2_ON"] | self.paLevel )
		else:
			# Disable Over Current Protection
			self.spi_write(registers["RFM69_REG_13_OCP"], registers["RF_OCP_OFF"])
			# Enable High Power Registers
			self.spi_write(registers["RFM69_REG_5A_TEST_PA1"], 0x5D)
			self.spi_write(registers["RFM69_REG_5C_TEST_PA2"], 0x7C)
			# Set PA Level
			self.paLevel = power + 11
			self.spi_write(registers["RFM69_REG_11_PA_LEVEL"], registers["RF_PALEVEL_PA0_OFF"] | registers["RF_PALEVEL_PA1_ON"] | registers["RF_PALEVEL_PA2_ON"] | self.paLevel )

		# Wait for PA ramp-up
		while((self.spi_read(registers["RFM69_REG_27_IRQ_FLAGS1"]) & registers["RF_IRQFLAGS1_TXREADY"]) == 0):
			pass

		# Transmit
		self.write_fifo(self.buf)

		# Wait for packet to be sent
		while ((self.spi_read(registers["RFM69_REG_28_IRQ_FLAGS2"]) & registers["RF_IRQFLAGS2_PACKETSENT"]) == 0):
			pass

		# Return Transceiver to original mode
		self.set_mode(oldMode)

		# If we were in high power, switch off High Power Registers
		if (power > 17):
			self.spi_write(registers["RFM69_REG_5A_TEST_PA1"], 0x55)
			self.spi_write(registers["RFM69_REG_5C_TEST_PA2"], 0x70)
			self.spi_write(registers["RFM69_REG_13_OCP"], (registers["RF_OCP_ON"] | registers["RF_OCP_TRIM_95"]))

		print ("Transmission complete!")

	def setLnaMode(self, lnaMode):
		self.spi_write(registers["RFM69_REG_58_TEST_LNA"], lnaMode)

	def clearFifo(self):
		self.set_mode(registers["RFM69_MODE_STDBY"])
		self.set_mode(registers["RFM69_MODE_RX"])

	def readTemp(self):
		oldMode = self.mode

		self.set_mode(registers["RFM69_MODE_STDBY"])

		self.spi_write(registers["RFM69_REG_4E_TEMP1"], registers["RF_TEMP1_MEAS_START"])

		while (self.spi_read(registers["RFM69_REG_4E_TEMP1"]) == 0x04):
			pass

		rawTemp = self.spi_read(registers["RFM69_REG_4F_TEMP2"])

		self.set_mode(oldMode)

		return (168 - rawTemp) - 5 # Offset and compensate for self-heating

	def lastRssi(self):
		return self.lastRssi

	def sampleRssi(self):
		# Must only be called in RX mode
		if (self.mode != registers["RFM69_MODE_RX"]):
			# Not sure what happens otherwise, so check this
			return 0

		# Trigger RSSI Measurement
		self.spi_write(registers["RFM69_REG_23_RSSI_CONFIG"], registers["RF_RSSI_START"])

		# Wait for Measurement to complete
		while((registers["RF_RSSI_DONE"] == 0x02) and (self.spi_read(registers["RFM69_REG_23_RSSI_CONFIG"]) == 0)):
			pass

		# Read, store in _lastRssi and return RSSI Value
		self.lastRssi = -(self.spi_read(registers["RFM69_REG_24_RSSI_VALUE"])/2)
		return self.lastRssi

	# Read/Write Functions
	def spi_read(self, register):
		data = bytearray(2)
		data[0] = register & ~0x80
		data[1] = 0
		resp = bytearray(2)
		self.nss.low()
		self.spi.send_recv(data, resp, timeout=5000)
		self.nss.high()
		return resp[1]

	def spi_burst_read(self, register, length):
		data = bytearray(length+1)
		data[0] = register & ~0x80
		for i in range(1,length):
			data[i] = 0
		# We get the length again as the first character of the buffer
		buf = bytearray(length)
		self.nss.low()
		self.spi.send_recv(data, buf, timeout=5000)
		self.nss.high()
		return buf[1:]

	def spi_write(self, register, value):
		data = bytearray(2)
		data[0] = register | 0x80
		data[1] = value
		self.nss.low()
		self.spi.send(data, timeout=5000) 
		self.nss.high()

	def write_fifo(self, data):
		fifo_data = bytearray(len(data)+1)
		fifo_data[0] = registers["RFM69_REG_00_FIFO"] | 0x80
		for i in range(1,len(data)+1):
			fifo_data[i] = data[i-1]
		self.nss.low()
		self.spi.send(fifo_data, timeout=5000)
		self.nss.high()
