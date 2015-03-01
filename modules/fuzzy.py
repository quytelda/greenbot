#
# modules/reload.py - Reloads bot modules during runtime
#
# Copyright (C) 2014 Quytelda <quytelda@tamalin.org>
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

def bot_HUG(bot, source, args, receive):
	do_action(bot, "hugs", receive, source.split('!')[0], args);


def bot_LICK(bot, source, args, receive):
	do_action(bot, "licks", receive, source.split('!')[0], args);


def do_action(bot, action, channel, nick, args):
	target = nick
	if len(args) > 0:
		target = args[0]

	# make sure the target is actually present
	if not bot.nick_in_channel(target, channel):
		bot.msg(channel, "But I can't find them! :(")
		return

	bot.msg(channel, "\x01ACTION %s %s\x01".encode('ascii') % (action, target))


def help_HUG(bot, source, args, receive):
	bot.msg(receive, "Syntax: HUG [victim]")
	bot.msg(receive, "Gives hugs to you or somebody else.")


def help_LICK(bot, source, args, receive):
	bot.msg(receive, "Syntax: LICK [victim]")
	bot.msg(receive, "Licks you or somebody else")
