import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if game != None:
		await reward_game(ids[not ids.index(memid)], memid, "exit", gamedata,channel,bot)
	else:
		await channel.send('You are not in a game! Make one with '+prefix+'newgame [mention]')
