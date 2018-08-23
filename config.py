import requests
from tok import *
SHARD_COUNT = 3

BOTURL = "https://discordbots.org/bot/366770566331629579"

MOTD = ""

ELO_K = 75

COLOR = 4623620
DBLURL = "https://discordbots.org/api/bots/366770566331629579/stats"

DISCURL = "https://discordapp.com/api"

MAXTEAMSIZE = 6

DBLHEADERS = {"Authorization" : DBLTOKEN}

DISCHEADERS = {"Authorization" : "Bot "+BOTTOKEN}

ID = 366770566331629579


prices = {"richbadge": (20000,"badge","rich"), "chumpchangebadge": (500,"badge","chump-change"), "teamworkmedal": (50000,"item","teamworkmedal")}

PREFIX = "|"

ADMINS = [202560559046983681]

ERRORCHANNEL = 433431162107723787
VOTECHANNEL = 430858422582378517
LOGCHANNEL = 436342882551595008
REPORTCHANNEL = 447451872337461248


BADGES = {"tournament-first-place": "\U0001f947", "tournament-second-place": "\U0001f948", "developer": "\U00002699", "voter": "\U0001f4dd","artist":"\U0001f3a8", "rich": "\U0001f4b0", "chump-change": "\U0001f4b8", "pro": "\U00002694", "expert": "\U0001f5e1", "novice": "\U0001f4a1", "addicted": "\U0001f48a", "international-master": "\U0001f3c6", "patron": "\U0001f4b3", "partner": "\U0001f517", "chess-bot-master": "\U0001f3f3", "beat-moca": "<:mocaREEE:476893827165192192>"}




def send_message(channel,content):
    r = requests.post(DISCURL+"/channels/"+str(channel)+"/messages", data={"content": content}, headers=DISCHEADERS)
    return r.json()


WINMESSAGES = [
"TORE THE HEAD OFF OF--err, won in a chess match against",
"tarnished the self-confidence of",
"demolished",
"just finished off",
"finally beat",
"actually beat",
"supprisingly beat",
"somehow beat",
"took the W against",
"is now the legal owner of",
"ruined the hopes and dreams of",
"forced dust into the mouth of",
"used an engine. Just kidding! He legitimately beat",
"completely slaughtered",
"is a cheater. Haha just kidding, he won fair and square against",
"owes a big kiss to",
"can now ask any favor from",
"can now request or demand anything from",
"is a chess master. Guess who isn't: ",
"needs to give a formal appology",
"will have to regain the friendship of",
"should say sorry to"
]





JOKES = [
"I was playing chess with a friend of mine the other day, and he says, \"Let's make this interesting.\" So we stopped playing chess.",
"Opening with 'Na3' is known as the sodium assault.",
"How do you make a small fortune in chess? Start out with a large one!",
"If the IRA are so anti-English, why do they use so much c4?",
"I like playing chess with bald men, but sometimes it is hard to find 32 of them."
"Why doesn't Botvinnik spill his coffee? Because he has an iron grip.",
"What do you call surrendering? The french defence.",
"Well this is more interesting than hearing a chess match on the radio.",
"Why are chess champions such good matchmakers? Because they always find mates for their opponents!",
"Where do you buy chess pieces ...at the PAWN SHOP!",
"Why can't the Brits play chess? Because they can't tell a Bishop from a Queen.",
"Why did the grandmaster date a Slovak girl? Because he wanted a czechmate.",
"Why is chess just like real life? The king can only take a step at a time and the queen can do as she pleases.",
"Why can't administrative officers win at chess? Because they can't stop to watch the clock.",
"What's the difference between a chess player and a highway construction worker? A chess player moves every now and then.",
"What do Kramnik and a wellhouse pump have in common? They could both draw water.",
"Chuck Norris doesn't play chess anymore. He found checkmating opponents in 1 move to be boring.",
"I was having dinner with Garry Kasporov – problem was, we had a checkered tablecloth and it took him an hour to pass the salt!",
"What's the difference between a professional chess player and a large cheese pizza? The pizza can feed a family of four.",
"Which group of women are the best chess players? Feminists. Their opponents begin with King and Queen, but *they* always start with 2 Queens.",
"How do you get a grandmaster off of your front porch? Pay him for the pizza.",
]


CSS = """
text {
    fill: #f1ad00;
    font-size:20px;
    font-weight: bold;
}
"""
