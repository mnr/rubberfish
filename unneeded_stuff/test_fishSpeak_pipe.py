import os

FIFO_PATH = '/tmp/SayThis_Fish'

pipeout = os.open(FIFO_PATH, 'w')

os.write(pipeout, 'Hello, I am a fish')
