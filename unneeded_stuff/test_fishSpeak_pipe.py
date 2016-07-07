import os

FIFO_PATH = '/tmp/SayThis_Fish'

pipeout = os.open(FIFO_PATH,"w")

saythis = "hello, I am a fish"
os.write(pipeout, saythis)
os.close(pipeout)
