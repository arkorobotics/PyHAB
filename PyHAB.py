# PyHAB
# WRITTEN BY: Arko at EMFCAMP 2016 - HABVILLE

import pyb
from pyb import UART
from pyb import SPI

import RFM69
from registers import registers
from config import config

from time import sleep, time

state = "RESET";

#GGA          Global Positioning System Fix Data
#123519       Fix taken at 12:35:19 UTC
#4807.038,N   Latitude 48 deg 07.038' N
#01131.000,E  Longitude 11 deg 31.000' E
#1            Fix quality: 0 = invalid
#				1 = GPS fix (SPS)
#				2 = DGPS fix
#				3 = PPS fix
#				4 = Real Time Kinematic
#				5 = Float RTK
#				6 = estimated (dead reckoning) (2.3 feature)
#				7 = Manual input mode
#				8 = Simulation mode
#08           Number of satellites being tracked
#0.9          Horizontal dilution of position
#545.4,M      Altitude, Meters, above mean sea level
#46.9,M       Height of geoid (mean sea level) above WGS84
#ellipsoid
#(empty field) time in seconds since last DGPS update
#(empty field) DGPS station ID number
#*47          the checksum data, always begins with *
#nema_msg = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
nema_msg = "" #"$GPGGA,,,,,,,,,,,,,,*47"
latitude = ""
longitude = ""
altitude = ""

# no alt sample packet: 3xL34.091,-118.067,T23X144716.00:N6ARA[PyHAB]
# full sample packet: 3oL34.091,-118.067,297.4T24X144937.00:N6ARA[PyHAB]
data_count = ["a" , "b" , "c" , "d" , "e" , "f" , "g" , "h" ,
"i" , "j" , "k" , "l" , "m" , "n" , "o" , "p" ,
"q" , "r" , "s" , "t" , "u" , "v" , "w" , "x" ,
"y" , "z"]

data_idx = 0

# Initialize perpherial variables
uart = UART(1, 9600)
#spi = SPI(1, SPI.MASTER, baudrate=1000000, polarity=0, phase=0, firstbit=SPI.MSB, crc=None)
rfm69 = RFM69.RFM69()

led = pyb.LED(4)
led.toggle()
pyb.delay(250)
led.toggle()
pyb.delay(250)
led.toggle()

def fault(*args):
    global state
    print ("Fault!")
    print ("Rebooting...")
    state = "RESET"
    return "RESET"

def reset():
	print ("Restarting...")
	return "INIT"

def init():
	print ("Initializing")

	# Initialize GPS
	# UART(1) is on PB: 
	# (TX,  RX) 
	# (X9,  X10)
	# (PB6, PB7)
	uart = UART(1, 9600)
	# Maybe add read_buf_len=128?
	# Maybe add timeout_char=200
	uart.init(9600, bits=8, stop=1, parity=None, timeout=5000)


	# Initialize Radio (RFM69)
	# SPI(1) is on PA:
	# (DIO0, RESET, NSS, SCK, MISO, MOSI) 
	# (X3,   X4,    X5,  X6,  X7,   X8) 
	# (PA2,  PA3,   PA4, PA5, PA6,  PA7)
	rfm69 = RFM69.RFM69()
	sleep(1)
	# Check version
	if (rfm69.getVersion() == 0x24):
		print ("RFM69 Version Valid: 0x24")
	else:
		print ("RFM69 Version Invalid!")
		return "FAULT"

	return "GPS_ACQ"

def gps_acq():
	print ("Acquiring GPS data")

	global nema_msg

	# Default GPS Data is 8 lines
	nema_sentence_flag = 0
	while (nema_sentence_flag != 1):
		nema_msg = uart.readline() 
		print (nema_msg)
		if (nema_msg[3:6] == bytearray(b'GGA')):
			nema_sentence_flag = 1

	print ("message found: %s" % nema_msg)
	return "PARSE_GPS"

def parse_gps():
	print ("Parsing GPS data")

	global nema_msg
	global time
	global latitude
	global longitude
	global altitude

	nema_arr = str(nema_msg).split(',')
	print (nema_arr)
	time = nema_arr[1]

	latitude_sign = ''
	longitude_sign = ''

	if(nema_arr[3] == 'N'): 
		latitude_sign = ''
	elif(nema_arr[3] == 'S'):
		latitude_sign = '-'

	if(len(nema_arr[2]) > 0):
		latitude = "%s%.3f" % (latitude_sign, float(nema_arr[2])/100)

	if(nema_arr[5] == 'E'): 
		longitude_sign = ''
	elif(nema_arr[5] == 'W'):
		longitude_sign = '-'

	if(len(nema_arr[2]) > 0):
		longitude = "%s%.3f" % (longitude_sign, float(nema_arr[4])/100)

	altitude = nema_arr[9]

	return "TRANSMIT"

def transmit():
	print (" ")
	print ("Transmitting position and telemetry")

	rfmtemp = rfm69.readTemp()

	print ("Temperature: %d" % rfmtemp)
	print ("RSSI: %d" % rfm69.sampleRssi())
	
	global time
	global latitude
	global longitude
	global altitude

	global data_count
	global data_idx

	if(data_idx >= 0 and data_idx < 25):
		data_idx += 1
	else:
		data_idx = 0

	print ("dataidx: %d" % data_idx)
	ukhasnode_str = "3%sL%s,%s,%sT%dX%s:N6ARA[PyHAB]" % (data_count[data_idx],latitude,longitude,altitude,rfmtemp,time)

	data = bytearray(ukhasnode_str)

	rfm69.send(data, len(data), 19)
	print (ukhasnode_str)
	print (" ")
	print (" ")
	sleep(1)
	print ("Check rx buf")
	rfm69.set_mode(registers["RFM69_MODE_RX"])
	rfm69.setLnaMode(registers["RF_TESTLNA_SENSITIVE"])
	#rfm69.checkRx()
	#print (rfm69.recv())
	rfm69.clearFifo()
	print (" ")

	return "GPS_ACQ"

states = {
		"FAULT": fault,
		"RESET": reset,
		"INIT": init, 
		"GPS_ACQ": gps_acq,
		"PARSE_GPS": parse_gps, 
		"TRANSMIT": transmit
}

# Semi-Safe State Machine?
while (True):
	state = states.get(state, fault)()
	print (state)

