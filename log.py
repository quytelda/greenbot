#
# log.py - logging functionality for greenbot
#
# Copyright (C) 2014 Quytelda Gaiwin <admin@tamalin.org>
#
# This file is part of greenbot, the python IRC logging bot.
#
# greenbot is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# greenbot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with greenbot.  If not, see <http://www.gnu.org/licenses/>.

import time
import os

class BufferLogger:
	
	def __init__(self, prefix):
		self.prefix = prefix
		self.buffers = {}

		# if the log directory doesn't exist, create it
		if not os.path.isdir(prefix): os.mkdir(prefix)


	def open_buffer(self, name):
		timestamp = int(time.time())
		buffer = open("%s/%s_%d.log" % (self.prefix, name, timestamp), 'a')
		self.buffers[name] = buffer


	def close_buffer(self, name):
		# close the buffer file stream if it is open
		if not self.buffers[name].closed:
			self.buffers[name].close()


	def log(self, buffer, message):
		# if the buffer file doesn't exist
		if not buffer in self.buffers:
			print "* Buffer %s does not exist." % buffer
			return

		# get timestamp
		timestamp = time.strftime("[%H:%M:%S]", time.localtime())

		# write to the stream and flush
		self.buffers[buffer].write(timestamp + ' ' + message + '\n')
		self.buffers[buffer].flush()

	def cycle(self, buffer):
		if not buffer in self.buffers:
			print "Buffer %s does not exist." % buffer
			return
		
		# cycle by closing and reopening the buffer
		self.log(buffer, "* Cycling to new buffer file...")
		self.close_buffer(buffer)
		self.open_buffer(buffer)
		self.log(buffer, "* Cycled to new buffer file.")


	def cycle_all(self):
		for buffer in self.buffers:
			self.cycle(buffer)


	def close_all(self):
		for buffer in self.buffers:
			self.close_buffer(buffer)
