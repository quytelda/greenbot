#!/usr/bin/python

# 
#
# commands/quit.py - Simple QUIT command
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

import sys

from twisted.internet import reactor

def handle_command(bot, source, command, args, receive):
	
	# check if this is from the actual owner
	if not source.split('!')[0] in bot.admins:
		bot.notice(receive, "Not authorized [QUIT].")
		return
	
	message = args[0] if len(args) > 0 else "Received QUIT from %s." % source
	
	# send a quit message
	bot.quit(message)
	bot.factory.quitted = True
