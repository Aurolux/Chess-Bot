import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	while 1:
		try:
			s = db.rand_listed_guild()["id"]
			inv = await list(bot.get_guild(s).channels)[0].create_invite(max_age=60)
			break
		except:
			db.update_guild(s, "listed", False)

	await channel.send(str(inv))
