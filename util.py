import math
from config import ELO_K as K
import config
import thedb as db
import random
import chess.pgn
import chess

def elo_probability(rating1, rating2):
    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))

def elo_rating(ra, rb, K):

    pb = elo_probability(ra, rb)

    pa = elo_probability(rb, ra)

    ra = int(round(ra + K * (1 - pa),0))
    rb = int(round(rb + K * (0 - pb),0))

    return (ra,rb)


def pgn_from_moves(g):
	pb = chess.pgn.Game().without_tag_roster()
	pb.headers["Site"] = config.BOTURL
	pn = pb
	for i in g:
		pn = pn.add_variation(chess.Move.from_uci(i))
	return pb

async def reward_game(winner,loser,outcome, gamedata, channel, bot):
	if gamedata["ranked"]:
		winner = db.get_user(winner)
		loser = db.get_user(loser)
		guildid = channel.guild.id

		if (outcome == "resign" and len(gamedata["moves"]) >= 10) or outcome == "checkmate":
			mon = int(loser["cur"]*0.05)
			db.inc_user(winner["id"],"wins",1)
			db.inc_user(loser["id"],"loss",1)
			db.inc_user(winner["id"],"games",1)
			db.inc_user(loser["id"],"games",1)
			db.inc_user(winner["id"],"cur",mon)
			db.inc_user(loser["id"],"cur",-mon)
			if loser["id"] not in winner["unique"]:
				db.push_user(winner["id"], "unique", loser["id"])
				db.inc_user(winner["id"],"xp",150)
			else:
				db.inc_user(winner["id"],"xp",50)

			new_elo = elo_rating(winner["elo"], loser["elo"], config.ELO_K)
			db.update_user(winner["id"], "elo", new_elo[0])
			db.update_user(loser["id"], "elo", new_elo[1])

			if winner["team"] != None and loser["team"] != None and winner["team"] != loser["team"]:
				lteam = db.get_team(loser["team"])
				mon = int(lteam["cur"]*0.05)
				db.inc_team(winner["team"], "cur", mon)
				db.inc_team(loser["team"], "cur", -mon)
				db.inc_team(winner["team"], "games", 1)
				db.inc_team(loser["team"], "games", 1)
				db.inc_team(winner["team"], "wins", 1)
				db.inc_team(loser["team"], "loss", 1)


		if outcome == "checkmate":
			await channel.send("<@!"+str(winner["id"])+"> "+random.choice(config.WINMESSAGES)+" <@!"+str(loser["id"])+">! Checkmate!")
			db.end_game(gamedata["_id"], winner["id"], loser["id"], "checkmate")
			await bot.get_channel(config.LOGCHANNEL).send("`Checkmate Game: "+winner["name"]+" "+loser["name"]+" "+str(guildid)+"`")

		if outcome == "resign":
			if len(gamedata["moves"]) >= 10:
				await channel.send("You have resigned! <@!"+str(winner["id"])+"> wins!")
				db.end_game(gamedata["_id"], winner["id"], loser["id"], "resign")
				await bot.get_channel(config.LOGCHANNEL).send("`Resign Game: "+winner["name"]+" "+loser["name"]+" "+str(guildid)+"`")

			else:
				await channel.send("You have resigned!")
				await bot.get_channel(config.LOGCHANNEL).send("`Exit Game: "+winner["name"]+" "+loser["name"]+" "+str(guildid)+"`")
				db.end_game(gamedata["_id"], None, None, "exit")


		if outcome == "draw" or outcome == "stalemate" or outcome == "accepteddraw":
			db.inc_user(winner["id"],"games",1)
			db.inc_user(loser["id"],"games",1)
			db.inc_user(winner["id"],"draws",1)
			db.inc_user(loser["id"],"draws",1)
			if outcome == "draw":
				await channel.send("Unable to Checkmate! The game is a draw!")
				db.end_game(gamedata["_id"], None, None, "draw")
			if outcome == "accepteddraw":
				await channel.send("Draw offer accepted! The game is a draw!")
				db.end_game(gamedata["_id"], None, None, "draw")
			if outcome == "stalemate":
				await channel.send("Stalemate! The game is a draw!")
				db.end_game(gamedata["_id"], None, None, "stalemate")

			if winner["team"] != None and loser["team"] != None and winner["team"] != loser["team"]:
				db.inc_team(winner["team"], "games", 1)
				db.inc_team(loser["team"], "games", 1)
				db.inc_team(winner["team"], "draws", 1)
				db.inc_team(loser["team"], "draws", 1)

		if outcome == "exit":
			await channel.send('You have exited the game!')
			db.end_game(gamedata["_id"], None, None, "exit")
			await bot.get_channel(config.LOGCHANNEL).send("`Exit Game: "+str(guildid)+"`")

		if winner["wins"] == 2:
			if not "novice" in winner["badges"]:
				db.push_user(winner["id"], "badges", "novice")
				await channel.send("<@!"+str(winner["id"])+">, congratulations! You have earned the Novice badge!")
		if winner["wins"] == 6:
			if not "expert" in winner["badges"]:
				db.push_user(winner["id"], "badges", "expert")
				await channel.send("<@!"+str(winner["id"])+">, congratulations! You have earned the Expert badge!")
		if winner["wins"] == 14:
			if not "pro" in winner["badges"]:
				db.push_user(winner["id"], "badges", "pro")
				await channel.send("<@!"+str(winner["id"])+">, congratulations! You have earned the Pro badge!")
		if winner["games"] == 24:
			if not "addicted" in winner["badges"]:
				db.push_user(winner["id"], "badges", "addicted")
				await channel.send("<@!"+str(winner["id"])+">, congratulations! You have earned the Addicted badge!")
		if loser["games"] == 24:
			if not "addicted" in winner["badges"]:
				db.push_user(loser["id"], "badges", "addicted")
				await channel.send("<@!"+str(loser["id"])+">, congratulations! You have earned the Addicted badge!")

	else:
		await channel.send("<@!"+str(loser["id"])+">, congratulations! You have earned the Addicted badge!")
		if outcome == "resign":
			await channel.send("You have resigned! The computer wins!")
			db.end_game(gamedata["_id"], "computer", loser, "resign")
		if outcome == "exit":
			await channel.send('You have exited the game!')
			db.end_game(gamedata["_id"], None, None, "exit")
		if outcome == "checkmate":
			if winner == "computer":
				await channel.send(winner+" "+random.choice(config.WINMESSAGES)+" <@!"+loser+">! Checkmate!")
				db.end_game(gamedata["_id"], "computer", loser, "checkmate")
			else:
				await channel.send("<@!"+winner+"> "+random.choice(config.WINMESSAGES)+" "+loser+" Checkmate!")
				db.end_game(gamedata["_id"], winner, "computer", "checkmate")

		if outcome == "draw":
			await channel.send("Unable to Checkmate! The game is a draw!")
			db.end_game(gamedata["_id"], None, None, "draw")
		if outcome == "stalemate":
			await channel.send("Stalemate! The game is a draw!")
			db.end_game(gamedata["_id"], None, None, "stalemate")


def rig(**kwargs):
    return "Game Rigged"
