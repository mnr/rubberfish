import os

FIFO_PATH = '/tmp/SayThis_Fish'

pipeout = os.open(FIFO_PATH, os.O_WRONLY)
counter = 0
while True:
    time.sleep(1)
    os.write(pipeout, 'Hello, big Number %03d\n' % counter)
    counter = (counter+1) % 5
