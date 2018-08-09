import discord
import chess
import thedb as db
import config
from util import *
async def main(args=None, command=None, bot=None, prefix=None, msg=None, message=None, guildid=None, guild=None, memid=None, mem=None, mentions=None, channel=None, user=None, game=None, gamedata=None, dbguild=None, msgcontent=None, ids=None):

	if args[0] == "help":
		if len(args) > 1:
			help = None
			if args[1].lower() == "core":
				help = """```css
[Core]
|about: See info about the bot.
|help: Displays this message.
|leaderboard (sort): See who the best players are! Sort changes what it sorts by: wins, loss, tokens, votes, teams, etc.
|profile (mention): Check all of your stats!
|badge [emoji]: Get badge name from emoji!
|hasbeat [mention] [mention]: Check if a player has ever beat another player.
|invite: Get bot invite link.```
				""".replace("|", prefix)

			elif args[1].lower() == "economy":
				help = """```css
[Economy]
|pay [mention] [amount]: Give tokens to another user!
|shop: See all the items on display that you could buy!
|buy [itemid]: Buy that item you've always wanted.```
				""".replace("|", prefix)
			elif args[1].lower() == "games":
				help = """```css
[Games]
|newgame [mention]: Request to play a game with whoever you mention.
|board: Shows the game board.
|move [notation]: Moves a piece using standard notation. Ex. a2a4: piece a2 to a4. a7a8q: piece a7 to a8 and promote to queen.
|go [notation]: Moves a piece. The notation format is standard algebraic notation. Ex. a3 would move piece a2 to a3. This is more complex, if you don't know how to use it, use |move.
|analyze: Check how many points you and your opponent have, and get an advantage analysis.
|draw: Request a draw.
|resign: Accept your defeat.
|exit: Exit the current game you are in.```
				""".replace("|", prefix)
			elif args[1].lower() == "teams":
				help = """```css
[Teams]
|newteam [name]: Create a team, costs 800T, name must be one word.
|renameteam [name]: Rename your team, costs 200T, name must be one word.
|recruit [mention]: Add people to your team.
|team (mention/teamname): View team stats.
|kick [mention]: Kick someone from your team.
|leave: Leave a team.
|disband: Disband your team, costs 800T.```
				""".replace("|", prefix)
			elif args[1].lower() == "servers":
				help = """```css
[Servers]
|prefix [prefix]: Edit the bot's prefix in your server.
|server: Get dev server and chess server link.
|listserver: Add your server to a list of servers where players can look for other chess players.
|unlistserver: Unlist your server.
|randserver: Get an invite for a random listed server.```
				""".replace("|", prefix)

			elif args[1].lower() == "other":
				help = """```css
[Other]
|coinflip: Flip a coin!
|donate: Please I need money for the server.
|vote: Vote for my bot to give it more reputation. Win tokens and a badge! Vote daily.
|suggestion [suggestion]: Suggest a feature for the bot.
|report [mention] [proof/reason]: Report a user for foul play.
|bug [bug]: Report a bug in the bot.```
				""".replace("'+prefix+'", prefix)


			else:
				await channel.send('You must specify a valid command category: `core`, `economy`, `games`, `teams`, `servers`, or `other`.')
			try:
				await channel.send(help)
			except:
				pass
		else:
			await channel.send('You must specify a command category: `core`, `economy`, `games`, `teams`, `servers`, or `other`.')
