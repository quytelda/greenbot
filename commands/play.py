#
# commands/play.py - Simple PING command
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

	channel = None
	if source.split('!')[0] != receive:
		# this will be true if the target is a channel
		channel = receive
	elif len(args) > 0:
		channel = args[0]
	else:
		bot.msg(receive, "PLAY takes a 1 parameter. Syntax: LINK <#chan>")
		return

	lines = readn(bot.factory.filename, 15)
	
	for line in lines:
		bot.msg(receive)

def readn(file, n = 0):
	f = open(file, 'r')
	
	f.seek(0, 2) # go to end
	
	lines = []
	buff = ""
	while (f.tell() >= 2) and len(lines) < n:
		f.seek(-2, 1)
		next = f.read(1)
		
		if(next == "\n"):
			lines.insert(0, buff[::-1])
			buff = ""
		else:
			buff += next

	return lines
