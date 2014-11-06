#
# modules/log.py - Logging functionality for greenbot
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

import os, time, urllib

from twisted.internet.task import LoopingCall

import config
import modules

logger = None

class BufferLogger:

	def __init__(self, prefix):
		self.prefix = prefix
		self.buffers = {}

		# if the log directory doesn't exist, create it
		if not os.path.isdir(prefix): os.mkdir(prefix)

		cycle_task = LoopingCall(self.cycle_all)

		duration = 0;
		try:
			duration = config.get_default("log", "cycle-duration", 3600*24)
		except ValueError:
			duration = 3600*24;

		cycle_task.start(duration);


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
		if not buffer in self.buffers or self.buffers[buffer].closed:
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

# ---------- Event Logging Hooks ---------- #

def irc_RPL_WELCOME(bot, prefix, params):
	"""
	Begin logging when the bot officially joins the network.
	"""
	global logger
	if logger is None:
		logger = BufferLogger(config.get_default("log", "dir", "greenbot"))


def irc_JOIN(bot, prefix, params):
	"""
	Open a buffer for logging this channel.
	"""
	nick = prefix.split('!')[0]
	channel = params[0]

	# when the bot joins a channel
	# it should open a new buffer for it
	if nick == bot.nickname:
		logger.open_buffer(channel)

	# log the JOIN
	logger.log(channel, "%s has joined %s." % (nick, channel))


def irc_PART(bot, prefix, params):
	"""
	Close the buffer for this channel.
	"""
	nick = prefix.split('!')[0]
	channel = params[0]

	# log the PART
	logger.log(channel, "%s has left %s." % (nick, channel))

	# when the bot joins a channel
	# it should open a new buffer for it
	if nick == bot.nickname:
		logger.close_buffer(channel)


def irc_KICK(bot, prefix, params):
	"""
	Close the buffer for this channel.
	"""
	nick = prefix.split('!')[0]
	channel = params[0]

	# log the KICK
	logger.log(channel, "%s was kicked from %s." % (nick, channel))

	# when the bot joins a channel
	# it should open a new buffer for it
	if nick == bot.nickname:
		logger.close_buffer(channel)


def irc_NICK(bot, prefix, params):
	"""
	Close the buffer for this channel.
	"""
	oldnick = prefix.split('!')[0]
	newnick = params[0]

	# log the NICK
	for channel in bot.channels:
		if bot.nick_in_channel(oldnick, channel):
			logger.log(channel, "%s is now known as %s." % (oldnick, newnick))
			bot.names(channel)


def irc_MODE(bot, prefix, params):
	"""
	Close the buffer for this channel.
	"""
	nick = prefix.split('!')[0]
	target = params[0]
	modes = ' '.join(params[1:])

	# ignore modes set on the bot (user modes)
	if(target == bot.nickname): return

	# log the MODE
	logger.log(target, "%s sets modes [%s]" % (nick, modes))
	bot.names(target)


def irc_QUIT(bot, prefix, params):
	"""
	Close all buffers on quit.
	"""
	nick = prefix.split('!')[0]
	message = params[0]

	# log the QUIT
	for channel in bot.channels:
		if bot.nick_in_channel(nick, channel):
			logger.log(channel, "* %s has quit (%s)." % (nick, message))
			bot.names(channel)

	# when the bot quits
	# it should close all it's buffers
	if nick == bot.nickname:
		modules.channels.notify(bot, "info", "* QUIT received, closing open connections.")
		logger.close_all()


def irc_PRIVMSG(bot, prefix, params):
	nick = prefix.split('!')[0]
	channel = params[0]
	message = params[1]

	# ignore private message
	if channel == bot.nickname: return

	# log the channel message
	logger.log(channel, "<%s> %s" % (nick, message))


def irc_NOTICE(bot, prefix, params):
	# sometimes we get notices before we are ready to start logging
	# TODO: maybe add dependancies to modules?
	# or make the logger just drop log()s until some init() is called
	if logger is None: return

	nick = prefix.split('!')[0]
	channel = params[0]
	message = params[1]

	# ignore private notices
	if channel == bot.nickname: return

	# log the channel notice
	logger.log(channel, "-%s/%s- %s" % (nick, channel, message))

# ---------- Bot Command Hooks ---------- #

def bot_LINK(bot, source, args, receive):

	# determine the channel name
	channel = None
	if len(args) > 0:
		channel = args[0]
	elif source.split('!')[0] != receive:
		# this will be true if the target is a channel
		channel = receive
	else:
		bot.msg(receive, "LINK takes a 1 parameter. Syntax: LINK <#chan>")
		return

	# we must have been in that channel recently
	if not channel in bot.channels:
		bot.msg(receive, "The logs for %s are unavailable." % channel)
		return

	# message back a URL
	base_url = config.get("log", "base-url")
	if base_url is not None:
		bot.msg(receive, base_url + urllib.quote_plus(channel))


def bot_CLEAR(bot, source, args, receive):
	nick = source.split('!')[0]

	# determine the channel name
	channel = None
	if len(args) > 0:
		channel = args[0]
	elif nick != receive:
		# this will be true if the target is a channel
		channel = receive
	else:
		bot.msg(receive, "CLEAR takes a 1 parameter. Syntax: CLEAR <#chan>")
		return

	# channel must exist
	if not channel in bot.channels:
		bot.msg(receive, "There is no open buffer for %s because I have not joined." % channel)
		return

	# must be a chanop at least
	if (not bot.privileged_in_channel(nick, channel)) and (not nick in bot.admins):
		bot.msg(receive, "You are not sufficient privileges." % channel)
		return

	# cycle the channel twice now
	bot.factory.logger.cycle(channel)
	time.sleep(0.5)
	bot.factory.logger.cycle(channel)

	bot.msg(receive, "Finished cycling logs for %s." % channel)
	bot.notify("[info] %s cleared logs for %s. " % (nick, channel))


def help_LINK(bot, source, args, receive):
	bot.msg(receive, "Syntax: LINK <channel>")
	bot.msg(receive, "LINK returns a link to the logs for the <channel>.")


def help_CLEAR(bot, source, args, receive):
	bot.msg(receive, "Syntax: CLEAR <channel>")
	bot.msg(receive, "CLEAR cycles the logs for <channel>.")
