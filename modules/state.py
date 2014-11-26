#
# modules/reload.py - Reloads bot modules during runtime
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
import config
import main

import modules.channels

def bot_RELOAD(bot, source, args, receive):
	if len(args) < 1: return

	nick = source.split('!')[0];

	# check if this is from the actual owner
	if not nick in bot.admins:
		bot.msg(receive, "You are not authorized.")
		return

	# if no args, complain
	if len(args) < 1:
		bot.msg("RELOAD requires at least one parameter.")
		return

	module_name = 'modules.' + args[0]

	if not module_name in sys.modules:
		bot.msg(receive, "No module '%s' is loaded." % module_name);
		return
	module = sys.modules[module_name]

	# skip if the module has been marked as reload disabled
	if hasattr(module, "NO_RELOAD"):
		return

	modules.channels.notify(bot, "info", "Module '%s' reloaded by %s" % (args[0], nick))
	reload(module)


def bot_REHASH(bot, source, args, receive):

	nick = source.split('!')[0];

	# check if this is from the actual owner
	if not nick in bot.admins:
		bot.msg(receive, "You are not authorized.")
		return

	config.load(main.runtime['config'])

	# announce rehash to admin channel
	modules.channels.notify(bot, "info", "Configuration rehashed by %s" % nick);


def help_RELOAD(bot, source, args, receive):
	bot.msg(receive, "Syntax: RELOAD <module name>")
	bot.msg(receive, "Reloads a module during runtime.")
	bot.msg(receive, "All data associated with that module may be lost.")

def help_REHASH(bot, source, args, receive):
	bot.msg(receive, "Syntax: REHASH")
	bot.msg(receive, "Reload configuration during runtime.")
