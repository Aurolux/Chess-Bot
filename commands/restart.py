import discord
import chess
import thedb as db
import config
import os
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if memid in config.ADMINS:

		await channel.send("Attempting to restart... Saving...")

		await channel.send("Saved...")
		if len(args) > 1:
			os.system("pm2 restart "+args[1])
		else:
			os.system("pm2 restart chess")
			await bot.change_presence(status=discord.Status.dnd)
