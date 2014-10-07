GREENBOT
========
Greenbot is a modular Python based IRC bot that uses the Twisted framework.
Greenbot's primary feature is it's ability to implement functionality via independant, easy to write modules.  Modules are loaded at startup, and can be reloaded during runtime (dynamic module loading is a planned feature).
A number of core modules are already present, including several useful logging modules.  Modules can be added or removed by editing 'modules/__init__.py'.

The current stable version is v3.1 (https://github.com/quytelda/greenbot/tree/v3.1)

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