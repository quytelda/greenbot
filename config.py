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

parser = None

def load(config_path):
	"""
	Load the configuration file into memory.
	"""
	global parser

	parser = ConfigParser.ConfigParser()
	parser.read(config_path)


def get(section, option):
	if not parser.has_option(section, option): return None

	return parser.get(section, option)


def get_default(section, option, default):
	result = get(section, option)

	if result is None: return default

	return result
