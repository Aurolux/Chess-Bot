import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if mentions:
		try:
			g = db.get_game_recent(mentions[0].id)
			await channel.send('```'+str(g["fen"])+'```')
		except:
			await channel.send(mentions[0].mention+" hasn't played any games! Make one with "+prefix+"newgame [mention]")

	else:
		try:
			g = db.get_game_recent(memid)
			await channel.send('```'+str(g["fen"])+'```')
		except:
			await channel.send("You haven't played any games! Make one with "+prefix+"newgame [mention]")
