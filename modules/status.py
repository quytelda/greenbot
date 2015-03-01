#
# modules/status.py - Simple commands to check status and uptime
#
# Copyright (C) 2014 Quytelda <quytelda@tamalin.org>
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

import datetime
import time

start_time = 0

def bot_PING(bot, source, args, receive):
	bot.msg(receive, "pong")


def bot_PONG(bot, source, args, receive):
	bot.msg(receive, "ping")


def irc_RPL_WELCOME(bot, prefix, params):
	global start_time

	start_time = time.time()


def bot_STATUS(bot, source, args, receive):

	# calculate uptime
	elapsed = time.time() - start_time
	uptime = datetime.timedelta(seconds = int(elapsed))

	bot.msg(receive, "Uptime: %s" % uptime)
	bot.msg(receive, "Channels (%d): %s" % (len(bot.channels), bot.channels.keys()))

	if source.split('!')[0] in bot.admins:
		bot.msg(receive, "Administrators (%d): %s" % (len(bot.admins), bot.admins))


def help_PING(bot, source, args, receive):
	bot.msg(receive, "Syntax: PING (or PONG)")
	bot.msg(receive, "PING and PONG reply with a ping/pong to verify that both the bot and the caller are still connected.")


def help_PONG(bot, source, args, receive):
	help_PING(bot, source, args, receive)


def help_STATUS(bot, source, args, receive):
	bot.msg(receive, "Syntax: STATUS")
	bot.msg(receive, "Outputs information about the status of the bot, including uptime, current channels, and logged in administrators.")
