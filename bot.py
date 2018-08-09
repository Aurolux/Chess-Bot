from __future__ import print_function
import chess
import re, sys, time
from itertools import count
from collections import OrderedDict, namedtuple
import discord
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
from alias import ALIASES
from util import *
from bson.objectid import ObjectId





bot = discord.AutoShardedClient()
board = chess.Board()



@bot.event
async def on_ready():
	print("Ready!")
	if config.MOTD == "":
		await bot.change_presence(activity=discord.Game(name=str(db.games.find().count())+" games!"),status=discord.Status.online)
	else:
		await bot.change_presence(activity=discord.Game(name=config.MOTD),status=discord.Status.online)

@bot.event
async def on_guild_join(guild):
	db.new_guild(guild.id,guild.name)
	await bot.get_channel(config.LOGCHANNEL).send("`Join guild: "+guild.name+"`")
	try:
		payload = {"shard_count": len(bot.shards), "server_count"  : len(bot.guilds)}
		async with aiohttp.ClientSession() as aioclient:
				await aioclient.post(config.DBLURL, data=payload, headers=config.DBLHEADERS)

	except:
		pass

@bot.event
async def on_guild_remove(guild):
	await bot.get_channel(config.LOGCHANNEL).send("`Leave guild: "+guild.name+"`")
	try:
		payload = {"shard_count": len(bot.shards), "server_count"  : len(bot.guilds)}
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
		if str(message.author.id) != str(config.ID) and not message.author.bot and message.content.startswith(prefix):


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
			ids = None
			if gamedata != None:
				game = chess.Board(fen=gamedata["fen"])
				ids = (gamedata["1"], gamedata["2"])

			args = ' '.join(msgcontent.strip(prefix).split()).split()
			try:
				command = args[0]
			except:
				return


			if command in ALIASES and ALIASES[command] != None:
				await channel.trigger_typing()
				await ALIASES[command](args=args,command=command,bot=bot,prefix=prefix,msg=msg,message=msg,guildid=guildid,guild=guild,memid=memid,mem=mem,mentions=mentions,channel=channel, user=user, game=game, gamedata=gamedata, msgcontent=msgcontent,ids=ids)

				if guild != None:
					await bot.get_channel(config.LOGCHANNEL).send("```Member: "+str(mem)+"\nMember ID: "+str(memid)+"\nGuild: "+str(guild)+"\nGuild ID: "+str(guildid)+"\n\nCommmand: "+str(command)+"\n\nArgs: "+str(args)+"```")
				else:
					await bot.get_channel(config.LOGCHANNEL).send("```Member: "+str(mem)+"\nMember ID: "+str(memid)+"\n\nCommmand: "+str(command)+"\n\nArgs: "+str(args)+"```")


	except Exception as E:
		await bot.get_channel(config.ERRORCHANNEL).send("```python\n"+str(traceback.format_exc())+"```\n"+"`"+str(message.author)+": "+message.content+"`")




bot.run(config.BOTTOKEN)
