"""
sudo raspi-config
enable spi

spi documentation
http://tightdev.net/SpiDev_Doc.pdf
"""

# works with MCP3008, ch0
# returns x/10ths of a volt
import spidev
import time
import csv

spi=spidev.SpiDev() # create a spi object

spiBus = 0          # spi port 0
spiSpeed = 200000
spiDeviceCh = 0       # GPIO CE0
spiDevice = spi.open(spiBus,spiDeviceCh)
spi.max_speed_hz=spiSpeed # mcp3008 requires >10khz


# instructions for this value are found in the MCP3008 datasheet
# Table 5-2: Configure bits for the MCP3008
spiStart = 0b00000001
spiControl = 0b00001000 # single end mcp3008 ch0
""" other spi control values to try
0b1000 0000 # single-end ch0
0b1001 0000 # single-end ch1
0b0000 0000 # differential ch0 = in+
0b0001 0000 # differential ch1 = in+
"""
spiControlList = [0b10000000,0b10010000,0b00000000,0b00010000]
# spiControlList = [0b10000000]
spiPlaceholder = 0b00000000

# to_send = [spiControl,0x02]
# to_send = [spiStart,spiControl,spiPlaceholder]

with open('spiCapture.csv', 'wb') as f:
    writer = csv.writer(f)

try:
    while True:
        # time.sleep(1)
        # resp = spi.xfer(to_send)
        # print (resp)
        for spiControl in spiControlList:
            to_send = [spiStart,spiControl,spiPlaceholder]
            resp = spi.xfer(to_send)
            # print (bin(spiControl) + " - " + str(resp))
            writer.writerows(spiControl,str(resp))
            time.sleep(.25)
except KeyboardInterrupt: #control-c
    spi.close()         # close the spi device
