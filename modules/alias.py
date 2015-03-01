#
# modules/alias.py - ALIAS tracks and logs nick changes
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

import json
import sqlite3

def irc_NICK(bot, prefix, params):

	oldname = prefix.split('!')[0]
	newname = params[0]

	# log the name change so we can use ALIAS
	# open the database
	alias_db = sqlite3.connect('greenbot.db')

	# create the table if it doesn't yet exist
	alias_db.execute('CREATE TABLE IF NOT EXISTS alias (id INTEGER PRIMARY KEY AUTOINCREMENT, nicklist TEXT)')
	alias_db.commit()

	# execute the query
	cursor = alias_db.execute("SELECT * FROM alias WHERE nicklist LIKE ? OR nicklist LIKE ?",
		('%"' + oldname + '"%', '%"' + newname + '"%'))

	nicklist = []

	# retreive the results
	for result in cursor:
		# parse the result row
		id = result[0]
		nicklist += json.loads(result[1])

		# remove the result from the database
		alias_db.execute("DELETE FROM alias WHERE id = ?", (id,))

	# add the new data, if necessary
	if not oldname in nicklist: nicklist.append(oldname)
	if not newname in nicklist: nicklist.append(newname)

	# strip duplicates
	nicklist = list(set(nicklist))
	entry = json.dumps(nicklist)

	# insert the updated entry
	alias_db.execute("INSERT INTO alias (nicklist) VALUES (?)", (entry,))

	# commit the changes
	alias_db.commit()
	alias_db.close()

def bot_ALIAS(bot, source, args, receive):

	if len(args) < 1:
		bot.notice(receive, "ALIAS takes one parameter; syntax: ALIAS <nickname>")
		return

	target = args[0]

	# only admins can use wildcards
	if (not source.split('!')[0] in bot.admins) and ('%' in target):
		bot.msg(receive, 'You are not authorized.')
		return

	try:
		# connect to the database
		alias_db = sqlite3.connect('greenbot.db')

		# query for pertinent records
		cursor = alias_db.execute('SELECT * FROM alias WHERE nicklist LIKE ?', ('%"'+target+'"%',))
		result = cursor.fetchone()
		alias_db.close()

		# send back the results (formatted nicely)
		if result:
			nicklist = json.loads(result[1])
			message = (', '.join(nicklist)).encode('ascii')
			bot.msg(receive, message)
		else:
			bot.msg(receive, "No nick changes logged for %s." % target)

	except sqlite3.Error, e:
		print "SQLite Error", e

def help_ALIAS(bot, source, args, receive):
	bot.msg(receive, "Syntax: ALIAS <nickname>")
	bot.msg(receive, "ALIAS returns a list of nicknames changed to or from recently by <nickname>.")
