#
# commands/channels.py - Bot channel management command
# This module is essential for greenbot.  Do not remove it or things won't work!
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

import config

admin_channel = None

# ---------- IRC Command Hooks ---------- #

def irc_RPL_WELCOME(bot, prefix, params):
	global admin_channel
	admin_channel = config.get("bot", "admin-channel")
	autojoin = config.get("bot", "autojoin")

	# autojoin channels
	if autojoin is not None:
		bot.join(autojoin);
	if admin_channel is not None:
		bot.join(admin_channel)


def irc_JOIN(bot, prefix, params):

	# update names list
	chan = params[0]
	nick = prefix.split('!')[0]
	bot.names(chan)

	# when the bot joins a channel
	if nick == bot.nickname:
		notify(bot, "info", "Joined %s" % chan)

	# administrative channel greetings
	admin_chan_greeting = config.get("bot", "admin-chan-greeting")

	if chan == admin_channel:
		if nick == bot.nickname:
			bot.notice(chan, "*** Registered home channel (%s) ***" % chan)
		elif admin_chan_greeting is not None:
			bot.notice(nick, admin_chan_greeting);


def irc_PART(bot, prefix, params):

	# update names list
	chan = params[0]
	nick = prefix.split('!')[0]
	bot.names(chan)

	# on self join
	if nick == bot.nickname:
		notify(bot, "info", "Left %s" % chan)


def irc_QUIT(bot, prefix, params):

	# update names list
	chan = params[0]
	bot.names(chan)


def irc_MODE(bot, prefix, params):

	# update names list
	chan = params[0]
	bot.names(chan)


def irc_RPL_NAMREPLY(bot, prefix, params):
	# parse the parameters
	target = params[0]
	chan_type = params[1]
	channel = params[2]

	names = params[-1]

	# parse the names list
	namlist = names.strip().split(' ')
	bot.channels[channel] = namlist



# ---------- Bot Command Hooks ---------- #

def bot_JOIN(bot, source, args, receive):

	if len(args) < 1:
		bot.msg(receive, 'JOIN takes one parameter!')
		return

	nick = source.split('!')[0]
	chan = args[0]

	# Is the caller authorized?
	if not nick in bot.admins:
		bot.msg(receive, 'You are not authorized.')
		return

	# send join request
	bot.join(chan)


def bot_PART(bot, source, args, receive):

	if len(args) < 1:
		bot.msg(receive, 'PART takes one parameter!')
		return

	nick = source.split('!')[0]
	chan = args[0]

	# Is the caller authorized?
	if not nick in bot.admins:
		bot.msg(receive, 'You are not authorized.')
		return

	# send part request
	bot.part(chan)


def bot_QUIT(bot, source, args, receive):

	nick = source.split('!')[0]
	reason = args[0] if len(args) > 0 else "Received QUIT from %s" % nick

	# Is the caller authorized?
	if not nick in bot.admins:
		bot.msg(receive, 'You are not authorized.')
		return

	# send quit notice
	bot.quit(reason)
	bot.factory.quitted = True


def bot_DNAM(bot, source, args, receive):
	if len(args) < 1:
		bot.msg(receive, 'DNAM takes one parameter!')
		return

	nick = source.split('!')[0]
	chan = args[0]

	# Is the caller authorized?
	if not nick in bot.admins:
		bot.msg(receive, 'You are not authorized.')
		return

	if not chan in bot.channels:
		bot.msg(receive, 'Bot is not in %s.' % chan)
		return

	# dump names list
	bot.msg(receive, str(bot.channels[chan]))


def help_JOIN(bot, source, args, receive):
	bot.msg(receive, "Syntax: JOIN <channel>")
	bot.msg(receive, "JOIN instructs the bot to attempt joining <channel>.")


def help_PART(bot, source, args, receive):
	bot.msg(receive, "Syntax: PART <channel>")
	bot.msg(receive, "PART instructs the bot to attempt parting <channel>.")


def help_QUIT(bot, source, args, receive):
	bot.msg(receive, "Syntax: QUIT [quit message]")
	bot.msg(receive, "QUIT instructs the bot to quit (disconnect from) the network.")
	bot.msg(receive, "An optional quit message may be provided.")


def help_DNAM(bot, source, args, receive):
	bot.msg(receive, "Syntax: DNAM <channel>")
	bot.msg(receive, "DNAM dumps the bot's NAMES list for <channel>; useful for debugging.")


def notify(bot, mtype, message):
	if admin_channel is not None:
		bot.msg(admin_channel, "[%s] %s" % (mtype, message))

	print "* [%s] %s" % (mtype, message)
