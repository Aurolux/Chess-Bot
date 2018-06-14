from sanic import Sanic, response
import asyncio
import thedb as db
import threading
import config
app = Sanic(__name__)

@app.route('/api/chess/votes', methods=['POST'])
async def on_vote(request):
    if request.headers.get('Authorization') == config.WEBHOOKTOKEN:
        data = request.json

        try:
            user = int(data['user'])

        except:
            return response.json({'success': False}, status=500)
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
            print(E)
            pass

        return response.json({'success': True}, status=200)
    else:
        return response.json({'success': False}, status=500)


app.run(host="0.0.0.0", port=3000)
