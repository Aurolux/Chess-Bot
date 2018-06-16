from __future__ import print_function
import chess
import re, sys, time
from itertools import count
from collections import OrderedDict, namedtuple
import discord
from discord.ext import commands
import asyncio
from boardgen import *
import json
import os
from chess import Board
import thedb as db
import datetime
import chess.pgn
import chess.variant
import chess.uci
import aiohttp
import traceback
import random
import math
import config
from collections import Counter



from bson.objectid import ObjectId

engine = chess.uci.popen_engine("stockfish")
analyze = chess.uci.InfoHandler()
engine.info_handlers.append(analyze)


async def reward_game(winner,loser,outcome, gamedata, channel):
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


bot = discord.AutoShardedClient()
board = chess.Board()

def pgn_from_moves(g):
	pb = chess.pgn.Game().without_tag_roster()
	pb.headers["Site"] = "https://discordbots.org/bot/366770566331629579"
	pn = pb
	for i in g:
		pn = pn.add_variation(chess.Move.from_uci(i))
	return pb

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name=str(db.games.find().count())+" games!"),status=discord.Status.online)

@bot.event
async def on_guild_join(guild):
	db.new_guild(guild.id,guild.name)
	await bot.get_channel(config.LOGCHANNEL).send("`Join guild: "+guild.name+"`")
	try:
		payload = {"server_count"  : len(bot.guilds)}
		async with aiohttp.ClientSession() as aioclient:
				await aioclient.post(config.DBLURL, data=payload, headers=config.DBLHEADERS)

	except:
		pass

@bot.event
async def on_guild_remove(guild):
	await bot.get_channel(config.LOGCHANNEL).send("`Leave guild: "+guild.name+"`")
	try:
		payload = {"server_count"  : len(bot.guilds)}
		async with aiohttp.ClientSession() as aioclient:
				await aioclient.post(config.DBLURL, data=payload, headers=config.DBLHEADERS)

	except:
		pass

@bot.event
async def on_member_update(before, after):
	user = db.get_member(after)
	if str(after) != user["name"]:
		db.update_user(user["id"],"name",str(after))

@bot.event
async def on_guild_update(before, after):
	guild = db.get_guild(after.id)
	if after.name != guild["name"]:
		db.update_guild(guild["id"],"name",after.name)



