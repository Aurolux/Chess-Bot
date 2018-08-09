import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	u = user

	if u["team"] != None:
		team = db.get_team(u["team"])
		if u["id"] == team["owner"]:
			await channel.send("As the team owner, you may not leave.")
		else:
			db.update_user(u["id"], "team", None)
			db.pull_team(u["team"], "members", u["id"])
			await channel.send("You have left "+team["name"]+"!")
			await bot.get_channel(config.LOGCHANNEL).send("`Leave Team: "+u["name"]+" "+team["id"]+" "+str(guildid)+"`")
	else:
		await channel.send("You are not in a team!")
