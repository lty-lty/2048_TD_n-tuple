from tuplenet import TupleNet
from board import Board
import time

def test(_episode=5000, _milestone=500):

	grid = Board()
	model = TupleNet()

	episode = _episode
	milestone = _milestone

	print("start testing")
	print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

	score = 0
	maxscore = 0

	for e in range(1,episode+1) :
		grid.Start_New_Game()
		model.New_Episode()
		totalR = 0
		while True:
			action , r = model.Take_Action(grid)
			#print(Game.tile)
			totalR += r
			if r != -5 :
				grid.Gen_New_Tile()
			if grid.End_Of_Game():
				break
		model.Add_Count(grid)
		score += totalR
		if totalR > maxscore:
			maxscore = totalR
		#print(e," ",totalR)

		if e % milestone == 0:
			print("\n")
			print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
			model.Print_Count(e)
			avgscore = score // e
			print("#Episode: {episode}, AvgScore: {avg_score}, MaxScore: {max_score}".format(episode = e , avg_score = avgscore , max_score = maxscore))
