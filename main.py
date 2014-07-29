#!/usr/bin/python

import sys
from twisted.internet import reactor

import greenbot

def main(argv):
	addr = argv[1]
	port = int(argv[2]) if (len(argv) > 2) else 6667
	
	print "* connecting to %s on port %d" % (addr, port)

	reactor.connectTCP(addr, port, greenbot.GreenbotFactory(addr + '.log'))
	reactor.run()

main(sys.argv)
