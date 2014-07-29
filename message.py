# message.py - Parsing for incoming messages
#
# Copyright (C) 2014 Quytelda Gaiwin <admin@tamalin.org>
#
# This file is part of GreenIRCd, the python IRC daemon.
#
# GreenIRCd is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# GreenIRCd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GreenIRCd.  If not, see <http://www.gnu.org/licenses/>.
class Command:
	def __init__(self, raw_msg = None):
		# parse raw_msg, if provided
		if raw_msg == None: return

		# first, split the command into its space-separated components
		components = raw_msg.split(' ')

		ptr = 0
		# first, determine the source of the message
		if(components[ptr].startswith(':')): # there is a prefix
			self.source = components[ptr][1:]
			ptr = ptr + 1
		
		# then, parse the command
		self.command = components[ptr]
		ptr = ptr + 1
		
		# next, parse the arguments
		# they are either trailing (following ':') or middle
		self.params = []
		for i in range(ptr, len(components)):
			if not components[i].startswith(':'):
				self.params.append(components[i])
			else: # trailing arguments
				self.params.append((' '.join(components[i:]))[1:])
				break
