# if you are using this with Raspberry Pi, don't forget to use raspi-config to enable i2c
# i2c-tools is handy. sudo apt-get install i2c-tools
# smbus adds i2c python interfaces . sudo apt-get install python-smbus
# this page was helpful: http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/
# also helpful: http://raspberrypi.stackexchange.com/questions/36983/how-to-change-read-channels-on-pcf8591
# Here is a data sheet, although it isn't 100% for this particular board: http://www.nxp.com/documents/data_sheet/PCF8591.pdf
# blog.chrysocome.net/2012/12/i2c-analog-to-digital-converter.html
# https://brainfyre.wordpress.com/2012/10/25/pcf8591-yl-40-ad-da-module-review/

# Removing a jumper allows an input channel to be fed from one of the external pins, labelled accordingly.

# connecting the Module
# SDA IIC data interface connected microcontroller IO ports (P2.0)
# SCL IIC clock interface connected microcontroller IO port (P2.1)
# The cathode interface external VCC power 3.3/5V positive power supply
# GND Negative interface external 3.3/5V negative supply

import smbus
from time import sleep

class PCF8591:
    """
    python interface to uxcell PCF8591 AD/DA Converter Module Analog to Digital to Conversion. 
    As purchased from amazon, ASIN B00BXX4UWC
    """

    # i2c bus (0 -- original Pi, 1 -- Rev 2 Pi)
    I2CBUS = 1

    # use i2cdetect -y 1 to discover this number
    # Rumor:  address is hard-coded (all i2c addr lines are connected to ground, so the addr is 0x48)
    # LCD Address
    ADDRESS = 0x48

    def __init__(self, addr=ADDRESS, port=I2CBUS):
        self.addr = addr
        self.bus = smbus.SMBus(port)

    def read_a2d(self):
        # Support 4 channel analog voltage the acquisition signal input (voltage input range of 0 - 5V)
        pass

    def write_d2a(self):
        # A module with DA output indicator (D2), when the DA output voltage reaches a certain value, the indicator light, the higher the voltage value, the brighter lights
        pass

    def read_temp(self):
        # Jumper P4 for AIN1: The temperature sensed by the R6 thermister is provided to the ADC
        pass

    def read_light(self):
        # Jumper P5 to AIN0: The R7 photocell voltage (resistance drop) is provided to the DAC.
        pass

    def read_pot(self):
        #  The module integrates a Road 0 - 5V voltage input acquisition (through the blue and white potentiometer to adjust the input voltage)
        # Jumper P6 to AIN3: The single turn 10K ohm trimpot voltage (resistance drop – brighter light, lower resistance).
        pass

    def read_ain0(self):
        pass
    def read_ain1(self):
        pass
    def read_ain2(self):
        pass
    def read_ain3(self):
        pass

# overview from http://www.icstation.com/pcf8591-adda-converter-module-light-temperature-intensity-p-2494.html
# PCF8591 AD / DA chip introduced:
# The PCF8591 Is a monolithically integrated, and a separate power supply, low-power, 8-bit CMOS data acquisition devices. The PCF8591 has the four analog inputs, one analog output and a serial I2C bus interface. PCF8591 three address pins A0, A1 and A2 can be used in hardware address programmed 8 PCF8591 device allows access to the same I2C bus, without the need for additional hardware. On the PCF8591 device input and output of the address, control and data signals are transmitted in serial fashion via the two-wire bidirectional I2C bus.
#
# PCF8591 main performance indicators:
# ★ single power supply
# ★ PCF8591 operating voltage range of 2.5V-6V
# ★ low standby current
# ★ via I2C bus serial input / output
# ★ PCF8591 by 3 hardware address pins addressing
# ★ PCF8591 I2C bus speed sampling rate decided
# ★ 4 analog inputs programmable single-ended or differential input
# ★ automatic incremental channel selection
# ★ PCF8591 analog voltage range from VSS to VDD
# ★ PCF8591 built-in track-and-hold circuit
# ★ 8-bit successive approximation A/D converter
# ★ 1 analog output DAC gain
#
# AINO chip analog input interface 0
# AIN1 chip analog input interface 1
# AIN2 chip analog input interface 2
# AIN3 chip analog input interface 3
# OUT analog output
