#
# config.py - Configuration handling module for greenbot
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

import ConfigParser

config_path = 'greenbot.conf'
parser = None

def load():
	"""
	Load the configuration file into memory (but don't apply it yet).
	"""
	global parser

	parser = ConfigParser.ConfigParser()
	parser.read(config_path) 


def configure(factory):
	"""
	Apply a runtime configuration from the configuration information in memory.
	All properties loaded by this function must be mutable during runtime, as it is called by rehash.

	config.load() must be called before this function can be used.
	"""
	if parser.has_option("self", "autojoin"):
		factory.autojoin = parser.get("self", "autojoin")

	if parser.has_option("self", "admin-channel"):
		factory.admin_channel = parser.get("self", "admin-channel")
	
	if parser.has_option("self", "admin-channel-modes"):
		factory.admin_channel_modes = parser.get("self", "admin-channel-modes")

	if parser.has_option("self", "password"):
		factory.password = parser.get("self", "password")

	if parser.has_option("self", "cycle"):
		factory.cycle = parser.getint("self", "cycle")


def connection(connection):
	"""
	Loads connection details from configuration file.
	Details passed as command line args override config file params.

	config.load() must be called before this function can be used.
	"""

	if (not connection['addr']) and parser.has_option("connection", "address"):
		connection['addr'] = parser.get("connection", "address")

	if (not connection['port']) and parser.has_option("connection", "port"):
		# port must be an integer
		try: connection['port'] = parser.getint("connection", "port")
		except ValueError: print "* Invalid port in config file: %s (must be an integer)" % port

	if (not connection['ssl']) and parser.has_option("connection", "ssl"):
		# ssl is boolean (on = True, anything else = False)
		mode = parser.getint("connection", "ssl")
		if ssl.lower() == 'on': connection['ssl'] = True
		else: connection['ssl'] = False

	if (not connection['password']) and parser.has_option("connection", "password"):
		connection['password'] = parser.get("connection", "password")

	if (not connection['username']) and parser.has_option("connection", "username"):
		connection['username'] = parser.get("connection", "username")

	if (not connection['modes']) and parser.has_option("connection", "modes"):
		connection['modes'] = parser.get("connection", "modes")
		
	return connection


def rehash(factory):
	"""
	Attempts to reload and re-apply the runtime configuration without interrupting service.

	config.load() does *not* need to be called before using this function.
	"""
	self.load()
	self.configure(factory)
