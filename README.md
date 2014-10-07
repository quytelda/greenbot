GREENBOT
========
Greenbot is a modular Python based IRC bot that uses the Twisted framework.
Greenbot's primary feature is it's ability to implement functionality via independant, easy to write modules.  Modules are loaded at startup (though dynamic module loading is a planned feature).
A number of core modules are already present, including a useful logging module.  Modules can be added or removed by editing 'modules/__init__.py'.

The current stable version is 3.1 (https://github.com/quytelda/greenbot/tree/v3.1)

<<<<<<< HEAD
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
=======
## Getting Greenbot
* Greenbot needs Python 2.7+ (it doesn't work with Python 3, currently)
* Greenbot depends on the Twisted framework and pyOpenSSL.

Install dependancies using apt:
		`$ sudo apt-get install python-twisted pyOpenSSL`


## Command-Line Options
greenbot can be launched with the following usage:
```
Usage: greenbot [options] [URL]
--port     -p [port]		  Port number to connect on (must be an integer)
--ssl      -s 				  Connect using SSL
--password -P [password]	  Connect to the server with this password
--config   -c [config]		  Use a different configuration file at the given path.
--username -u [username]	  Connect with the given username
--nickname -n [nickname]	  Connect with the given nickname

--foreground -f				  Do not fork into the background
--version    -v				  Print version information
--help		 -h				  Print help information
```

## Configuration Options
greenbot's reads configuration files of traditional INI format, located by default in `./greenbot.conf`.  Here is an introduction to the INI format: http://en.wikipedia.org/wiki/INI_file#Format

Configuration of the greenbot core is divided into two sections: `[server]` and `[bot]`
`[server]` contains configuration relevent to the IRC server (such as the address, port, and password), while `[bot]` contains configuration relative to the bot (such as nickname, username, and administrative password).  Here is an example base configuration file:
```
; server/connection details section
[server]
address: irc.example.org		; IRC server address
port: 6667						; IRC server port (defaults to 6667)

; bot properties section
[bot]
nickname: greenbot		; nickname to use when connecting
username: greenbot		; username to use when connecting
password: password		; password for authenticating to the bot (per the `auth` module)
```

## Adding Modules
To add a module to greenbot, put the .py file in the `modules` directory.  Then edit `modules/__init__.py` and add the new modules name to the `__all__` list.  Assuming everything works, the module will be loaded at start-time.
>>>>>>> 4d37d75... Update header styles on README.md
