import discord
import chess
import thedb as db
import config
from util import *

async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
    if mentions:
        gs = [i for i in db.get_games(mentions[0].id)]
        u = db.get_user(mentions[0].id)
        if gs == []:
            channel.send(mentions[0].mention+" hasn't played any games!")
            return

    else:
        gs = [i for i in db.get_games(memid)]
        u = user
        if gs == []:
            channel.send("You haven't played any games!")
            return


    em = discord.Embed()
    em.title= u["name"]+"'s games"
    em.colour = discord.Colour(config.COLOR)
    em.type = "rich"
    em.description = "Game ids sorted by time"
    for g in gs:
        em.add_field(name=str(g["_id"]),value=db.get_user(g["1"])["name"] + " vs "+db.get_user(g["2"])["name"])

    await channel.send(embed=em)
