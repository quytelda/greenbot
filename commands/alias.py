#
# commands/help.py - ALIAS command for outputting usage info
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

import json
import sqlite3

def handle_command(bot, source, command, args, receive):
	# make sure there is a channel to join
	if len(args) < 1:
		bot.notice(receive, "ALIAS takes one parameter; syntax: ALIAS <nickname>")
		return
	
	target = args[0]
	if '%' in target:
		bot.notify('[warn] Suspicious SQL query by %s (%s).' % (source, target))
		return
	
	try:
		# connect to the database
		alias_db = sqlite3.connect('alias.db')

		# query for pertinent records
		cursor = alias_db.execute('SELECT * FROM alias WHERE nicklist LIKE ?', ('%"'+target+'"%',))
		result = cursor.fetchone()
		
		# send back the results (formatted nicely)
		if result:
			nicklist = json.loads(result[1])
			message = (', '.join(nicklist)).encode('ascii')
			bot.msg(receive, message)
		else:
			bot.msg(receive, "No nick changes logged for %s." % target)
		
	except sqlite3.Error, e:
		print "SQLite Error", e
