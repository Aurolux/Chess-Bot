import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	em = discord.Embed()
	em.set_thumbnail(url="http://simpleicon.com/wp-content/uploads/shop-5.png")
	em.title="Chess Shop"
	em.colour = discord.Colour(4623620)
	em.type = "rich"
	#badges
	em.add_field(name="Chump Change Badge",value="Price: "+str(config.prices["chumpchangebadge"][0])+"T\nID: chumpchangebadge",inline=True)
	em.add_field(name="Rich Badge",value="Price: "+str(config.prices["richbadge"][0])+"T\nID: richbadge",inline=True)
	#items
	em.add_field(name="Medal Of Teamwork",value="Price: "+str(config.prices["teamworkmedal"][0])+"T\nID: teamworkmedal",inline=True)
	await channel.send(embed=em)
