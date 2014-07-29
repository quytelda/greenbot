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

import urllib
import json

def handle_command(bot, source, command, args, receive):
	# make sure there is a channel to join
	if len(args) < 1:
		bot.notice(receive, "ALIAS takes one parameter; syntax: ALIAS <nickname>")
		return
	
	nick = args[0]
	
	bot.msg(receive, "Generating alias list for %s..." % nick)

	url = urllib.urlopen("http://lagopus.tamalin.org/greenbot/alias.php?nick=" + urllib.quote_plus(nick))
	alias_list_json = url.readline();
	
	# output the list that was generated
	alias_list = json.loads(alias_list_json)
	if alias_list == None:
		bot.msg(receive, 'There are no nick changes logged for "%s"!' % nick)
		return
	
	alias_list_str = ', '.join(alias_list)
	bot.msg(receive, alias_list_str.encode('ascii'))
