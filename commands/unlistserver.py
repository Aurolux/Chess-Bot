import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):

	try:
		db.new_guild(guildid,guildname)
	except:
		pass
	if mem == guild.owner:
		db.update_guild(guildid,"listed",False)
		await channel.send("Server unlisted!")
	else:
		await channel.send("You are not the server owner!")
