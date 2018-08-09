import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if args[0] == "hasbeat":

		if not len(message.raw_mentions)<2:
			try:
				user = db.get_user(message.raw_mentions[0])
				if message.raw_mentions[1] in user["unique"]:
					await channel.send("<@!"+str(message.raw_mentions[0])+"> **has** beat <@!"+str(message.raw_mentions[1])+">!")
				else:
					await channel.send("<@!"+str(message.raw_mentions[0])+"> **has not** beat <@!"+str(message.raw_mentions[1])+">!")
			except:
				await channel.send("<@!"+str(message.raw_mentions[0])+"> **has not** beat <@!"+str(message.raw_mentions[1])+">!")
		else:
			await channel.send("You must mention two people!")
