from tuplenet import TupleNet
from board import Board
import time

def train(_episode=5000, _milestone=500):

	grid = Board()
	model = TupleNet()

	episode = _episode
	milestone = _milestone

	print("start training")
	print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

	totalR = 0
	for e in range(1,episode+1):
		grid.Start_New_Game()
		model.New_Episode()
		while True :
			action , r = model.Take_Action(grid)
			totalR += r
			if r != -5 :
				grid.Gen_New_Tile()
			if grid.End_Of_Game():
				break
		model.Del_Episode()
		model.Add_Count(grid)
		if e % milestone == 0:
			print("\n")
			print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
			print("#Episode: {episode}, score: {score}".format(episode = e, score = totalR // milestone ))
			model.Save_TupleNet()	
			model.Print_Count(milestone)
			model.Reset_Count()
			totalR = 0

