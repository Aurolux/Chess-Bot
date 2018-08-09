import discord
import chess
import thedb as db
import config
from util import *

async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if message.mentions:
		try:
			g = db.get_game_recent(message.mentions[0].id)
			await channel.send('```'+str(pgn_from_moves(g["moves"]))+'```')
		except:
			await channel.send("That user hasn't played any games!")
	else:
		try:
			g = db.get_game_recent(memid)
			await channel.send('```'+str(pgn_from_moves(g["moves"]))+'```')
		except:
			await channel.send("You haven't played any games! Play one with "+prefix+"newgame [mention]")
