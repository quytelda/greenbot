#
# modules/actions.py - Bot action commands
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

def bot_SAY(bot, source, args, receive):
	"""
	This is the command hook that tells the bot to send a message.
	"""
	
	nick = source.split('!')[0]
	target = None
	message = None
	
	if len(args) < 1:
		bot.msg(receive, "SAY requires more parameters. Syntax: SAY [<#channel>] <message>")
		return
	
	# check if the request is authorized
	if not nick in bot.admins:
		bot.msg(receive, 'You are not authorized.')
		return
	
	# figure out the intended target
	if (len(args) > 1) and (args[0].startswith('#')):
		target = args.pop(0)
	elif nick != receive:
		# this will be true if the target is a channel
		target = receive
	else:
		bot.msg(receive, "SAY requires a target in this context. Syntax: SAY <#channel> <message>")
		return
	
	message = ' '.join(args)
	
def bot_ACT(bot, source, args, receive):
	"""
	This is the command hook that tells the bot to send a CTCP action message.
	"""

	nick = source.split('!')[0]
	target = None
	message = None

	if len(args) < 1:
		bot.msg(receive, "SAY requires more parameters. Syntax: SAY [<#channel>] <message>")
		return

	# check if the request is authorized
	if not nick in bot.admins:
		bot.msg(receive, 'You are not authorized.')
		return

	# figure out the intended target
	if (len(args) > 1) and (args[0].startswith('#')):
		target = args.pop(0)
	elif nick != receive:
		# this will be true if the target is a channel
		target = receive
	else:
		bot.msg(receive, "SAY requires a target in this context. Syntax: SAY <#channel> <message>")
		return

	message = ' '.join(args)

	# now, actually send the message
	# ACTION messages are CTCP denoted by special unicode blocks
	# However, twisted only handles ASCII, so we have to convert
	message = 'ACTION ' + message + ''.encode('ascii')
	bot.msg(target, message)


def bot_RAW(bot, source, args, receive):
	if len(args) < 1: return
	
	# check if this is from the actual owner
	if not source.split('!')[0] in bot.admins:
		bot.msg(receive, "You are not authorized.")
		return
	
	message = ' '.join(args)

	bot.transport.write(message + '\r\n')
