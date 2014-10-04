#
# modules/auth.py - Bot authentication/login over IRC module
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

def bot_AUTH(bot, source, args, receive):

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
	#if pswd != bot.factory.password:
	#	bot.msg(receive, 'Invalid login password.')
	#	bot.notify('[auth] Failed login attempt from %s.' % source)
	#	return

	user = source.split('!')[0]
	if not user in bot.admins: bot.admins.append(user)
	bot.msg(receive, "You are authenticated.")

def bot_LOGOUT(bot, source, args, receive):
	nick = source.split('!')[0]

	if not nick in bot.admins:
		bot.msg(receive, "You are not logged in.")
		return

	bot.admins.remove(nick)
	bot.msg(receive, "Succesfully logged out.")

def help_AUTH(bot, source, args, receive):
 	bot.msg(receive, "Syntax: AUTH [password]")
	bot.msg(receive, "AUTH is used to log into the bot with the bot's administration password.")
	bot.msg(receive, "If no password is supplied, the command returns the user's current login status.")

def help_LOGOUT(bot, source, args, receive):
	bot.msg(receive, "Syntax: LOGOUT")
	bot.msg(receive, "LOGOUT terminates an existing login session with the bot.")
