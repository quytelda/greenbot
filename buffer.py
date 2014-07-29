class IRCBuffer:
	def __init__(self, filename):
		self.filename = filename
		self.open = False
		
	def init(self, msg):
		self.logfile = open(self.filename, 'a')
		self.open = True
		self.write(msg)
		
	def write(self, message):
		if not self.open:
			self.init('Opening buffer...')

		self.logfile.write(message + '\n')
		self.logfile.flush()
		
	def close(self):
		self.logfile.close()
		self.open = False
