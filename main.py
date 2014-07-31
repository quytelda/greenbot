#!/usr/bin/python

import sys
import ConfigParser

from twisted.internet import reactor

import greenbot

def main(argv):
	config_path = 'greenbot.conf'
	addr = argv[1]
	port = int(argv[2]) if (len(argv) > 2) else 6667
	
	print "* connecting to %s on port %d" % (addr, port)
	
	factory = greenbot.GreenbotFactory()
	
	# load configuration properties
	parser = ConfigParser.ConfigParser()
	parser.read(config_path)
	
	# parse the config file entries
	if parser.has_section("server"):
		if parser.has_option("server", "address"):
			addr = parser.get("server", "address")
		if parser.has_option("server", "address"):
			port = parser.getint("server", "port")
		if parser.has_option("bot", "autojoin"):
			factory.autojoin = parser.get("bot", "autojoin")
		if parser.has_option("bot", "admin-channel"):
			factory.admin_channel = parser.get("bot", "admin-channel")
		if parser.has_option("bot", "password"):
			factory.password = parser.get("bot", "password")
		if parser.has_option("bot", "cycle"):
			factory.cycle = parser.getint("bot", "cycle")

	# initiate the connection to the server
	reactor.connectTCP(addr, port, factory)
	reactor.run()

main(sys.argv)
