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

	nick = source.split('!')[0]

	# if there is no password, it is a status query
	if len(args) < 1:
		if nick in bot.admins:
			bot.msg(receive, "You are an administrator.")
		else:
			bot.msg(receive, "You are an not logged in.")

		return
	
	pswd = args[0]
	
	# add the user to the admins list
	if pswd != bot.factory.password:
		bot.msg(receive, 'Invalid login password.')
		bot.notify('[auth] Failed login attempt from %s.' % source)
		return

	user = source.split('!')[0]
	bot.admins.append(user)

	# send a welcome reply
	bot.msg(receive, 'You are authenticated.')
	bot.notify('[auth] Successful login from %s.' % source)

	# attempt to op the person in the home channel, if there are any
	if bot.factory.admin_channel:
		bot.mode(bot.factory.admin_channel, True, 'o', user = user)
