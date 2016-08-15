# RFM69 Dictionary
#
# Ported to Micropython 2016 Ara Kourchians
#
# C code Author: Phil Crump (phildcrump@gmail.com)
# Copyright (C) 2014 Phil Crump
# Based on RF22.h
# Author: Mike McCauley (mikem@open.com.au)
# Copyright (C) 2011 Mike McCauley

# Minimal register/config dictionary, see RFM69Dict_complete.py for more
registers = {
"RFM69_SPI_WRITE_MASK" : 0x80,
"RFM69_MAX_MESSAGE_LEN" : 64,
"RFM69_FIFO_SIZE" : 64,
"RFM69_MODE_SLEEP" :    0x00, # 0.1uA
"RFM69_MODE_STDBY" :    0x04, # 1.25mA
"RFM69_MODE_RX" :       0x10, # 16mA
"RFM69_MODE_TX" :       0x0c, # >33mA
"RFM69_REG_58_TEST_LNA" :       0x58,
"RF_TESTLNA_SENSITIVE" :        0x2D,
"RFM69_REG_00_FIFO" :           0x00,
"RFM69_REG_01_OPMODE" :         0x01,
"RFM69_REG_02_DATA_MODUL" :     0x02,
"RFM69_REG_03_BITRATE_MSB" :    0x03,
"RFM69_REG_04_BITRATE_LSB" :    0x04,
"RFM69_REG_05_FDEV_MSB" :       0x05,
"RFM69_REG_06_FDEV_LSB" :       0x06,
"RFM69_REG_07_FRF_MSB" :        0x07,
"RFM69_REG_08_FRF_MID" :        0x08,
"RFM69_REG_09_FRF_LSB" :        0x09,
"RFM69_REG_0B_AFC_CTRL" :       0x0B,
"RFM69_REG_10_VERSION" :        0x10, #Version and serial number
"RFM69_REG_11_PA_LEVEL" :       0x11,
"RFM69_REG_12_PA_RAMP" :        0x12,
"RFM69_REG_13_OCP" :            0x13,
"RFM69_REG_18_LNA" :            0x18,
"RFM69_REG_19_RX_BW" :          0x19,
"RFM69_REG_1E_AFC_FEI" :        0x1E,
"RFM69_REG_23_RSSI_CONFIG" :    0x23,
"RFM69_REG_24_RSSI_VALUE" :     0x24,
"RFM69_REG_25_DIO_MAPPING1" :   0x25,
"RFM69_REG_26_DIO_MAPPING2" :   0x26,
"RFM69_REG_27_IRQ_FLAGS1" :     0x27,
"RFM69_REG_28_IRQ_FLAGS2" :     0x28,
"RFM69_REG_2E_SYNC_CONFIG" :    0x2E,
"RFM69_REG_2F_SYNCVALUE1" :     0x2F,
"RFM69_REG_30_SYNCVALUE2" :     0x30,
"RFM69_REG_37_PACKET_CONFIG1" : 0x37,
"RFM69_REG_38_PAYLOAD_LENGTH" : 0x38,
"RFM69_REG_3C_FIFO_THRESHOLD" : 0x3C,
"RFM69_REG_3D_PACKET_CONFIG2" : 0x3D,
"RFM69_REG_6F_TEST_DAGC" :      0x6F,
"RF_OPMODE_SEQUENCER_ON" :              0x00,  # Default
"RF_OPMODE_LISTEN_OFF" :                    0x00,  # Default
"RF_DATAMODUL_DATAMODE_PACKET" :             0x00,  # Default
"RF_DATAMODUL_MODULATIONTYPE_FSK" :             0x00,  # Default
"RF_DATAMODUL_MODULATIONSHAPING_00" :           0x00,  # Default
"RF_AFCLOWBETA_OFF" :                   0x00,    # Default
"RF_PALEVEL_PA0_OFF" :      0x00,
"RF_PALEVEL_PA1_ON" :       0x40,
"RF_PALEVEL_PA2_ON" :       0x20,
"RF_PARAMP_500" :                       0x03,
"RF_OCP_OFF" :                              0x0F,
"RF_OCP_ON" :                               0x1A,  # Default
"RF_OCP_TRIM_95" :                      0x0A,
"RF_LNA_ZIN_50" :                               0x00,
"RF_RXBW_DCCFREQ_010" :                     0x40,  # Default
"RF_RXBW_MANT_16" :                           0x00,
"RF_RXBW_EXP_2" :                           0x02,
"RF_AFCFEI_AFCAUTOCLEAR_ON" :               0x08,
"RF_AFCFEI_AFCAUTO_ON" :                        0x04,
"RF_RSSI_DONE" :                                    0x02,
"RF_RSSI_START" :                                   0x01,
"RF_DIOMAPPING1_DIO0_01" :                  0x40,
"RF_DIOMAPPING2_CLKOUT_OFF" :                 0x07,  # Default
"RF_IRQFLAGS1_TXREADY" :                        0x20,
"RF_IRQFLAGS2_PACKETSENT" :                   0x08,
"RF_IRQFLAGS2_PAYLOADREADY" :                0x04,
"RF_SYNC_ON" :                              0x80,  # Default
"RF_SYNC_FIFOFILL_AUTO" :           0x00,  # Default -- when sync interrupt occurs
"RF_SYNC_SIZE_2" :                      0x08,
"RF_SYNC_TOL_0" :                           0x00,  # Default
"RF_PACKET1_FORMAT_VARIABLE" :      0x80,
"RF_PACKET1_DCFREE_OFF" :           0x00,  # Default
"RF_PACKET1_CRC_ON" :                         0x10,  # Default
"RF_PACKET1_CRCAUTOCLEAR_ON" :      0x00,  # Default
"RF_PACKET1_ADRSFILTERING_OFF" :                  0x00,  # Default
"RF_FIFOTHRESH_TXSTART_FIFOTHRESH" :          0x00,
"RF_FIFOTHRESH_TXSTART_FIFONOTEMPTY" :      0x80,  # Default
"RF_FIFOTHRESH_VALUE" :                             0x0F,  # Default
"RF_PACKET2_RXRESTARTDELAY_2BITS" :           0x10,
"RF_PACKET2_AUTORXRESTART_ON" :                 0x02,  # Default
"RF_PACKET2_AES_OFF" :                              0x00,  # Default
"RF_TEMP1_MEAS_RUNNING" :               0x04,
"RF_DAGC_IMPROVED_LOWBETA0" :   0x30,  # Recommended default
"RFM69_REG_4E_TEMP1" :          0x4E,
"RFM69_REG_4F_TEMP2" :          0x4F,
"RF_TEMP1_MEAS_START" :         0x08,
"RFM69_REG_5A_TEST_PA1" :       0x5A,
"RFM69_REG_5C_TEST_PA2" :       0x5C,
}

