"""
sudo raspi-config
enable spi
"""

# works with MCP3008, ch0
# returns x/10ths of a volt
import spidev
import time

spi=spidev.SpiDev() # create a spi object

spiBus = 0          # spi port 0
spiDeviceCh = 0       # GPIO CE0
spiDevice = spi.open(spiBus,spiDeviceCh)

# instructions for this value are found in the MCP3008 datasheet
# Table 5-2: Configure bits for the MCP3008
spiStart = 0b00000001
spiControl = 0b00001000 # single end mcp3008 ch0
""" other spi control values to try
0b1000 # single-end ch0
0b1001 # single-end ch1
0b0000 # differential ch0
0b0001 # differential ch1
"""
spiControlList = [0b1000,0b1001,0b0000,0b0001]
spiPlaceholder = 0b00000000

# to_send = [spiControl,0x02]
# to_send = [spiStart,spiControl,spiPlaceholder]

try:
    while True:
        # time.sleep(1)
        # resp = spi.xfer(to_send)
        # print (resp)
        for spiControl in spiControlList:
            to_send = [spiStart,spiControl,spiPlaceholder]
            resp = spi.xfer(to_send)
            print spiControl," - ",resp
except KeyboardInterrupt: #control-c
    spi.close()         # close the spi device
