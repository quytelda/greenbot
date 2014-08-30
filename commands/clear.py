# 
#
# commands/clear.py - CLEAR command to clear channel buffer
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

def handle_command(bot, source, command, args, receive):
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
	time.sleep(1)
	bot.factory.logger.cycle(channel)
	
	bot.msg(receive, "Finished cycling logs for %s." % channel)
	bot.notify("[info] %s cleared logs for %s. " % (source, channel))
	
	
