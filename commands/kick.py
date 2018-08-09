import discord
import chess
import thedb as db
import config
from util import *

async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	await channel.trigger_typing()
	if mentions:
		u1 = user

		u2 = db.get_member(mentions[0])


		if u2["team"] == u1["team"]:
			team = db.get_team(u1["team"])
			if team != None and team["owner"] == u1["id"]:
				db.pull_team(team["id"], "members", u2["id"])
				db.update_user(u2["id"], "team", None)
				await channel.send('<@!'+str(u2["id"])+'>, you have been kicked from team '+team["name"]+'!')
				await bot.get_channel(config.LOGCHANNEL).send("`Kick Team: "+u2["name"]+" "+team["id"]+" "+str(guildid)+"`")
			else:
				await channel.send('You do not own a team!')
		else:
			await channel.send("That user isn't in your team!")
	else:
		await channel.send('You must mention another user!')
