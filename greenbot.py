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
import json
import sqlite3
import re

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.words.protocols import irc
from twisted.internet.task import LoopingCall
from twisted.internet import reactor, ssl

import log

import commands.ping
import commands.quit
import commands.auth
import commands.status
import commands.raw
import commands.link
import commands.help
import commands.alias
import commands.logout
import commands.clear

VERSION = 3.1

class GreenBot(irc.IRCClient):

	nickname = None
	username = None
	password = None
	quitted = False

	hooks = {}
	
	channels = {}
	admins = []

	start_time = None
	
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

	def signedOn(self):
		# record sign-on time for calculating uptime
		self.start_time = time.time()


	def joined(self, channel):
		pass


	def left(self, channel):
		pass

	### actions the bot sees other users doing

	def userQuit(self, user, quitMessage):
		pass

	def userJoined(self, user, channel):
		pass

	def userLeft(self, user, channel):
		pass
		
	def modeChanged(self, user, channel, set, modes, args):
		pass

	def userRenamed(self, oldname, newname):
			

	def privmsg(self, user, channel, message):
		# if the private message is addressed to me, it is a command
		if channel == self.nickname:
			self.handle_command(user, message, user.split('!')[0])
			return

		# if it starts with PREFIX, it is a command
		if message.startswith(self.factory.prefix) and len(message) > 1:
			self.handle_command(user, message[1:], channel)


	def action(self, user, channel, data):
		pass


	def noticed(self, user, channel, message):
		pass


	def names(self, channel):
		self.transport.write("NAMES %s\r\n" % channel)


	def irc_RPL_NAMREPLY(self, prefix, params):
		# parse the parameters
		target = params[0]
		chan_type = params[1]
		channel = params[2]

		names = params[-1]

		# parse the names list
		namlist = names.strip().split(' ')
		self.channels[channel] = namlist
		
	

	# ------------------- Bot Command Functions ------------------- #

	def register_hooks(self):
		pass


	def handle_command(self, source, command, receive):
		# split into components by ' '
		elems = command.strip().split(' ')

		# parse the command
		if len(elems) < 1: return
		cmd = elems[0].upper()
		args = elems[1:]

		if cmd in self.hooks:
			try: self.hooks[cmd].handle_command(self, source, command, args, receive)
			except Exception as e: self.msg(receive, "Internal error! Please fix me.")
		else:
			self.msg(receive, "Unrecognized Command [%s]; try HELP." % cmd)
			
	
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

		bot.register_hooks()
		
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