@bot.event
async def on_message(message):
	try:
		try:
			dbguild = db.retrieve_guild(message.guild)
			prefix = dbguild["prefix"]
		except:
			prefix = "|"
		if str(message.author.id) != config.ID and not message.author.bot and message.content.startswith(prefix):
			msg = message
			msgcontent = msg.content
			mem = msg.author
			memid = mem.id
			user = db.get_member(mem)
			if user["blacklisted"]:
				return
			guild = msg.guild
			try:
				guildid = guild.id
				guildname = guild.name
				guildowner = guild.owner
			except:
				pass
			channel = msg.channel
			mentions = msg.mentions

			gamedata = db.get_game(memid)
			game = None
			if gamedata != None:
				game = chess.Board(fen=gamedata["fen"])
				ids = (gamedata["1"], gamedata["2"])

			args = ' '.join(msgcontent.strip(prefix).split()).split()
			try:
				command = args[0]
			except:
				return

			if command in ["move", "m"] or command in ["go", "g"]:
				await channel.trigger_typing()
				if game != None:
					if memid != ids[game.turn]:
						if len(args) > 1:
							movecoord = args[1]

							if command in ["move", "m"]:
								try:
									move = chess.Move.from_uci(movecoord)
									if move in game.legal_moves:
										game.push(move)

										await channel.send(file=discord.File(open(makeboard(game),'rb')), content="<@!"+str(ids[not game.turn])+">")
										db.add_move(gamedata["_id"], move.uci(), game.fen())

									else:
										await channel.send("That move is illegal!")
								except Exception as E:
									await channel.send("That move is invalid! Try something like: a2a4")

							elif command in ["go", "g"]:
								try:
									move = game.parse_san(movecoord)
									if move in game.legal_moves:
										game.push(move)

										await channel.send(file=discord.File(open(makeboard(game), 'rb')), content="<@!"+str(ids[not game.turn])+">")
										db.add_move(gamedata["_id"], move.uci(), game.fen())

									else:
										await channel.send("That move is illegal!")
								except Exception as E:
									await channel.send("That move is invalid! Try something like: a4")


							if game.is_checkmate():
								if gamedata["ranked"]:
									await reward_game(memid, ids[not ids.index(memid)], "checkmate", gamedata,channel)
								else:
									await reward_game(memid, "computer", "checkmate", gamedata,channel)

							if game.is_stalemate() or game.is_fivefold_repetition() or game.is_seventyfive_moves():
								if gamedata["ranked"]:
									await reward_game(memid, ids[not ids.index(memid)], "stalemate", gamedata,channel)
								else:
									await reward_game(None, None, "stalemate", gamedata,channel)

							if game.is_insufficient_material():
								if gamedata["ranked"]:
									await reward_game(memid, ids[not ids.index(memid)], "draw", gamedata,channel)
								else:
									await reward_game(None, None, "draw", gamedata,channel)

						else:
							await channel.send("You must specify what move you wish to make!")
					else:
						await channel.send("It is not your turn!")

					if game.is_check() and not game.is_checkmate():
						await channel.send('**Check!**')

				else:
					await channel.send('You are not in a game! Make one with '+prefix+'newgame [mention]')



			if command in ["analyze", "an"]:
				if game != None:
					await channel.trigger_typing()
					engine.position(game)
					engine.go(depth=20)
					advantage = analyze.info["score"][1].cp
					if not advantage==None:
						if not game.turn:
							advantage = advantage*-1
						await channel.send("```css\nWhite Points: "
						+str(39-sum([1 if i=="p" else 3 if i=="n" else 3 if i =="b" else 5 if i == "r" else 9 if i == "q" else 0 for i in str(game).replace("\n", " ").split(" ")]))
						+"\nBlack Points: "+str(39-sum([1 if i=="P" else 3 if i=="N" else 3 if i =="B" else 5 if i == "R" else 9 if i == "Q" else 0 for i in str(game).replace("\n", " ").split(" ")]))
						+"\nAdvantage: "+str(round(advantage/100, 1))
						+"```")
					else:
						mate = analyze.info["score"][1].mate
						if not game.turn:
							mate = mate*-1
						await channel.send("```css\nWhite Points: "
						+str(39-sum([1 if i=="p" else 3 if i=="n" else 3 if i =="b" else 5 if i == "r" else 9 if i == "q" else 0 for i in str(game).replace("\n", " ").split(" ")]))
						+"\nBlack Points: "+str(39-sum([1 if i=="P" else 3 if i=="N" else 3 if i =="B" else 5 if i == "R" else 9 if i == "Q" else 0 for i in str(game).replace("\n", " ").split(" ")]))
						+"\nAdvantage: #"+str(mate)
						+"```")

				else:
					await channel.send('You are not in a game! Make one with '+prefix+'newgame [mention]')


			if command == "pay":
				await channel.trigger_typing()
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





			if args[0] == "bio":
				if len(args) > 1:
					u = user


					bio = ' '.join(args[1:])
					if len(bio)<=250:
						db.update_user(u["id"],"bio",bio)
						await channel.send("Bio set!")
					else:
						await channel.send('Your bio is too long! (Over 250 characters)')
				else:
					await channel.send('You must specify a bio!')

			if args[0] == "teambio":
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




			if args[0] == "newteam":

				if len(args) > 1:
					u = user

					if u["team"] == None:
						name = args[1].replace("@", "")
						if len(name) > 2 and len(name) < 17:
							if not name in db.teams.distinct('name'):
								if u["xp"] >= 800:
									db.inc_user(u["id"], "xp", -800)
									db.new_team(name, u["id"])
									db.update_user(u["id"], "team", name)
									await channel.send("Team "+name+" has been created by <@!"+str(u["id"])+">!")
									await bot.get_channel(config.LOGCHANNEL).send("`Create Team: "+name+"`")
								else:
									await channel.send("You do not have enough tokens to create a team! 800T needed!")
							else:
								await channel.send("That team name is already taken!")
						else:
							await channel.send("The team name must be in between 3 and 16 characters long (and one word)!")
					else:
						await channel.send("You are already in a team! Leave it first.")
				else:
					await channel.send("You must specify a team name!")

			if args[0] == "renameteam":

				if len(args) > 1:
					u = user

					if u["team"] != None:
						name = args[1].replace("@", "")
						if len(name) > 2 and len(name) < 17:
							if not name in db.teams.distinct('name'):
								if u["xp"] >= 200:
									team = db.get_team(u["team"])
									db.inc_user(u["id"], "xp", -200)
									db.update_team(u["team"], "id", name)
									db.update_team(name, "name", name)
									for m in team["members"]:
										db.update_user(m, "team", name)

									await channel.send("Team "+team["name"]+" has been renamed to "+name+"!")
									await bot.get_channel(config.LOGCHANNEL).send("`Rename Team: "+team["name"]+" "+name+"`")
								else:
									await channel.send("You do not have enough tokens to rename your team! 200T needed!")
							else:
								await channel.send("That team name is already taken!")
						else:
							await channel.send("The team name must be in between 3 and 16 characters long (and one word)!")
					else:
						await channel.send("You do not own a team!")
				else:
					await channel.send("You must specify a team name!")

			if args[0] == "transferownership":

				if message.mentions:
					u = user
					t = db.get_team(user["team"])
					if t != None and t["owner"] == u["id"]:
						newowner = message.mentions[0]
						if newowner.id in t["members"]:
							if newowner.id == t["owner"]:
								await channel.send("Making yourself feel like you have more power doesn't mean you have more power...")
							else:
								db.update_team(t["id"], "owner", newowner.id)
								await channel.send("The ownership of team "+t["id"]+" has been transfered to <@!"+str(newowner.id)+">!")
						else:
							await channel.send("That user is not in your team!")

					else:
						await channel.send("You do not own a team!")
				else:
					await channel.send("You must specify a new owner!")


			if args[0] == "kick":
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

			if args[0] == "disband":
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


			if args[0] == "leave":
				await channel.trigger_typing()

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



			if args[0] == "recruit":
				await channel.trigger_typing()
				if mentions:
					u1 = user

					u2 = db.get_member(mentions[0])


					if u2["team"] == None:
						team = db.get_team(u1["team"])
						if team != None and team["owner"] == u1["id"]:
							if len(team["members"]) < config.MAXTEAMSIZE:
								await channel.send(str(mentions[0].mention)+", you are being invited to "+str(mem.mention)+"'s team! Use `"+prefix+"join` to join or `"+prefix+"decline` to decline the request!")
								try:
									def check(message):
										return message.author == mentions[0] and (message.content == prefix+'join' or message.content == prefix+'decline')
									resp = await bot.wait_for('message', check=check, timeout=50)
									if resp.content == prefix+'join':
										team = db.get_team(u1["team"])
										if len(team["members"]) < config.MAXTEAMSIZE:
											await resp.channel.trigger_typing()
											db.push_team(team["id"], "members", u2["id"])
											db.update_user(u2["id"], "team", team["id"])
											await resp.channel.send("<@!"+str(u2["id"])+"> has joined team "+team["name"]+"!")
											await bot.get_channel(config.LOGCHANNEL).send("`Join Team: "+u2["name"]+" "+team["id"]+" "+str(guildid)+"`")
										else:
											await resp.channel.send('That team is full!')
									elif resp.content == prefix+'decline':
										await resp.channel.send('You have declined the request!')
								except:
									await channel.send("The request has timed out!")
							else:
								await channel.send('Your team is full!')
						else:
							await channel.send('You do not own a team!')
					else:
						await channel.send('That user is already in a team!')
				else:
					await channel.send('You must mention another user!')


			if args[0] == "draw":

				await channel.trigger_typing()
				if game != None:

					await channel.send("<@!"+str(ids[not ids.index(memid)])+">, you are being offered a draw from "+str(mem.mention)+"! Use `"+prefix+"accept` to accept the draw or `"+prefix+"decline` to decline the draw!")

					try:

						def check(message):
							return message.author.id == ids[not ids.index(memid)] and (message.content == prefix+'accept' or message.content == prefix+'decline')
						resp = await bot.wait_for('message', check=check, timeout=15)

						if resp.content == prefix+'accept':
							await reward_game(memid, ids[not ids.index(memid)], "accepteddraw", gamedata,channel)

						elif resp.content == prefix+'decline':
							await channel.send("You have declined the draw request!")

					except:
						await channel.send("The request has timed out!")

				else:
					await channel.send('You are not in a game! Make one with '+prefix+'newgame [mention]')




			if args[0] == "team":
				await channel.trigger_typing()
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


			if args[0] == "buy":

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



			if args[0] == "coinflip":
				await channel.send(random.choice(["Heads","Tails"]))

			if command == "joke":
				await channel.send(random.choice(config.JOKES))


			if args[0] in ["board", "bd"]:
				await channel.trigger_typing()
				if game != None:
					await channel.send(content= ["Black", "White"][game.turn]+" to move...", file=discord.File(open(makeboard(game), 'rb')))
				else:
					await channel.send('You are not in a game! Make one with '+prefix+'newgame [mention]')


			if args[0] in ["profile", "pf"]:
				await channel.trigger_typing()

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




			if args[0] == "about":
				await channel.trigger_typing()
				em = discord.Embed()
				em.title="About Chess"
				em.set_thumbnail(url=bot.user.avatar_url)
				em.colour = discord.Colour(4623620)
				em.type = "rich"

				em.description = "A bot for playing a Chess game in your server with ease. Challenge your friends to fight to the death."
				em.add_field(name="Creator",value="qwerty#6768",inline=True)
				em.add_field(name="Help Command",value=prefix+"help",inline=True)
				em.add_field(name="Servers",value=str(len(bot.guilds)),inline=True)
				em.add_field(name="Users",value=str(sum([len(i.members) for i in bot.guilds])),inline=True)
				em.add_field(name="Support Server",value="discord.gg/uV5y7RY",inline=True)
				em.add_field(name="Version",value="2.5.9",inline=True)
				em.set_footer(text="Special thanks: Rapptz, niklasf, channelcat, MongoDB Inc, DBL, Aurora, And you, yes you.")
				em.url = "https://discordbots.org/bot/366770566331629579"
				await channel.send(embed=em)



			if args[0] == "shop":
				await channel.trigger_typing()
				em = discord.Embed()
				em.set_thumbnail(url="http://simpleicon.com/wp-content/uploads/shop-5.png")
				em.title="Chess Shop"
				em.colour = discord.Colour(4623620)
				em.type = "rich"
				#badges
				em.add_field(name="Chump Change Badge",value="Price: "+str(config.prices["chumpchangebadge"][0])+"T\nID: chumpchangebadge",inline=True)
				em.add_field(name="Rich Badge",value="Price: "+str(config.prices["richbadge"][0])+"T\nID: richbadge",inline=True)
				#items
				await channel.send(embed=em)





			if args[0] in ["leaderboard", "lb"]:
				await channel.trigger_typing()
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

					elif args[1].lower() == "teams":
						unit = "cur"
						lead = db.leaderboardteams(8,"cur")

					elif args[1].lower() == "server":
						unit = "cur"
						lead = db.leaderboardguild(guild,"cur")

					elif args[1].lower() == "servers":
						unit = "games"
						lead = db.leaderboardguilds(8,"games")

					else:
						lead = db.leaderboard(8)
						title = "shards"
						unit = "cur"
					#if args[1].lower() == "unique":
					#	lead = db.leaderboard(5,"unique")
				else:
					lead = db.leaderboard(8)
					title = "shards"
					unit = "cur"
				em.title = title.title()
				for i,ii in zip(lead,range(len(lead))):
					em.add_field(name=str(ii+1),value=i["name"]+": "+str(i[unit]),inline=False)


				await channel.send(embed=em)

			if args[0] == "listserver":

				try:
					db.new_guild(guildid,guildname)
				except:
					pass
				try:
					inv = await list(message.guild.channels)[0].create_invite()
					if mem == guildowner:
						await bot.get_channel(433475984751329283).send(str(inv))
						db.update_guild(guildid,"listed",True)
						await channel.send("Server listed!")
					else:
						await channel.send("You are not the server owner!")
				except Exception as E:
					try:
						inv = await list(message.guild.channels)[1].create_invite()
						if mem == guildowner:
							await bot.get_channel(433475984751329283).send(str(inv))
							db.update_guild(guildid,"listed",True)
							await channel.send("Server listed!")
						else:
							await channel.send("You are not the server owner!")
					except Exception as E:
						await channel.send("I do not have permission to make an invite link!")


			if args[0] == "unlistserver":

				try:
					db.new_guild(guildid,guildname)
				except:
					pass
				if mem == guildowner:
					db.update_guild(guildid,"listed",False)
					await channel.send("Server unlisted!")
				else:
					await channel.send("You are not the server owner!")

			if args[0] == "randserver":
				while 1:
					try:
						s = db.rand_listed_guild()["id"]
						inv = await list(bot.get_guild(s).channels)[0].create_invite(max_age=60)
						break
					except:
						db.update_guild(s, "listed", False)

				await channel.send(str(inv))



			if args[0] == "prefix":
				if len(args) > 1:
					if mem == guildowner:
						if len(args[1]) < 3:
							db.update_guild(guild.id, "prefix", args[1])
							await channel.send("Prefix set!")
						else:
							await channel.send("That prefix is too long!")
					else:
						await channel.send("You are not the server owner!")
				else:
					await channel.send("You must specify a prefix!")



			if args[0] == "hasbeat":

				if not len(message.raw_mentions)<2:
					try:
						user = db.get_user(message.raw_mentions[0])
						if message.raw_mentions[1] in user["unique"]:
							await channel.send("<@!"+str(message.raw_mentions[0])+"> **has** beat <@!"+str(message.raw_mentions[1])+">!")
						else:
							await channel.send("<@!"+str(message.raw_mentions[0])+"> **has not** beat <@!"+str(message.raw_mentions[1])+">!")
					except:
						await channel.send("<@!"+str(message.raw_mentions[0])+"> **has not** beat <@!"+str(message.raw_mentions[1])+">!")
				else:
					await channel.send("You must mention two people!")



			if args[0] in ["newgame", "ng"]:
				await channel.trigger_typing()
				if game == None:
					if mentions:


						game2 = db.get_game(mentions[0].id)

						if game2 == None:
							if mentions[0].id == memid:
								await channel.send("You can't connect with yourself in this way. Why not take a walk?")

							else:
								await channel.send(str(mentions[0].mention)+", you are being challenged to a chess game by "+str(mem.mention)+"! Use `"+prefix+"accept` to accept the challenge or `"+prefix+"decline` to decline the challenge!")

								try:

									def check(message):
										return message.author == mentions[0] and (message.content == prefix+'accept' or message.content == prefix+'decline')
									resp = await bot.wait_for('message', check=check, timeout=50)

									if resp.content == prefix+'accept':
										await resp.channel.trigger_typing()
										u1 = db.get_member(mem)
										u2 = db.get_member(mentions[0])

										db.new_game(chess.Board().fen(),u1["id"], u2["id"])

										await channel.send('The game has started! Type '+prefix+'board to see the board!')

										await bot.get_channel(config.LOGCHANNEL).send("`Create Game: "+str(u1["name"])+" "+str(u2["name"])+" "+str(guildid)+"`")

										await bot.change_presence(activity=discord.Game(name=str(db.games.find().count())+" games!"),status=discord.Status.online)
										db.inc_guild(guildid, "games", 1)
									elif resp.content == prefix+'decline':
										await channel.send("You have declined the game request!")
								except:
									await channel.send("The request has timed out!")

						else:
							await channel.send('That user is currently in a game with another person!')
					else:
						await channel.send('You must mention another user!')
				else:
					await channel.send('You are already in a game! Resign it with '+prefix+'resign')



			if args[0] == "exit":
				if game != None:
					await reward_game(ids[not ids.index(memid)], memid, "exit", gamedata,channel)
				else:
					await channel.send('You are not in a game! Make one with '+prefix+'newgame [mention]')

			if args[0] == "resign":
				if game != None:
					await reward_game(ids[not ids.index(memid)], memid, "resign", gamedata,channel)
				else:
					await channel.send('You are not in a game! Make one with '+prefix+'newgame [mention]')



			if args[0] == "pgn":
				if message.mentions:
					try:
						g = db.get_game_recent(message.mentions[0].id)
						await channel.send('```'+str(pgn_from_moves(g["moves"]))+'```')
					except:
						await channel.send("That user hasn't played any games!")
				else:
					try:
						g = db.get_game_recent(memid)
						await channel.send('```'+str(pgn_from_moves(g["moves"]))+'```')
					except:
						await channel.send("You haven't played any games! Play one with "+prefix+"newgame [mention]")

			if args[0] == "fen":
				try:
					g = db.get_game_recent(memid)
					await channel.send('```'+str(g["fen"])+'```')
				except:
					await channel.send("You haven't played any games! Make one with "+prefix+"newgame [mention]")



			if args[0] == "badge":
				if len(args) > 1:
					try:
						await channel.send([key for key, value in config.BADGES.items() if value == args[1]][0].replace("-"," ").title())
					except:
						await channel.send('Badge not found!')
				else:
					await channel.send('You must specify a badge as an emoji!')


			if args[0] == "help":
				if len(args) > 1:
					help = None
					if args[1].lower() == "core":
						help = """```css
[Core]
|about: See info about the bot.
|help: Displays this message.
|leaderboard (sort): See who the best players are! Sort changes what it sorts by: wins, loss, tokens, votes, teams, etc.
|profile (mention): Check all of your stats!
|badge [emoji]: Get badge name from emoji!
|hasbeat [mention] [mention]: Check if a player has ever beat another player.
|invite: Get bot invite link.```
						""".replace("|", prefix)

					elif args[1].lower() == "economy":
						help = """```css
[Economy]
|pay [mention] [amount]: Give tokens to another user!
|shop: See all the items on display that you could buy!
|buy [itemid]: Buy that item you've always wanted.```
						""".replace("|", prefix)
					elif args[1].lower() == "games":
						help = """```css
[Games]
|newgame [mention]: Request to play a game with whoever you mention.
|board: Shows the game board.
|move [notation]: Moves a piece using standard notation. Ex. a2a4: piece a2 to a4. a7a8q: piece a7 to a8 and promote to queen.
|go [notation]: Moves a piece. The notation format is standard algebraic notation. Ex. a3 would move piece a2 to a3. This is more complex, if you don't know how to use it, use |move.
|analyze: Check how many points you and your opponent have, and get an advantage analysis.
|draw: Request a draw.
|resign: Accept your defeat.
|exit: Exit the current game you are in.```
						""".replace("|", prefix)
					elif args[1].lower() == "teams":
						help = """```css
[Teams]
|newteam [name]: Create a team, costs 800T, name must be one word.
|renameteam [name]: Rename your team, costs 200T, name must be one word.
|recruit [mention]: Add people to your team.
|team (mention/teamname): View team stats.
|kick [mention]: Kick someone from your team.
|leave: Leave a team.
|disband: Disband your team, costs 800T.```
						""".replace("|", prefix)
					elif args[1].lower() == "servers":
						help = """```css
[Servers]
|prefix [prefix]: Edit the bot's prefix in your server.
|server: Get dev server and chess server link.
|listserver: Add your server to a list of servers where players can look for other chess players.
|unlistserver: Unlist your server.
|randserver: Get an invite for a random listed server.```
						""".replace("|", prefix)

					elif args[1].lower() == "other":
						help = """```css
[Other]
|coinflip: Flip a coin!
|donate: Please I need money for the server.
|vote: Vote for my bot to give it more reputation. Win tokens and a badge! Vote daily.
|suggestion [suggestion]: Suggest a feature for the bot.
|report [mention] [proof/reason]: Report a user for foul play.
|bug [bug]: Report a bug in the bot.```
						""".replace("'+prefix+'", prefix)


					else:
						await channel.send('You must specify a valid command category: `core`, `economy`, `games`, `teams`, `servers`, or `other`.')
					try:
						await channel.send(help)
					except:
						pass
				else:
					await channel.send('You must specify a command category: `core`, `economy`, `games`, `teams`, `servers`, or `other`.')





			if args[0] == "server":
				await channel.send("https://discord.gg/uV5y7RY")


			if args[0] == "invite":
				await channel.send("https://discordapp.com/oauth2/authorize?client_id=366770566331629579&scope=bot&permissions=8")

			if args[0] == "donate":
				await channel.send("https://www.patreon.com/qwertyquerty")

			if args[0] == "vote":
				await channel.send("https://discordbots.org/bot/366770566331629579/vote")



			if args[0] == "debug" and memid in config.ADMINS:
				try:
					await channel.send(str(eval(msgcontent.replace(prefix+"debug "," "))))
				except Exception as E:
					await channel.send("```python\n"+str(traceback.format_exc())+"```")


			if args[0] == "ping":
				now = datetime.datetime.utcnow()
				delta = now-message.created_at
				await channel.send(str(delta.total_seconds()*1000)+'ms')




			if args[0] == "time" and memid in config.ADMINS:
				try:
					t0 = time.time()
					msg = eval(msgcontent.replace(prefix+"time "," "))
					t1 = time.time()
					tf = t1-t0

					await channel.send((str(msg))+", `"+str(tf)+"`")
				except Exception as E:
					await channel.send("```python\n"+str(traceback.format_exc())+"```")



			if args[0] == "test" and memid in config.ADMINS:
				n = 0
				for guild in bot.guilds:
					n+=1

					if len(guild.members) <= 2000:
						print(str(n))
						try:
							cs = [c for c in guild.channels if c.name in ["general", "bots", "commands", "bot-commands","bot", "botuse", "chess"]]
							channel = cs[0]
							em = discord.Embed()
							em.title="Yet Another Chess Tournament!"
							em.set_thumbnail(url=bot.user.avatar_url)
							em.colour = discord.Colour(4623620)
							em.type = "rich"
							em.description = "My creator has decided they want to hold a second (yes a second) Chess tournament using the ChessBot (me!) The prize for winning will be 3000 tokens, a special role, and a tournament winner badge on your profile! There might be some money too but who knows.... Heres how to join:"
							em.add_field(name="Step 1",value="Join the Chess Tournament server. You can get the invite link by doing the command "+prefix+"server.",inline=True)
							em.add_field(name="Step 2",value="DM qwerty#6768 (my creator) telling him you want to join the tournament.")
							em.add_field(name="Step 3",value="The tournament will only start once a certain amount of players have joined, so play the waiting game.")
							em.set_footer(text="Tournament Games do not have to be played at set times. There will be cheat detection. This message will not come again.")
							await channel.send(embed=em)
						except:
							try:
								channel = cs[1]
								em = discord.Embed()
								em.title="Yet Another Chess Tournament!"
								em.set_thumbnail(url=bot.user.avatar_url)
								em.colour = discord.Colour(4623620)
								em.type = "rich"
								em.description = "My creator has decided they want to hold a second (yes a second) Chess tournament using the ChessBot (me!) The prize for winning will be 3000 tokens, a special role, and a tournament winner badge on your profile! There might be some money too but who knows.... Heres how to join:"
								em.add_field(name="Step 1",value="Join the Chess Tournament server. You can get the invite link by doing the command "+prefix+"server.",inline=True)
								em.add_field(name="Step 2",value="DM qwerty#6768 (my creator) telling him you want to join the tournament.")
								em.add_field(name="Step 3",value="The tournament will only start once a certain amount of players have joined, so play the waiting game.")
								em.set_footer(text="Tournament Games do not have to be played at set times. There will be cheat detection. This message will not come again.")
								await channel.send(embed=em)
							except Exception as E:
								print(E)

			if args[0] == "test2" and memid in config.ADMINS:
					try:
						await channel.trigger_typing()
						em = discord.Embed()
						em.title="Yet Another Chess Tournament!"
						em.set_thumbnail(url=bot.user.avatar_url)
						em.colour = discord.Colour(4623620)
						em.type = "rich"
						em.description = "My creator has decided they want to hold a second (yes a second) Chess tournament using the ChessBot (me!) The prize for winning will be 3000 tokens, a special role, and a tournament winner badge on your profile! There might be some money too but who knows.... Heres how to join:"
						em.add_field(name="Step 1",value="Join the Chess Tournament server. You can get the invite link by doing the command "+prefix+"server.",inline=True)
						em.add_field(name="Step 2",value="DM qwerty#6768 (my creator) telling him you want to join the tournament.")
						em.add_field(name="Step 3",value="The tournament will only start once a certain amount of players have joined, so play the waiting game.")
						em.set_footer(text="Tournament Games do not have to be played at set times. There will be cheat detection. This message will not come again.")
						await channel.send(embed=em)
					except:
						pass






			if args[0] == "suggestion":
				if len(args) > 1:
					await channel.send("Suggestion sent!")
					em = discord.Embed()
					em.description=' '.join(args[1:])
					em.colour = discord.Colour(4623620)
					em.set_author(name=str(mem), icon_url=mem.avatar_url)
					msg = await bot.get_channel(441095220038467585).send(embed=em)
					await msg.add_reaction("\U00002705")
					await msg.add_reaction("\U0000274e")

			if args[0] == "bug":
				if len(args) > 1:
					await channel.send("Report sent!")
					em = discord.Embed()
					em.description=' '.join(args[1:])
					em.colour = discord.Colour(4623620)
					em.set_author(name=str(mem), icon_url=mem.avatar_url)
					msg = await bot.get_channel(433404972227493890).send(embed=em)
					await msg.add_reaction("\U00002705")
					await msg.add_reaction("\U0000274e")


			if args[0] == "report":
				if message.mentions:
					if len(args) > 2 or message.attachments:
						await channel.send("Report sent!")
						em = discord.Embed()
						em.description=' '.join(args[2:])
						em.colour = discord.Colour(4623620)
						em.add_field(name="Name", value=str(message.mentions[0]),inline=False)
						em.add_field(name="ID", value=str(message.mentions[0].id),inline=False)
						em.add_field(name="Server", value=str(message.guild.id),inline=False)
						em.set_author(name=str(mem), icon_url=mem.avatar_url)
						if message.attachments:
							em.set_image(url=message.attachments[0].url)
						msg = await bot.get_channel(config.REPORTCHANNEL).send(embed=em)
						await msg.add_reaction("\U00002705")
						await msg.add_reaction("\U0000274e")

					else:
						await channel.send("You must specify a report reason / proof!")
				else:
					await channel.send("You must specify who you want to report!")

			if args[0] == "restart" and memid in config.ADMINS:

				await channel.send("Attempting to restart... Saving...")

				await channel.send("Saved...")
				if len(args) > 1:
					os.system("pm2 restart "+args[1])
				else:
					os.system("pm2 restart chess")
					await bot.change_presence(status=discord.Status.dnd)



			if args[0] == "await" and memid in config.ADMINS:
				try:
					await channel.send(await eval(msgcontent.replace(prefix+"await "," ")))
				except Exception as E:
					await channel.send(E)

			if args[0] == "setstatus" and memid in config.ADMINS:
				await bot.change_presence(activity=discord.Game(name=msgcontent.replace(prefix+"setstatus "," ")),status=discord.Status.online)

	except discord.errors.Forbidden:
		return
	except Exception as E:
		await bot.get_channel(config.ERRORCHANNEL).send("```python\n"+str(traceback.format_exc())+"```\n"+"`"+str(message.author)+": "+message.content+"`")




bot.run(config.BOTTOKEN)
