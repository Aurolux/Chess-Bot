import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
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
