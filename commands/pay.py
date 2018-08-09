import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if mentions:
		if len(args) > 2:
			u1 = user
			u2 = db.get_member(mentions[0])

			try:
				amount = int(args[2])
				amount = abs(amount)
				if not amount > u1["xp"]:
					if u1["id"] == u2["id"]:
						await channel.send("Paying yourself may make you feel richer, but you won't actually be any richer.")
					else:
						db.inc_user(u1["id"],"xp",-amount)
						db.inc_user(u2["id"],"xp", amount)
						await channel.send("<@!"+str(u1["id"])+">, you have paid <@!"+str(u2["id"])+"> "+str(amount)+" tokens!")
				else:
					await channel.send("You dont have enough tokens!")
			except Exception as e:
				await channel.send("You must specify a valid amount of tokens!")
		else:
			await channel.send('You must specify how many tokens you want to give!')
	else:
		await channel.send('You must specify who you want to give tokens to!')
