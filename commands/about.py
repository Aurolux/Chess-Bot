import discord
import chess
import thedb as db
import config
from util import *

async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	em = discord.Embed()
	em.title="About Chess"
	em.set_thumbnail(url=bot.user.avatar_url)
	em.colour = discord.Colour(4623620)
	em.type = "rich"

	em.description = "A bot for playing a Chess game in your server with ease. Challenge your friends to fight to the death."
	em.add_field(name="Creator",value="qwerty#6768",inline=True)
	em.add_field(name="Help Command",value=prefix+"help",inline=True)
	em.add_field(name="Servers",value=str(len(bot.guilds)),inline=True)
	em.add_field(name="Users",value=str(sum([len(i.members) for i in bot.guilds])),inline=True)
	em.add_field(name="Support Server",value="discord.gg/uV5y7RY",inline=True)
	em.add_field(name="Version",value="2.5.9",inline=True)
	em.set_footer(text="Special thanks: Rapptz, niklasf, channelcat, MongoDB Inc, DBL, Aurora, And you, yes you.")
	em.url = "https://discordbots.org/bot/366770566331629579"
	await channel.send(embed=em)
