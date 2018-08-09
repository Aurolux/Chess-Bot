import discord
import chess
import thedb as db
import config
from boardgen import *
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
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
						await reward_game(memid, ids[not ids.index(memid)], "checkmate", gamedata,channel,bot)
					else:
						await reward_game(memid, "computer", "checkmate", gamedata,channel,bot)

				if game.is_stalemate() or game.is_fivefold_repetition() or game.is_seventyfive_moves():
					if gamedata["ranked"]:
						await reward_game(memid, ids[not ids.index(memid)], "stalemate", gamedata,channel,bot)
					else:
						await reward_game(None, None, "stalemate", gamedata,channel,bot)

				if game.is_insufficient_material():
					if gamedata["ranked"]:
						await reward_game(memid, ids[not ids.index(memid)], "draw", gamedata,channel,bot)
					else:
						await reward_game(None, None, "draw", gamedata,channel,bot)

			else:
				await channel.send("You must specify what move you wish to make!")
		else:
			await channel.send("It is not your turn!")

		if game.is_check() and not game.is_checkmate():
			await channel.send('**Check!**')

	else:
		await channel.send('You are not in a game! Make one with '+prefix+'newgame [mention]')
