import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
	if message.mentions:
		if len(args) > 2 or message.attachments:
			await channel.send("Report sent!")
			em = discord.Embed()
			em.description=' '.join(args[2:])
			em.colour = discord.Colour(4623620)
			em.add_field(name="Name", value=str(message.mentions[0]),inline=False)
			em.add_field(name="ID", value=str(message.mentions[0].id),inline=False)
			em.add_field(name="Server", value=str(message.guild.id),inline=False)
			em.set_author(name=str(mem), icon_url=mem.avatar_url)
			if message.attachments:
				em.set_image(url=message.attachments[0].url)
			msg = await bot.get_channel(config.REPORTCHANNEL).send(embed=em)
			await msg.add_reaction("\U00002705")
			await msg.add_reaction("\U0000274e")

		else:
			await channel.send("You must specify a report reason / proof!")
	else:
		await channel.send("You must specify who you want to report!")
