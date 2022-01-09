from gamegrid import GameGrid
from argparse import ArgumentParser
from trainer import train
from tester import test

parser = ArgumentParser()
parser.add_argument("--mode", help = "Play/Train/Eval (play/train/test), default: play", dest="mode", default="play")
parser.add_argument("-e", help = "Total episodes to train/test, default: 5000", dest="episode", type=int, default=5000)
parser.add_argument("-m", help = "Milestone to save tuple nets and show training statistics, default: 500", dest="milestone", type=int, default=500)

args = parser.parse_args()

if __name__ == "__main__":


	EPISODE = args.episode
	MILESTONE = args.milestone	

	if args.mode == "play":
		print("\n\n")
		print("#########		Use w/a/s/d to move tiles UP/LEFT/DOWN/RIGHT")
		print("#########		Wanna get a hint?") 
		print("#########		Press 'h' to let the AI to help moving the critical step for you!")
		print("#########		Can't breakthrough your personal record?") 
		print("#########		Press 'z' to see how the AI crack this game! (AI auto play mode)")
		print("")
		print("auto play mode can be toggled by pressing 'z' again\n\n")
		Game2048 = GameGrid()

	if args.mode == "train":
		train(EPISODE, MILESTONE)

	if args.mode == "test":
		test(EPISODE, MILESTONE)
