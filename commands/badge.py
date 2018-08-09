import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if len(args) > 1:
		try:
			await channel.send([key for key, value in config.BADGES.items() if value == args[1]][0].replace("-"," ").title())
		except:
			await channel.send('Badge not found!')
	else:
		await channel.send('You must specify a badge as an emoji!')
