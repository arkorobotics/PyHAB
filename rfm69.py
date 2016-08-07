# RFM69.py
#
# Ported to Micropython 2016 Ara Kourchians
#
# Copyright (C) 2014 Phil Crump
#
# Based on RF22 Copyright (C) 2011 Mike McCauley ported to mbed by Karl Zweimueller
# Based on RFM69 LowPowerLabs (https://github.com/LowPowerLab/RFM69/)

import pyb
from pyb import Pin, ExtInt
from pyb import SPI

from time import sleep, time

from RFM69Dict import registers, config

#print (config["RFM69_REG_01_OPMODE"])
#print (registers["RFM69_SPI_WRITE_MASK"])

class RFM69:
	def __init__(self, reset_pin=None, dio0_pin=None, spi_channel=None, config=None):
		self.reset_pin = reset_pin
		self.dio0_pin = dio0_pin
		self.spi_channel = spi_channel
		self.spi = SPI(1, SPI.MASTER, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB, crc=None)
		self.dio0_pin = Pin('X3', Pin.IN, Pin.PULL_DOWN)

	def init_gpio(self):
		self.dio0_pin = Pin('X3', Pin.IN, Pin.PULL_DOWN)

	def init_spi(self):
		self.spi = SPI(1, SPI.MASTER, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB, crc=None)

	def reset(self):
		""" Reset the module, then check it's working. """
		print ("Initialising RFM...")
		self.reset_pin = Pin('X4', Pin.OUT_PP)
		self.reset_pin.high()
		sleep(0.05)                 # TODO: Ara - replace with pyb timer
		self.reset_pin = Pin('X4', Pin.IN, Pin.PULL_DOWN)
		sleep(0.05)

		if (self.spi_read(registers["RFM69_REG_10_VERSION"]) != 0x24):
			print ("Failed to initialise RFM69")

	def read_register(self, register_cls):
	    resp = self.spi_read(register_cls.REGISTER)
	    return register_cls.unpack(resp)

	def write_register(self, register):
	    self.spi_write(register.REGISTER, register.pack())

	def spi_read(self, register):
		data = bytearray(2)
		data[0] = register & ~0x80
		data[1] = 0
		resp = bytearray(2)
		self.spi.send_recv(data, resp, timeout=5000)
		return resp[1]

	def spi_burst_read(self, register, length):
		data = bytearray(length)
		data[0] = register & ~0x80
		for i in range(1, length):
			data[i] = 0
		# We get the length again as the first character of the buffer
		buf = bytearray(length)
		self.spi.send_recv(data, buf, timeout=5000)
		return buf[0:]

	def spi_write(self, register, value):
		data = bytearray(2)
		data[0] = register | 0x80
		data[1] = value
		self.spi.send(data, timeout=5000) 

	def write_fifo(self, data):
		fifo_data = bytearray(2)
		fifo_data[0] = Register.FIFO | 0x80
		fifo_data[1] = data
		self.spi.send(fifo_data, timeout=5000) 
