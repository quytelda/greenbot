#
# commands/help.py - HELP command for outputting usage info
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

import modules
import sys

def bot_HELP(bot, source, args, receive):
	bot.msg(receive, "\x02greenbot\x02 4.0 [http://github.com/quytelda/greenbot]");

	print dir(modules)

	commands = __lookup_commands()

	# send back a list of supported commands
	bot.msg(receive, "\x02greenbot\x02 supports the following commands:")
	bot.msg(receive, (' ' * 4 + '\x02') + '\x02, \x02'.join(commands) + '\x02')
	bot.msg(receive, "To see help/usage for any command, use \x02HELP\x02 <command>");

def __lookup_commands():
	commands = []
	for module in dir(modules):
		if module.startswith('__'): continue

		print "* loading module:", module
		mod = sys.modules['modules.%s' % module]

		# find every bot command handler
		for function in dir(mod):
			if function.startswith('bot_'):
				commands.append(function.replace('bot_', ''))

	return commands
