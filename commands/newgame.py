import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
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
							if config.MOTD == "":
								await bot.change_presence(activity=discord.Game(name=str(db.games.find().count())+" games!"),status=discord.Status.online)
							else:
								await bot.change_presence(activity=discord.Game(name=config.MOTD),status=discord.Status.online)

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
