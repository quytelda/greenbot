#!/usr/bin/python

#
# main.py - Primary entry point and configuration for greenbot
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
import os

import greenbot
import config

connection = {
	'addr' : None,		# host address
	'port' : None,		# connection port
	'ssl' : None,		# use SSL?
	'username' : None,	# username
	'password' : None,	# connection password
	'modes' : None		# modes to set on connection
}

runtime = {
	'verbose' : False,		# verbose mode
	'foreground' : False	# run in foreground?
}

def main(argv):
	global connection

	############### Argument Parsing ###############
	i = 1
	while i < len(argv):
		if arg_matches(argv[i], '--port', '-p'):
			i += 1
			try: connection['port'] = int(argv[i])
			except ValueError: print "* Ignoring invalid port number:", argv[i]
		elif arg_matches(argv[i], '--ssl', '-s'):
			connection['ssl'] = True
		elif arg_matches(argv[i], '--username', '-u'):
			i += 1
			connection['username'] = argv[i]
		elif arg_matches(argv[i], '--password', '-P'):
			i += 1
			connection['password'] = argv[i]
		elif arg_matches(argv[i], '--modes', '-m'):
			i += 1
			connection['modes'] = argv[i]
		elif arg_matches(argv[i], '--config', '-c'):
			i += 1
			config.config_path = argv[i]
		elif arg_matches(argv[i], '--foreground', '-f'):
			runtime['foreground'] = True
		elif arg_matches(argv[i], '--help', '-h'):
			print_help()
			return
		elif arg_matches(argv[i], '--version'):
			version()
			return
		elif (i == len(argv) - 1):
			connection['addr'] = argv[i]
		else:
			print "Unrecognized argument:", argv[i]

		i += 1

	factory = greenbot.GreenbotFactory()

	############### Configuration ###############

	config.load() # read configuration file
	connection = config.connection(connection) # connection properties
	config.configure(factory) # runtime properties

	# we need some connection information to initiate a connection
	# the default port is 6667
	# the dafault username is 'greenbot'
	if not connection['addr']:
		print "* Unable to connect to the address you didn't provide."
		return

	if not connection['port']:
		print "* No port specified; using 6667"
		port = 6667

	if not connection['username']:
		print "* No username specified; using 'greenbot'"
		username = 'greenbot'

	if connection['ssl']:
		print "* Using SSL"

	############### Real Work ###############

	if not runtime['foreground']: # this is a daemon; get forking...
		print "* Forking into background..."
		pid = os.fork()

	if runtime['foreground'] or pid == 0: # child process should run in the background
		if not runtime['foreground']: os.setsid()

		# initiate the connection to the server
		greenbot.start(connection['addr'], connection['port'], factory, connection['ssl'])



# ----------------- Other Stuff ------------------ #

def arg_matches(value, longer, shorter = None):
	return (value == longer) or (value == shorter)


def version():
	print "greenbot %s, Copyright(C) 2014 Quytelda Gaiwin (GPLv3)" % greenbot.VERSION


def print_help():
	version()
	print "\nUsage: main.py [options] [host]"
	print "-c  --config <path>        Load the config file on <path> (default: ./greenbot.conf)"
	print "-f  --foreground           Do not fork into the background"
	print "-h  --help                 Display this information"
	print "-p  --port <port>          Connect on <port> (default: 6667)"
	print "-P  --password <password>  Connect using a password"
	print "-s  --ssl                  Use SSL to connect to server"
	print "-u  --username <username>  Connect with the username <username>"
	print "    --version              Display version and copyright information"

# entry point
main(sys.argv)
