#
# commands/link.py - Simple PING command
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

import urllib

def handle_command(bot, source, command, args, receive):

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

	# message back a valid URL
	bot.msg(receive, "http://lagopus.tamalin.org/viewlog.php?target=" + urllib.quote_plus(channel))
