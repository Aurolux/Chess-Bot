import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
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
