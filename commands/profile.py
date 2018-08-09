import discord
import chess
import thedb as db
import config
from util import *

async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):

	if mentions:
		member = await bot.get_user_info(mentions[0].id)
		user = db.get_member(mentions[0])

	else:
		member = await bot.get_user_info(memid)
		user = user


	em = discord.Embed()
	em.title=member.name
	em.set_thumbnail(url=member.avatar_url)
	em.colour = discord.Colour(user["color"])
	em.type = "rich"
	if user["bio"] !=None:
		em.description = user["bio"]
	em.add_field(name="Shards",value=user["cur"],inline=True)
	em.add_field(name="Elo",value=user["elo"],inline=True)
	em.add_field(name="Tokens",value=user["xp"],inline=True)
	em.add_field(name="Wins",value=user["wins"],inline=True)
	em.add_field(name="Losses",value=user["loss"],inline=True)
	try:
		em.add_field(name="W/G",value=str(round(user["wins"]/user["games"],2)*100)+"%",inline=True)
	except:
		em.add_field(name="W/G",value="None",inline=True)
	em.add_field(name="Draws",value=user["draws"],inline=True)
	em.add_field(name="Games",value=user["games"],inline=True)
	em.add_field(name="Votes",value=user["votes"],inline=True)
	if user["team"] != None:
		team = db.get_team(user["team"])
		em.add_field(name="Team",value=team["name"],inline=True)
	else:
		em.add_field(name="Team",value="None",inline=True)

	if len(user["badges"]) > 0:
		em.add_field(name="Badges",value=' '.join([config.BADGES[i] for i in user["badges"]]),inline=True)
	else:
		em.add_field(name="Badges",value="None",inline=True)
	await channel.send(embed=em)
