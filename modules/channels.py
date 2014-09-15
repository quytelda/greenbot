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

# ---------- IRC Command Hooks ---------- #

def irc_JOIN(bot, prefix, params):

	# update names list
	bot.names()


def irc_PART(bot, prefix, params):

	# update names list
	bot.names()


def irc_QUIT(bot, prefix, params):
	
	# update names list
	bot.names()

	
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
	bot.msg(receive, bot.channels[chan])
