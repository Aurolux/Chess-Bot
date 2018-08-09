import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if mentions:
		user = db.get_member(mentions[0])

		team = db.get_team(user["team"])
		if team == None:
			await channel.send(mentions[0].mention+" is not in a team!")

	else:
		if len(args) > 1:
			team = db.get_team(args[1])
			if team == None:
				await channel.send('Team not found!')
		else:
			user = user

			team = db.get_team(user["team"])
			if team == None:
				await channel.send("You are not in a team!")

	if team != None:
		em = discord.Embed()
		em.title=team["name"]
		if "image" in team:
			em.set_thumbnail(url=team["image"])
		else:
			em.set_thumbnail(url="https://cdn4.iconfinder.com/data/icons/glyph-seo-icons/48/business-strategy-512.png")
		em.colour = discord.Colour(4623620)
		em.type = "rich"
		if team["bio"] != None:
			em.description = team["bio"]
		em.add_field(name="Members",value=', '.join([db.get_user(i)["name"] for i in team["members"]]),inline=False)
		em.add_field(name="Owner",value=db.get_user(team["owner"])["name"],inline=True)
		em.add_field(name="Shards",value=team["cur"],inline=True)
		em.add_field(name="Wins",value=team["wins"],inline=True)
		em.add_field(name="Losses",value=team["loss"],inline=True)
		try:
			em.add_field(name="W/G",value=str(round(team["wins"]/team["games"],2)*100)+"%",inline=True)
		except:
			em.add_field(name="W/G",value="None",inline=True)

		em.add_field(name="Draws",value=team["draws"],inline=True)
		em.add_field(name="Games",value=team["games"],inline=True)

		await channel.send(embed=em)
