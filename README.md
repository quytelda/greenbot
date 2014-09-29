GREENBOT
========
Greenbot is a modular Python based IRC bot that uses the Twisted framework.
Greenbot's primary feature is it's ability to implement functionality via independant, easy to write modules.  Modules are loaded at startup (though dynamic module loading is a planned feature).
A number of core modules are already present, including a useful logging module.  Modules can be added or removed by editing 'modules/__init__.py'.

# Getting Greenbot
Greenbot requires Python 2; it will not work with Python 3.
Greenbot depends on the Twisted framework, as well as pyOpenSSL.
Install using apt:
$ sudo apt-get install python-twisted pyOpenSSL

or on Arch Linux:
$ sudo pacman -S python2-twisted

# Commands
These commands are provided by the core modules.

* ALIAS <nickname>
The ALIAS command returns of nicknames changed to or from recently by <nickname>.

* AUTH [<password>]
The AUTH command is used to log into the bot with the bot's administration password.
The password is given in the config file.  If no password is supplied the command returns
the user's current login status

* CLEAR [<channel>] (NOTE: currently disabled)
The CLEAR command clears the viewable logs for the given channel in case something occurs that
should not be publicly viewable.  The log files still exist, but are cycled twice to create an
empty buffer.  A channel operator, admin, or owner may invoke this command for their channel.

* HELP
The HELP command returns a short list of commands that greenbot supports with brief descriptions.

* LINK [<channel>]
The LINK command returns an HTTP link to a webpage for viewing the bots most recent logs
of <channel>.

* LOGOUT (NOTE: currently disabled)
The LOGOUT command terminates an existing login session with the bot.

* PING
The PING command simply replies with a pong to verify that it and the caller are still connected.

* QUIT [<message>]
Causes the bot to disconnect from the IRC server and terminate the daemon.  An option quit message
may be supplied as <message>.

* PLAY <channel> (NOTE: currently disabled)
The PLAY command reads back the last few lines of history for <channel>

* RAW <message>
The RAW command sends an appropriately CR-LF padded raw IRC message to the server.
For example "RAW JOIN #channel" would cause the bot to join #channel.

* STATUS
The STATUS command prints the current status of the bot, including uptime, current channels,
and logged in administrators.