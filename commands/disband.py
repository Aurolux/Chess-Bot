import discord
import chess
import thedb as db
import config
from util import *

async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	await channel.trigger_typing()
	team = db.get_team(user["team"])
	if team != None and team["owner"] == user["id"]:
		if user["xp"] >= 800:
			db.inc_user(user["id"], "xp", -800)
			db.delete_team(team["id"])
			await channel.send('Team '+team["name"]+" has been disbanded!")
			await bot.get_channel(config.LOGCHANNEL).send("`Disband Team: "+team["id"]+" "+str(guildid)+"`")
		else:
			await channel.send("You do not have enough tokens to disband your team! 800T needed!")

	else:
		await channel.send('You do not own a team!')
