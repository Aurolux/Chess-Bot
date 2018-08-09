import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if len(args) > 1:
		if mem == guild.owner:
			if len(args[1]) < 3:
				db.update_guild(guild.id, "prefix", args[1])
				await channel.send("Prefix set!")
			else:
				await channel.send("That prefix is too long!")
		else:
			await channel.send("You are not the server owner!")
	else:
		await channel.send("You must specify a prefix!")
