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

# load configuration properties
parser = ConfigParser.ConfigParser()
parser.read(config_path) 

def load_mutable_properties(factory):
		if parser.has_option("server", "password"):
			factory.srv_password = parser.get("server", "password")
		if parser.has_option("server", "username"):
			factory.username = parser.get("server", "username")
		if parser.has_option("bot", "autojoin"):
			factory.autojoin = parser.get("bot", "autojoin")
		if parser.has_option("bot", "admin-channel"):
			factory.admin_channel = parser.get("bot", "admin-channel")
		if parser.has_option("bot", "password"):
			factory.password = parser.get("bot", "password")
		if parser.has_option("bot", "cycle"):
			factory.cycle = parser.getint("bot", "cycle")

