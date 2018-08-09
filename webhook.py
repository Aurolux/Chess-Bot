from flask import Flask, request,jsonify
import thedb as db
import config
import tok
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
app = Flask(__name__)
print("test")


@app.route('/api/votes', methods=['POST'])
def on_vote():
    print(request.headers)
    if request.headers.get('Authorization') == tok.WEBHOOKTOKEN:
        data = request.json

        try:
            user = int(data['user'])

        except Exception as E:
            return jsonify({'success': False})
        try:
            member = db.get_user(user)
            db.inc_user(user,"xp",70)
            db.inc_user(user,"votes",1)
            if "voter" not in member["badges"]:
                db.add_badge(user,"voter")
                config.send_message(config.VOTECHANNEL, member["name"]+" voted and got 70 tokens plus the voter badge!")
            else:
                config.send_message(config.VOTECHANNEL, member["name"]+" voted and got 70 tokens!")
        except Exception as E:
            pass

        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route('/api/users/<int:userid>', methods=['GET'])
def api_user(userid):
    try:
        user = db.get_user(userid)
        del user["_id"]
        return jsonify(user)
    except:
        return jsonify({'error': 'unknown'})

@app.route('/api/users/<int:userid>/games', methods=['GET'])
def api_user_games(userid):
    try:
        games = [game for game in db.get_games(userid)]
        for game in games:
            game["id"] = str(game["_id"])
            game["timestamp"] = int(game["timestamp"].timestamp())
            del game["_id"]

        return jsonify(games)
    except:
        return jsonify({'error': 'unknown'})



@app.route('/api/users/<int:userid>/games/recent', methods=['GET'])
def api_user_games_recent(userid):
    try:
        game = db.get_game_recent(userid)
        game["id"] = str(game["_id"])
        game["timestamp"] = int(game["timestamp"].timestamp())
        del game["_id"]

        return jsonify(game)
    except:
        return jsonify({'error': 'unknown'})

@app.route('/api/games/<string:gameid>', methods=['GET'])
def api_game(gameid):
    try:
        game = db.get_game_from_id(gameid)
        game["id"] = str(game["_id"])
        game["timestamp"] = int(game["timestamp"].timestamp())
        del game["_id"]

        return jsonify(game)
    except:
        return jsonify({'error': 'unknown'})



@app.route('/api/servers/<int:serverid>', methods=['GET'])
def api_server(serverid):
    try:
        server = db.get_guild(serverid)
        del server["_id"]

        return jsonify(server)
    except:
        return jsonify({'error': 'unknown'})

@app.route('/api/teams/<string:teamid>', methods=['GET'])
def api_team(teamid):
    try:
        team = db.get_team(teamid)
        del team["_id"]

        return jsonify(team)
    except:
        return jsonify({'error': 'unknown'})

@app.route('/api/stats', methods=['GET'])
def api_stats():
    try:
        stats = {
            "members": db.users.count(),
            "servers": db.guilds.count(),
            "teams": db.teams.count(),
            "games": db.games.count(),
            "unfinished_games": db.games.find({"done": False}).count(),
            "listed_servers": db.games.find({"listed": True}).count(),
            "motd": config.MOTD
        }

        return jsonify(stats)
    except:
        return jsonify({'error': 'unknown'})


#app.run(host="0.0.0.0", port=80,debug=True)

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(80)
IOLoop.instance().start()
