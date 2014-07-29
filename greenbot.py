#!/usr/bin/python

# 
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

from twisted.internet.protocol import ClientFactory
from twisted.words.protocols import irc

import commands.ping
import commands.quit
import commands.admins
import commands.auth
import commands.status
import commands.raw
import commands.play
import commands.link
import commands.help

from buffer import IRCBuffer

class GreenBot(irc.IRCClient):

	nickname = "greenbot"
	prefix = '`'

	hooks = {}
	
	admins = []
	
	# ------------------- Connection Event Handlers ------------------- #
	
	def connectionMade(self):
		# call the parent method
		irc.IRCClient.connectionMade(self)
		
		# status message
		host = self.transport.getPeer().host
		
		# open the log file stream
		self.factory.logger = open(self.factory.filename, 'a', 0)
		
		# log the new connection
		self.factory.logger.write("* Connected established with %s.\n" % host)


	def connectionLost(self, reason):
		# call parent method
		irc.IRCClient.connectionMade(self)
		
		# log the lost connection (before we close the logs :P)
		self.factory.logger.write("* Connection lost (%s).\n" % reason)
		
		# close log file stream
		self.factory.logger.close()


	# ------------------- IRC Event Handlers ------------------- #

	def signedOn(self):
		# join all the channels in the autojoin list
		self.join(self.factory.autojoin)
	

	def joined(self, channel):
		print "* joined", channel


	def left(self, channel):
		print "* left", channel
		
	
	def userQuit(self, user, quitMessage):
		# if the user is an admin, remove them from the list
		if user in self.admins:
			self.admins.remove(user)
			
	
	def userRenamed(self, oldname, newname):		
		if oldname in self.admins:
			self.admins.remove(oldname)
			self.admins.append(newname)


	def privmsg(self, user, channel, message):
		# if the private message is addressed to me, it is a command
		if channel == self.nickname:
			self.handle_command(user, message, user.split('!')[0])

		# if it starts with PREFIX, it is a command
		if message.startswith(self.prefix) and len(message) > 1:
			self.handle_command(user, message[1:], channel)


	def lineReceived(self, line):
		# keep parent functionality
		irc.IRCClient.lineReceived(self, line)
	
		# log the line
		# we'll use the local timestamp
		t = time.localtime()
		timestamp = time.strftime("[%H:%M:%S]", t)
		self.factory.logger.write(timestamp + ' ' + line + '\r\n')


	# ------------------- Bot Command Functions ------------------- #

	def register_hooks(self):
		# register hooks
		self.hooks['PING'] = commands.ping
		self.hooks['QUIT'] = commands.quit
		self.hooks['ADMINS'] = commands.admins
		self.hooks['AUTH'] = commands.auth
		self.hooks['STATUS'] = commands.status
		self.hooks['RAW'] = commands.raw
		self.hooks['PLAY'] = commands.play
		self.hooks['LINK'] = commands.link
		self.hooks['HELP'] = commands.help


	def handle_command(self, source, command, receive):
		# split into components by ' '
		elems = command.split(' ')

		# parse the command
		if len(elems) < 1: return
		cmd = elems[0].upper()
		args = elems[1:]

		if cmd in self.hooks:
			self.hooks[cmd].handle_command(self, source, command, args, receive)
		else:
			self.notice(receive, "Unrecognized Command [%s]!" % cmd)



class GreenbotFactory(ClientFactory):

	autojoin = '#green'

	def __init__(self, filename):
		self.filename = filename


	def buildProtocol(self, addr):
		bot = GreenBot()
		
		bot.factory = self
		bot.register_hooks()
		
		return bot
		
