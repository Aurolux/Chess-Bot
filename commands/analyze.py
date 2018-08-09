import discord
import chess
import config
import thedb as db
import chess.uci
from util import *
engine = chess.uci.popen_engine("stockfish")
analyze = chess.uci.InfoHandler()
engine.info_handlers.append(analyze)


async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if game != None:
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
