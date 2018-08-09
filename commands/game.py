import discord
import chess
import thedb as db
import config
from util import *

async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):
    if mentions:
        try:
            g = db.get_game_recent(mentions[0].id)
        except:
            await channel.send(mentions[0].mention+" hasn't played any games!")
            return
        if g == None:
            await channel.send(mentions[0].mention+" hasn't played any games!")
            return
    else:
        if len(args) > 1:
            try:
                g = db.get_game_from_id(args[1])
            except:
                await channel.send("Invalid game id!")
                return
            if g == None:
                await channel.send("Game not found!")
                return
        else:
            try:
                g = db.get_game_recent(memid)
            except:
                await channel.send("You haven't played any games!")
                return
            if g == None:
                await channel.send("You haven't played any games!")
                return

    em = discord.Embed()
    em.title="Game "+str(g["_id"])
    em.colour = discord.Colour(config.COLOR)
    em.type = "rich"
    em.description = str(pgn_from_moves(g["moves"]))
    em.add_field(name="White",value=db.get_user(g["1"])["name"],inline=True)
    em.add_field(name="Black",value=db.get_user(g["2"])["name"],inline=True)
    if g["done"]:
        em.add_field(name="Outcome",value=g["outcome"].title(),inline=True)
    else:
        em.add_field(name="Outcome",value="Unfinished",inline=True)
    em.add_field(name="Completed",value=str(g["done"]),inline=True)
    if g["outcome"] in ["checkmate", "resign"]:
        em.add_field(name="Winner",value=db.get_user(g["winner"])["name"],inline=True)

    em.add_field(name="Timestamp",value=str(g["timestamp"].strftime('%m-%d-%Y %H:%M:%S')),inline=True)

    await channel.send(embed=em)
