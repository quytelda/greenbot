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

def handle_command(bot, source, command, args, receive):
	if len(args) < 1: return
	
	pswd = args[0]
	
	# add the user to the admins list
	if pswd != 'password':
		bot.msg(receive, 'Invalid login password.')
		return

	if source in bot.admins: return

	bot.admins.append(source.split('!')[0])

	# send a welcome replay
	bot.msg(receive, 'You are authenticated.')
