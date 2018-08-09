import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
    if len(args) > 1:
    	await channel.send("Report sent!")
    	em = discord.Embed()
    	em.description=' '.join(args[1:])
    	em.colour = discord.Colour(4623620)
    	em.set_author(name=str(mem), icon_url=mem.avatar_url)
    	msg = await bot.get_channel(433404972227493890).send(embed=em)
    	await msg.add_reaction("\U00002705")
    	await msg.add_reaction("\U0000274e")
