import discord
import chess
import thedb as db
import config
import traceback
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):

    if memid in config.ADMINS:
        try:
            o = await eval(msgcontent.replace(prefix+"await "," "))
            await channel.send(str(o))
        except Exception as E:
            await channel.send("```python\n"+str(traceback.format_exc())+"```")
