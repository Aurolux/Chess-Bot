import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
    if memid in config.ADMINS:
        config.MOTD = msgcontent.replace(prefix+"setstatus ","")
        await bot.change_presence(activity=discord.Game(name=config.MOTD),status=discord.Status.online)
        await channel.send('Status set!')
