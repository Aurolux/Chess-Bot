import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
    if game != None:

    	await channel.send("<@!"+str(ids[not ids.index(memid)])+">, you are being offered a draw from "+str(mem.mention)+"! Use `"+prefix+"accept` to accept the draw or `"+prefix+"decline` to decline the draw!")

    	try:

    		def check(message):
    			return message.author.id == ids[not ids.index(memid)] and (message.content == prefix+'accept' or message.content == prefix+'decline')
    		resp = await bot.wait_for('message', check=check, timeout=15)

    		if resp.content == prefix+'accept':
    			await reward_game(memid, ids[not ids.index(memid)], "accepteddraw", gamedata,channel,bot)

    		elif resp.content == prefix+'decline':
    			await channel.send("You have declined the draw request!")

    	except:
    		await channel.send("The request has timed out!")

    else:
    	await channel.send('You are not in a game! Make one with '+prefix+'newgame [mention]')
