class TTSWSClientProtocol(WebSocketClientProtocol):
""" as found at https://www.ibm.com/watson/developercloud/doc/text-to-speech/websockets.shtml#python """

   def __init__(self):
      WebSocketClientProtocol.__init__(self)
      self.msgs = []
      self.binaryBytesReceived = 0

   def onConnect(self, response):
      logging.info('onConnect')

   def onOpen(self):
      logging.info('onOpen')
      self.sendMessage(json.dumps({'text': 'Hello <mark name="here"/> world.',
                                   'accept': 'audio/ogg;codecs=opus'}))

   def onMessage(self, msg, binary):
      if binary:
         logging.info('binary message: %s bytes received', len(msg))
         self.binaryBytesReceived += len(msg)
      else:
         logging.info(msg)
         self.msgs.append(json.loads(msg))

   def onClose(self, wasClean, code, reason):
      logging.info((wasClean, code, reason))
