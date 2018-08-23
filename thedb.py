from pymongo import MongoClient
import math
import datetime
import random
import config
import itertools
from bson.objectid import ObjectId

client = MongoClient()
db = client.chess
users = db.users
guilds = db.guilds
teams = db.teams
games = db.games


users.create_index("id",unique=True)
guilds.create_index("id",unique=True)
teams.create_index("id",unique=True)





def new_game(fen, player1,player2,ranked=True):
    data = {"fen": fen, "moves": [], "winner": None, "loser": None, "done": False, "outcome": None, "1": player1, "2": player2, "ranked": ranked, "timestamp": datetime.datetime.utcnow()}
    games.insert_one(data)


def update_game(id,key,value):
    games.update_one({"_id":id},{"$set": {key:value}})

def get_game_id(id):
    return games.find_one({"_id": id})


def add_move(id, move, fen):
    db.games.update_one({"_id":id},{"$push": {"moves": move}})
    db.games.update_one({"_id":id},{"$set": {"fen": fen}})

def end_game(id, winner, loser, outcome):
    db.games.update_one({"_id":id},{"$set": {"winner": winner}})
    db.games.update_one({"_id":id},{"$set": {"loser": loser}})
    db.games.update_one({"_id":id},{"$set": {"outcome": outcome}})
    db.games.update_one({"_id":id},{"$set": {"done": True}})

def get_game(userid):
    return games.find_one({"$or": [{"$and":[{"1":userid},{"done": False}]},  {"$and":[{"2":userid},{"done": False}]}]})


def get_game_from_id(gameid):
    return games.find_one({"_id": ObjectId(gameid)})


def get_games(userid):
    return games.find({"$or": [{"1":userid},{"2":userid}]}).sort('timestamp',-1)

def get_game_recent(userid):
    return games.find({"$or": [{"1":userid},  {"2":userid}]}).sort('timestamp',-1).next()



def get_old_game(userid):
    return games.find_one({"$or": [{"$and":[{"1":userid},{"done": True}]},  {"$and":[{"2":userid},{"done": True}]}]})


def new_guild(id,name):
    data = {"name":name,"id":id,"prefix":"|","listed":False, "games": 0}
    guilds.insert_one(data)

def update_guild(id,key,value):
    guilds.update_one({"id":id},{"$set": {key:value}})

def inc_guild(id,key,value):
    guilds.update_one({"id":id},{"$inc": {key:value}})


def get_guild(id):
    return guilds.find_one({"id":id})



def rand_listed_guild():
     return [i for i in guilds.find({"listed": True}).limit(1).skip(math.floor(random.random()*guilds.count({"listed": True})))][0]



def new_team(name,owner):
    data = {"name":name,"id":name,"members": [owner], "cur": 10000, "games":0, "wins": 0, "draws": 0, "loss": 0, "bio": None, "owner": owner}
    teams.insert_one(data)

def update_team(id,key,value):
    teams.update_one({"id":id},{"$set": {key:value}})


def inc_team(id,key,value):
    teams.update_one({"id":id},{"$inc": {key:value}})

def push_team(id,key,value):
    teams.update_one({"id":id},{"$push": {key:value}})

def pull_team(id,key,value):
    teams.update_one({"id":id},{"$pull": {key:value}})

def get_team(id):
    return teams.find_one({"id":id})

def delete_team(id):
    t = get_team(id)
    for m in t["members"]:
        update_user(m, "team", None)
    teams.delete_one({"id":id})



def new_user(id,name):
    data = {"name":name,"id":id,"team": None, "wins":0,"loss":0,"draws":0,"games":0,"xp":0,"unique":[],"badges": [], "votes": 0, "skins": ["default"], "inv": [],"skin": "default", "bio": None, "blacklisted": False, "color": config.COLOR, "elo": 1600}
    users.insert_one(data)

def update_user(id,key,value):
    users.update_one({"id":id},{"$set": {key:value}})


def inc_user(id,key,value):
    users.update_one({"id":id},{"$inc": {key:value}})

def push_user(id,key,value):
    users.update_one({"id":id},{"$push": {key:value}})

def pull_user(id,key,value):
    users.update_one({"id":id},{"$pull": {key:value}})

def add_badge(id,badge):
    users.update_one({"id":id},{"$push": {"badges":badge}})

def remove_badge(id,badge):
    users.update_one({"id":id},{"$pull": {"badges":badge}})

def leaderboard(limit,sort="elo"):
    return [i for i in db.users.find({"games": {"$gt": 0}}).sort(sort,-1).limit(limit)]

def leaderboardteams(limit,sort="cur"):
    return [i for i in db.teams.find({"games": {"$gt": 0}}).sort(sort,-1).limit(limit)]

def leaderboardguild(guild,sort="elo"):
    ids = [i.id for i in guild.members]
    return [i for i in itertools.islice((i for i in db.users.find({"games": {"$gt": 0}}).sort(sort,-1) if i["id"] in ids),8)]

def leaderboardguilds(limit,sort="games"):
    return [i for i in db.guilds.find({"games": {"$gt": 0}}).sort(sort,-1).limit(limit)]

def get_user(id):
    return users.find_one({"id":id})

def get_member(member):
    u = get_user(member.id)
    if u == None:
    	new_user(member.id,str(member))
    	u = get_user(member.id)
    return u

def retrieve_guild(guild):
    u = get_guild(guild.id)
    if u == None:
    	new_guild(guild.id,guild.name)
    	u = get_guild(member.id)
    return u


def delete_user(id):
    users.delete_one({"id":id})
