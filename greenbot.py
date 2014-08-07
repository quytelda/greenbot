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
import json
import sqlite3

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.words.protocols import irc
from twisted.internet.task import LoopingCall
from twisted.internet import reactor, ssl

import commands.ping
import commands.quit
import commands.admins
import commands.auth
import commands.status
import commands.raw
#import commands.play
import commands.link
import commands.help
import commands.alias

class GreenBot(irc.IRCClient):

	nickname = None
	username = None
	password = None
	prefix = '`'
	quitted = False

	hooks = {}
	
	admins = []
	
	# ------------------- Connection Event Handlers ------------------- #
	
	def connectionMade(self):
		# call the parent method
		irc.IRCClient.connectionMade(self)
		
		# status message
		host = self.transport.getPeer().host
		
		# initiate the cycling log files
		log_cycle = LoopingCall(self.factory.cycle_logfile)
		log_cycle.start(self.factory.cycle)
		
		# log the new connection
		self.factory.logger.write("* Connected established with %s.\n" % host)


	def connectionLost(self, reason):
		# call parent method
		irc.IRCClient.connectionMade(self)
		
		# log the lost connection (before we close the logs :P)
		self.factory.logger.write("* Connection lost (%s).\n" % reason)
		
		# if this wasn't a manual quit, try to reconnect
		if not self.quitted:
			pass
		
		# close log file stream
		self.factory.logger.close()


	# ------------------- IRC Event Handlers ------------------- #

	def signedOn(self):
		# join the admin channel, if there is one
		if self.factory.admin_channel:
			self.join(self.factory.admin_channel)
			self.notice(self.factory.admin_channel, "*** Registered home channel [%s]." % self.factory.admin_channel)
	
		# join all the channels in the autojoin list
		if self.factory.autojoin:
			self.join(self.factory.autojoin)
	

	def joined(self, channel):
		self.notify("[info] joined %s" % channel)


	def left(self, channel):
		self.notify("[info] left %s" % channel)
		
	
	def userQuit(self, user, quitMessage):
		# if the user is an admin, remove them from the list
		if user in self.admins:
			self.admins.remove(user)
			
	
	def userRenamed(self, oldname, newname):		
		if oldname in self.admins:
			self.admins.remove(oldname)
			self.admins.append(newname)

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

		# if it starts with PREFIX, it is a command
		if message.startswith(self.prefix) and len(message) > 1:
			self.handle_command(user, message[1:], channel)


	def lineReceived(self, line):
		# keep parent functionality
		irc.IRCClient.lineReceived(self, line)
	
		# log the line
		# we'll use the local timestamp
		#t = time.localtime()
		#timestamp = time.strftime("[%H:%M:%S]", t)
		#self.factory.logger.write(timestamp + ' ' + line + '\r\n')


	# ------------------- Bot Command Functions ------------------- #

	def register_hooks(self):
		# register hooks
		self.hooks['PING'] = commands.ping
		self.hooks['QUIT'] = commands.quit
		self.hooks['ADMINS'] = commands.admins
		self.hooks['AUTH'] = commands.auth
		self.hooks['STATUS'] = commands.status
		self.hooks['RAW'] = commands.raw
		#self.hooks['PLAY'] = commands.play
		self.hooks['LINK'] = commands.link
		self.hooks['HELP'] = commands.help
		self.hooks['ALIAS'] = commands.alias


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
			self.notice(receive, "Unrecognized Command [%s]; try HELP." % cmd)
			
			
	def notify(self, message):
		# print the message to standard output
		self.factory.logger.write(message + '\n')

		# echo the message to any admin channels
		if self.factory.admin_channel:
			self.msg(self.factory.admin_channel, message)



class GreenbotFactory(ReconnectingClientFactory):

	quitted = False

	def __init__(self):
		self.logger = None
		self.alias_db = None
		self.prefix = "greenbot"
		self.autojoin = None
		self.cycle = 86400 # 24 hours
		self.admin_channel = None
		self.password = None
		self.nickname = "greenbot"
		self.username = "greenbot"
		self.srv_password = None


	def buildProtocol(self, addr):
		bot = GreenBot()
		
		bot.factory = self
		bot.nickname = self.nickname
		bot.username = self.username
		bot.password = self.srv_password

		bot.register_hooks()
		
		self.resetDelay()
		
		return bot

	def clientConnectionLost(self, connector, reason):
		if self.quitted: twisted.internet.reactor.stop()
		else:
			ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
	
	def clientConnectionFailed(self, connector, reason):
		ReconnectingClientFactory.clientConnectionLost(self, connector, reason)


	def cycle_logfile(self):
		# generate a logfile name
		logfile = self.make_logfile_name()
	
		# if there is already an open logfile stream
		if self.logger and not self.logger.closed:
			self.logger.close()
	
		# open the log file stream
		self.logger = open(logfile, 'a', 0)
		
		print "* cycled to new logfile:", logfile


	def make_logfile_name(self):
		timestamp = int(time.time())
		return "%s_%s.log" % (self.prefix, timestamp)



def start(addr, port, factory, use_ssl = False):
	if use_ssl:
		reactor.connectSSL(addr, port, factory, ssl.ClientContextFactory())
	else:
		reactor.connectTCP(addr, port, factory)
	
	# now that connection is initiated, run the reactor and get off the ground
	# basically: "Away we go!"
	reactor.run()
