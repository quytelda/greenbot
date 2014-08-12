#!/usr/bin/python

# 
#
# commands/ping.py - Simple PING command
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
import datetime

def handle_command(bot, source, command, args, receive):
	
	# calculate uptime
	elapsed = time.time() - bot.start_time
	uptime = datetime.timedelta(seconds = int(elapsed))

	bot.msg(receive, "Uptime: %s" % uptime)
	bot.msg(receive, "Channels (%d): %s" % (len(bot.channels), bot.channels.keys()))
	bot.msg(receive, "Administrators (%d): %s" % (len(bot.admins), bot.admins))
