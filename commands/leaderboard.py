import discord
import chess
import thedb as db
import config
from util import *

async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):

	em = discord.Embed()
	em.title="Leaderboard"
	em.colour = discord.Colour(4623620)
	em.type = "rich"
	if len(args) > 1:
		title = args[1].title()
		if args[1].lower() == "tokens":
			unit = "xp"
			lead = db.leaderboard(8,"xp")
		elif args[1].lower() == "wins":
			unit = "wins"
			lead = db.leaderboard(8,"wins")
		elif args[1].lower() == "loss" or args[1].lower() == "losses":
			unit = "loss"
			lead = db.leaderboard(8,"loss")
		elif args[1].lower() == "games":
			unit = "games"
			lead = db.leaderboard(8,"games")
		elif args[1].lower() == "draws":
			unit = "draws"
			lead = db.leaderboard(8,"draws")
		elif args[1].lower() == "votes":
			unit = "votes"
			lead = db.leaderboard(8,"votes")
		elif args[1].lower() == "shards":
			unit = "cur"
			lead = db.leaderboard(8,"cur")

		elif args[1].lower() == "teams":
			unit = "cur"
			lead = db.leaderboardteams(8,"cur")

		elif args[1].lower() == "server":
			unit = "elo"
			lead = db.leaderboardguild(guild,"elo")

		elif args[1].lower() == "servers":
			unit = "games"
			lead = db.leaderboardguilds(8,"games")

		else:
			lead = db.leaderboard(8,"elo")
			title = "elo"
			unit = "elo"
		#if args[1].lower() == "unique":
		#	lead = db.leaderboard(5,"unique")
	else:
		lead = db.leaderboard(8,"elo")
		title = "elo"
		unit = "elo"
	em.title = title.title()
	for i,ii in zip(lead,range(len(lead))):
		em.add_field(name=str(ii+1),value=i["name"]+": "+str(i[unit]),inline=False)


	await channel.send(embed=em)
