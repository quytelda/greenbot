#
# commands/help.py - HELP command for outputting usage info
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

def handle_command(bot, source, command, args, receive):
	bot.msg(receive, "GreenBot 3.2 (C) 2014 Quytelda Gaiwin")
	bot.msg(receive, "GreenBot logs all channel traffic it receives from the IRC server; A web extension allows others to view recent entries into the log (within ~48hrs).")
	bot.msg(receive, "\x02COMMANDS:\x02 (commands marked * are privileged):")
	bot.msg(receive, "\x02LINK <#chan>\x02  Returns an HTTP link to the viewable channel log for the channel <#chan>.")
	bot.msg(receive, "\x02ALIAS <nickname>\x02  Attempts to list all nicks that have recently been used by <nickname>.")
	bot.msg(receive, "\x02CLEAR* <#chan>\x02  Cycles the logs for <#chan> twice to remove the current contents (must be at least chanop).")
	bot.msg(receive, "Other commands: PING, RAW*, AUTH*, LOGOUT*, QUIT*, STATUS")
	bot.msg(receive, "\x02*** END OF HELP ***\x02")
