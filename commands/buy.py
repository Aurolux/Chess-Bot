import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if len(args) > 1:
		u = user


		if args[1] in config.prices.keys():
			item = config.prices[args[1]]
			if item[0] > u["xp"]:
				await channel.send("You do not have enough tokens to buy that!")
			else:
				if item[1] == "badge":
					if item[2] in u["badges"]:
						await channel.send("You already have that badge!")
					else:
						db.push_user(u["id"],"badges",item[2])
						db.inc_user(u["id"],"xp", -item[0])
						await channel.send("You bought "+args[1]+" for "+str(item[0])+"T!")


				elif item[1] == "item":
					db.push_user(u["id"],"inv",item[2])
					db.inc_user(u["id"],"xp", -item[0])
					await channel.send("You bought "+args[1]+" for "+str(item[0])+"T!")

				await bot.get_channel(config.LOGCHANNEL).send("`Item Bought: "+item[2]+" "+str(item[0])+" "+u["name"]+" "+str(guildid)+"`")

		else:
			await channel.send("That is not a valid item ID!")
	else:
		await channel.send("You must specify the ID of an item to buy! See `"+prefix+"shop`")
