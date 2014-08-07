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
import ConfigParser

import greenbot

def main(argv):

	# default connection settings
	config_path = 'greenbot.conf'	
	addr = None
	port = None
	password = None
	ssl = False
	foreground = False

	# parse command line arguments
	i = 0
	while i < len(argv):
		if arg_matches(argv[i], '--ssl', '-s'):
			ssl = True
		elif arg_matches(argv[i], '--port', '-p'):
			i += 1
			# parse connection port
			try: port = int(argv[i])
			except ValueError: print "* Ignoring invalid port number:", argv[i]
		elif arg_matches(argv[i], '--foreground', '-f'):
			foreground = True
		elif arg_matches(argv[i], '--config', '-c'):
			i += 1
			config_path = argv[i]
		elif (i == len(argv) - 1):
			addr = argv[i]
		else:
			print "Unrecognized argument:", argv[i]
		
		# iterate to next argument
		i += 1

	factory = greenbot.GreenbotFactory()
	
	# load configuration properties
	parser = ConfigParser.ConfigParser()
	parser.read(config_path)
	
	# parse the config file entries
	if parser.has_section("server"):
		if parser.has_option("server", "address") and (not addr):
			addr = parser.get("server", "address")
		if parser.has_option("server", "password"):
			factory.srv_password = parser.get("server", "password")
		if parser.has_option("server", "username"):
			factory.username = parser.get("server", "username")
		if parser.has_option("server", "address") and (not port):
			port = parser.getint("server", "port")
		if parser.has_option("bot", "autojoin"):
			factory.autojoin = parser.get("bot", "autojoin")
		if parser.has_option("bot", "admin-channel"):
			factory.admin_channel = parser.get("bot", "admin-channel")
		if parser.has_option("bot", "password"):
			factory.password = parser.get("bot", "password")
		if parser.has_option("bot", "cycle"):
			factory.cycle = parser.getint("bot", "cycle")

	# can't continue without a target address and port
	# the default port is 6667
	if not addr:
		print "* Unable to connect to the address you didn't provide."
		return
	if not port:
		print "* No port specified; using 6667"
		port = 6667

	# fork into the the background
	if not foreground:
		print "* Forking into background..."
		pid = os.fork()

	if foreground or pid == 0: # child process should run in the background
		if not foreground: os.setsid()

		print "* Connecting to %s on port %d" % (addr, port)
		# initiate the connection to the server
		greenbot.start(addr, port, factory, ssl)

def arg_matches(value, longer, shorter = None):
	return (value == longer) or (value == shorter)

main(sys.argv)