config = {
    "RFM69_REG_01_OPMODE" :      registers["RF_OPMODE_SEQUENCER_ON"] | registers["RF_OPMODE_LISTEN_OFF"] | registers["RFM69_MODE_RX"],
    "RFM69_REG_02_DATA_MODUL" :  registers["RF_DATAMODUL_DATAMODE_PACKET"] | registers["RF_DATAMODUL_MODULATIONTYPE_FSK"] | registers["RF_DATAMODUL_MODULATIONSHAPING_00"],
    "RFM69_REG_03_BITRATE_MSB" : 0x3E, # 2000 bps
    "RFM69_REG_04_BITRATE_LSB" : 0x80,
    "RFM69_REG_05_FDEV_MSB" :    0x00, # 12000 hz (24000 hz shift)
    "RFM69_REG_06_FDEV_LSB" :    0xC5,
    "RFM69_REG_07_FRF_MSB" :     0x6C, #0xD9, # 869.5 MHz
    "RFM69_REG_08_FRF_MID" :     0x80, #0x60, # calculated: 0x80?
    "RFM69_REG_09_FRF_LSB" :     0x00, #0x12,
    "RFM69_REG_0B_AFC_CTRL" :    registers["RF_AFCLOWBETA_OFF"], # AFC Offset On
    "RFM69_REG_11_PA_LEVEL" : registers["RF_PALEVEL_PA0_OFF"] | registers["RF_PALEVEL_PA1_ON"] | registers["RF_PALEVEL_PA2_ON"] | 0x1f, # 50mW
    "RFM69_REG_12_PA_RAMP" : registers["RF_PARAMP_500"], # 500us PA ramp-up (1 bit)
    "RFM69_REG_13_OCP" :         registers["RF_OCP_ON"] | registers["RF_OCP_TRIM_95"],
    "RFM69_REG_18_LNA" :         registers["RF_LNA_ZIN_50"], # 50 ohm for matched antenna, 200 otherwise
    "RFM69_REG_19_RX_BW" :       registers["RF_RXBW_DCCFREQ_010"] | registers["RF_RXBW_MANT_16"] | registers["RF_RXBW_EXP_2"], # Rx Bandwidth: 128KHz
    "RFM69_REG_1E_AFC_FEI" :     registers["RF_AFCFEI_AFCAUTO_ON"] | registers["RF_AFCFEI_AFCAUTOCLEAR_ON"], # Automatic AFC on, clear after each packet
    "RFM69_REG_25_DIO_MAPPING1" : registers["RF_DIOMAPPING1_DIO0_01"],
    "RFM69_REG_26_DIO_MAPPING2" : registers["RF_DIOMAPPING2_CLKOUT_OFF"], # Switch off Clkout
    "RFM69_REG_2E_SYNC_CONFIG" : registers["RF_SYNC_ON"] | registers["RF_SYNC_FIFOFILL_AUTO"] | registers["RF_SYNC_SIZE_2"] | registers["RF_SYNC_TOL_0"],
    "RFM69_REG_2F_SYNCVALUE1" : 0x2D,
    "RFM69_REG_30_SYNCVALUE2" : 0xAA,
    "RFM69_REG_37_PACKET_CONFIG1" : registers["RF_PACKET1_FORMAT_VARIABLE"] | registers["RF_PACKET1_DCFREE_OFF"] | registers["RF_PACKET1_CRC_ON"] | registers["RF_PACKET1_CRCAUTOCLEAR_ON"] | registers["RF_PACKET1_ADRSFILTERING_OFF"],
    "RFM69_REG_38_PAYLOAD_LENGTH" : registers["RFM69_FIFO_SIZE"], # Full FIFO size for rx packet
    "RFM69_REG_3C_FIFO_THRESHOLD" : registers["RF_FIFOTHRESH_TXSTART_FIFONOTEMPTY"] | 0x05, #TX on FIFO not empty
    "RFM69_REG_3D_PACKET_CONFIG2" : registers["RF_PACKET2_RXRESTARTDELAY_2BITS"] | registers["RF_PACKET2_AUTORXRESTART_ON"] | registers["RF_PACKET2_AES_OFF"], #RXRESTARTDELAY must match transmitter PA ramp-down time (bitrate dependent)
    "RFM69_REG_6F_TEST_DAGC" : registers["RF_DAGC_IMPROVED_LOWBETA0"] # run DAGC continuously in RX mode, recommended default for AfcLowBetaOn=0
}

