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
		
		# initiate the cycling log files
		self.factory.logger = log.BufferLogger(self.factory.log_path)
		log_cycle = LoopingCall(self.factory.logger.cycle_all)
		log_cycle.start(self.factory.cycle)
		
		# log the new connection
		self.factory.logger.open_buffer('greenbot') # TODO null that
		self.factory.logger.log('greenbot', "* Connection established with %s.\n" % host)


	def connectionLost(self, reason):
		# call parent method
		irc.IRCClient.connectionMade(self)
		
		# log the lost connection (before we close the logs :P)
		self.factory.logger.log('greenbot', "* Connection lost (%s).\n" % reason)
		
		# close log file stream
		self.factory.logger.close_all()


	# ------------------- IRC Message Event Handlers ------------------- #

	def signedOn(self):
		# record sign-on time for calculating uptime
		self.start_time = time.time()

		# identify myself
		self.transport.write("MODE %s +B\r\n" % self.nickname)

		# join the admin channel, if there is one
		# the admin channel will have special properties for the bot
		if self.factory.admin_channel:
			self.register_admin_channel(self.factory.admin_channel)
	
		# join all the channels in the autojoin list
		if self.factory.autojoin:
			self.join(self.factory.autojoin)


	def joined(self, channel):
		self.notify("[info] joined %s" % channel)
		self.channels[channel] = None
		
		# open a buffer for this channel
		self.factory.logger.open_buffer(channel)
		
		# set modes on admin channel /after/ joining
		if channel == self.factory.admin_channel:
			self.mode(self.factory.admin_channel, True, self.factory.admin_channel_modes)


	def names(self, channel):
		self.transport.write("NAMES %s\r\n" % channel)


	def left(self, channel):
		self.notify("[info] left %s" % channel)
		del channels[channel]

		# close the buffer for this channel
		self.factory.logger.close_buffer(channel)


	### actions the bot sees other users doing

	def userQuit(self, user, quitMessage):
		# if the user is an admin, remove them from the list
		if user in self.admins:
			self.admins.remove(user)

		# log the quit message
		for channel in self.channels:
			if self.nick_in_channel(user, channel):
				self.factory.logger.log(channel, "* %s has quit (%s)." % (user, quitMessage))
				self.names(channel)


	def userJoined(self, user, channel):
		# if this is an administrative channel, we send a welcome message
		if (channel == self.factory.admin_channel) and (user not in self.admins):
			self.notice(user,
				"Welcome to %s, %s! For help with %s, try '/MSG %s HELP' or just type '`help'." %
				(channel, user, self.nickname, self.nickname))
	
		# add user to the channel list
		self.names(channel)

		# log the JOIN
		self.factory.logger.log(channel, "%s has joined %s." % (user, channel))


	def userLeft(self, user, channel):
		# update the names list
		self.names(channel)

		# log the PART
		self.factory.logger.log(channel, "%s has left %s." % (user, channel))
		
	def modeChanged(self, user, channel, set, modes, args):
		# update the names list
		self.names(channel)
		
		nick = user.split('!')[0]
		mode_string = '+' if set else '-'
		mode_string += modes
		if len(args) > 0: mode_string += ' ' + ' '.join(str(x) for x in args)

		# log the MODE
		self.factory.logger.log(channel, "%s sets modes [%s] on %s." % (nick, mode_string, channel))
		#print user, channel, set, modes, args

	def irc_RPL_NAMREPLY(self, prefix, params):
		# parse the parameters
		target = params[0]
		chan_type = params[1]
		channel = params[2]

		names = params[-1]

		# parse the names list
		namlist = names.strip().split(' ')
		self.channels[channel] = namlist
		
	
	def userRenamed(self, oldname, newname):		
		if oldname in self.admins:
			self.admins.remove(oldname)
			self.admins.append(newname)

		# log the name change to the buffer logs
		for channel in self.channels:
			if self.nick_in_channel(oldname, channel) or self.nick_in_channel(newname, channel):
				self.factory.logger.log(channel, "* %s is now known as %s." % (oldname, newname))
				self.names(channel)

		# log the name change so we can use ALIAS
		# open the database
		alias_db = sqlite3.connect('alias.db')
		
		# create the table if it doesn't yet exist
		alias_db.execute('CREATE TABLE IF NOT EXISTS alias (id INTEGER PRIMARY KEY AUTOINCREMENT, nicklist TEXT)')
		alias_db.commit()

		# execute the query
		cursor = alias_db.execute("SELECT * FROM alias WHERE nicklist LIKE ? OR nicklist LIKE ?",
			('%"' + oldname + '"%', '%"' + newname + '"%'))

		nicklist = []

		# retreive the results
		for result in cursor:
			# parse the result row
			id = result[0]
			nicklist += json.loads(result[1])

			# remove the result from the database
			alias_db.execute("DELETE FROM alias WHERE id = ?", (id,))

		# add the new data, if necessary
		if not oldname in nicklist: nicklist.append(oldname)
		if not newname in nicklist: nicklist.append(newname)

		# strip duplicates
		nicklist = list(set(nicklist))
		entry = json.dumps(nicklist)
		
		# insert the updated entry
		alias_db.execute("INSERT INTO alias (nicklist) VALUES (?)", (entry,))
			
		# commit the changes
		alias_db.commit()
			

	def privmsg(self, user, channel, message):
		# if the private message is addressed to me, it is a command
		if channel == self.nickname:
			self.handle_command(user, message, user.split('!')[0])
			return

		# if it starts with PREFIX, it is a command
		if message.startswith(self.factory.prefix) and len(message) > 1:
			self.handle_command(user, message[1:], channel)

		# log the channel message
		self.factory.logger.log(channel, "<%s> %s" % (user.split('!')[0], message))


	def action(self, user, channel, data):
		# log the channel message
		self.factory.logger.log(channel, "* %s %s" % (user.split('!')[0], data))


	def noticed(self, user, channel, message):
		# ignore private notices
		if channel == self.nickname: return
		if (channel == "AUTH") or (channel == "*"): return # don't complain about server messages

		# log the channel notice
		self.factory.logger.log(channel, "-%s/%s- %s" % (user.split('!')[0], channel, message))

	# ------------------- Bot Command Functions ------------------- #

	def register_hooks(self):
		# register hooks
		self.hooks['PING'] = commands.ping
		self.hooks['QUIT'] = commands.quit
		self.hooks['AUTH'] = commands.auth
		self.hooks['STATUS'] = commands.status
		self.hooks['RAW'] = commands.raw
		self.hooks['LINK'] = commands.link
		self.hooks['HELP'] = commands.help
		self.hooks['ALIAS'] = commands.alias
		self.hooks['LOGOUT'] = commands.logout
		self.hooks['CLEAR'] = commands.clear


	def handle_command(self, source, command, receive):
		# split into components by ' '
		elems = command.strip().split(' ')

		# parse the command
		if len(elems) < 1: return
		cmd = elems[0].upper()
		args = elems[1:]

		if cmd in self.hooks:
			self.hooks[cmd].handle_command(self, source, command, args, receive)
		else:
			self.msg(receive, "Unrecognized Command [%s]; try HELP." % cmd)
			
	
	# ------------------- Convenience Functions ------------------- #
			
	def notify(self, message):
		# print the message to standard output
		self.factory.logger.log('greenbot', message + '\n')

		# echo the message to any admin channels
		if self.factory.admin_channel:
			self.msg(self.factory.admin_channel, message)


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


	def register_admin_channel(self, channel):
		self.join(self.factory.admin_channel)
		self.notice(self.factory.admin_channel, "*** Registering home channel [%s]" % channel)


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
