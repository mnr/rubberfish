import os

FIFO_PATH = '/tmp/SayThis_Fish'

pipeout = os.open(FIFO_PATH,os.O_WRONLY)

os.write(pipeout, bytes("hello, I am a fish", 'UTF-8'))
os.close(pipeout)
