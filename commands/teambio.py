import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if len(args) > 1:
		u = user
		team = db.get_team(u["team"])
		if team != None and team["owner"] == u["id"]:
			bio = ' '.join(args[1:])
			if len(bio)<=250:
				db.update_team(team["id"],"bio",bio)
				await channel.send("Team bio set!")
			else:
				await channel.send('Your bio is too long! (Over 250 characters)')

		else:
			await channel.send('You do not own a team!')
	else:
		await channel.send('You must specify a bio!')
