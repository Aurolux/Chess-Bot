import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageSequence
import thedb as db
import chess
import imageio
import numpy
import random
import chess.svg
import cairosvg
import config as cfg




"""
def makeboard(boardstring, check,move,ids,computer=False):
	skin1 = db.get_user(ids[0])["skin"]
	if computer == False:
		skin2 = db.get_user(ids[1])["skin"]
	else:
		skin2 = "default"

	skin = "default"

	bd = boardstring
	boardstring = str(boardstring)
	if check:
		board = Image.open("boardcheck.jpg")
	else:
		board = Image.open("board.jpg")

	draw = ImageDraw.Draw(board)
	try:
		draw.line([
		((move.to_square%8)*58)+63+29,
		((8-int(move.to_square/8))*58)+64-29,
		((move.from_square%8)*58)+63+29,
		((8-int(move.from_square/8))*58)+64-29],width=10,fill=(0,0,0))
	except Exception as e:
		#print(e)
		pass

	for i1, i2 in zip(boardstring.split('\n'), range(len(boardstring.split('\n')))):
		ypos = (i2*58)+64
		for ii1, ii2 in zip(i1.split(' '), range(len(i1.split(' ')))):
			xpos = (ii2*58)+64
			if ii1 != ".":
				if ii1.islower():
					ii1 = 'b'+ii1
					board.paste(Image.open('./pieces/'+skin2+'/'+ii1.lower()+'.png').resize((58,58)), (xpos,ypos), mask=Image.open('./pieces/'+skin2+'/'+ii1.lower()+'.png').resize((58,58)))
				else:
					board.paste(Image.open('./pieces/'+skin1+'/'+ii1.lower()+'.png').resize((58,58)), (xpos,ypos), mask=Image.open('./pieces/'+skin1+'/'+ii1.lower()+'.png').resize((58,58)))

	filename = './boardimages/'+str(random.randint(0,99))+'.png'
	board.save(filename, "PNG")
	return(filename)
"""

def makeboard(board):
	filename = './boardimages/'+str(random.randint(0,99))+'.png'
	if len(board.move_stack)>0:
		#flipped=not board.turn
		cairosvg.svg2png(bytestring=chess.svg.board(board=board, lastmove=board.peek(), style=cfg.CSS), write_to=filename)
	else:
		#flipped=not board.turn
		cairosvg.svg2png(bytestring=chess.svg.board(board=board, style=cfg.CSS), write_to=filename)
	return filename
