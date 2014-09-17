#
# greenbot.py - Primary entry point for greenbot software
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
import sys
import os

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.words.protocols import irc
from twisted.internet import reactor, ssl

import modules
from modules import *

VERSION = 3.1

class GreenBot(irc.IRCClient):

	nickname = None
	username = None
	password = None
	quitted = False

	modules = []
	
	channels = {}
	admins = []


	# ------------------- Connection Event Handlers ------------------- #
	
	def connectionMade(self):
		# call the parent method
		irc.IRCClient.connectionMade(self)
		
		# status message
		host = self.transport.getPeer().host


	def connectionLost(self, reason):
		# call parent method
		irc.IRCClient.connectionMade(self)


	# ------------------- IRC Message Event Handlers ------------------- #

	def privmsg(self, user, channel, message):
		# if the private message is addressed to me, it is a command
		if channel == self.nickname:
			self.handle_bot_command(user, message, user.split('!')[0])
			return

		# if it starts with PREFIX, it is a command
		if message.startswith(self.factory.prefix) and len(message) > 1:
			self.handle_bot_command(user, message[1:], channel)


	def names(self, channel):
		self.transport.write("NAMES %s\r\n" % channel)
		
	# ------------------- Module functions ------------------- #

	# ------------------- Bot Command Functions ------------------- #

	def load_modules(self):
		print dir(modules)
		for module in dir(modules):
			if module.startswith('__'): continue

			print "* loading module:", module
			mod = sys.modules['modules.%s' % module]
			
			# put in master list
			self.modules.append(mod)


	def handleCommand(self, command, prefix, params):

		# execute pre-command module hooks
		for mod in self.modules:
			hook = getattr(mod, "pre_irc_%s" % command, None)
			if hook: hook(self, prefix, params)

		# regular handling (superclass)
		irc.IRCClient.handleCommand(self, command, prefix, params)
		
		# execute post-command module hooks
		for mod in self.modules:
			hook = getattr(mod, "irc_%s" % command, None)
			if hook: hook(self, prefix, params)


	def handle_bot_command(self, source, message, receive):

		# we haven't parsed the message yet
		msg = self.parse_message(message)
	
		for mod in self.modules:
			hook = getattr(mod, "bot_%s" % msg['command'], None)
			if hook: hook(self, source, msg['params'], receive)
			
	
	# ------------------- Convenience Functions ------------------- #
			
	def notify(self, message):
		pass


	def nick_in_channel(self, nick, channel):
		namlist = self.channels[channel]
		for name in namlist:
			if re.match("[+%@&~]*" + nick, name): return True

		return False


	def privileged_in_channel(self, nick, channel):
		namlist = self.channels[channel]
		for name in namlist:
			if re.match('[%@&~]' + nick, name): return True

		return False
		
	def parse_message(self, raw):
		"""
		Parses a raw bot command message into a dictionary representing it's compository elements.
		Bot commands are in the format: COMMAND (SINGLE PARAM) (:TRAILING PARAM)
		Single params are space separated, while a trailing param may contain spaces.
		"""
		message = {}
	
		elems = raw.strip().split(' ')
	
		message['command'] = elems.pop(0).upper()
	
		# parse the parameters
		message['params'] = []

		for i in range(0, len(elems)):
			if elems[i].startswith(':'):
				message['params'].append(' '.join(elems[i:]))
				break

			message['params'].append(elems[i])

		return message


class GreenbotFactory(ReconnectingClientFactory):

	quitted = False

	def __init__(self):
		### global properties (defaults)
		self.nickname = "greenbot"
		self.username = "greenbot"
		self.srv_password = None
		self.password = None

		self.prefix = "`"
		self.autojoin = None
		self.admin_channel = None
		self.admin_channel_modes = "+mnst"

		self.log_path = "greenbot"
		self.logger = None
		self.cycle = 86400 # 24 hours


	def buildProtocol(self, addr):
		bot = GreenBot()
		
		# set needed properties
		bot.factory = self
		bot.nickname = self.nickname
		bot.username = self.username
		bot.password = self.srv_password

		bot.load_modules()
		
		self.resetDelay() # required for reconnecting clients
		
		return bot

	def clientConnectionLost(self, connector, reason):
		print "* Disconnected from server."
		if self.quitted:
			print "* Exiting main loop."
			reactor.stop()
		else:
			print "* Reconnecting..."
			ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
	
	def clientConnectionFailed(self, connector, reason):
		print "* Connection failed.  Retrying..."
		ReconnectingClientFactory.clientConnectionLost(self, connector, reason)


def start(addr, port, factory, use_ssl = False):
	if use_ssl:
		reactor.connectSSL(addr, port, factory, ssl.ClientContextFactory())
	else:
		reactor.connectTCP(addr, port, factory)
	
	# now that connection is initiated, run the reactor and get off the ground
	# basically: "Away we go!"
	reactor.run()
	
if __name__ == "__main__":
	register_hooks()
