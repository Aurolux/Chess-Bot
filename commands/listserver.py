import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	try:
		db.new_guild(guildid,guildname)
	except:
		pass
	try:
		inv = await list(message.guild.channels)[0].create_invite()
		if mem == guild.owner:
			await bot.get_channel(433475984751329283).send(str(inv))
			db.update_guild(guildid,"listed",True)
			await channel.send("Server listed!")
		else:
			await channel.send("You are not the server owner!")
	except Exception as E:
		try:
			inv = await list(message.guild.channels)[1].create_invite()
			if mem == guild.owner:
				await bot.get_channel(433475984751329283).send(str(inv))
				db.update_guild(guildid,"listed",True)
				await channel.send("Server listed!")
			else:
				await channel.send("You are not the server owner!")
		except Exception as E:
			await channel.send("I do not have permission to make an invite link!")
