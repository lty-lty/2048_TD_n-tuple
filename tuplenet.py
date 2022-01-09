from board import Board
import numpy as np
import random
import os

class TupleNet():

	def __init__(self):
		self.episode = []
		self.net = []
		self.alpha = 0.0025
		self.gamma = 1.0
		self.Reset_Count()
		
		if os.path.isfile("tupleNet/tuple1.npy"):
			print("Found tuple network. Loading...")
			self.Load_TupleNet("tupleNet/tuple")
			print("Completed")
		else:
			print("Building tuple Network...")
			self.Build_TupleNet()
			print("Completed")

	def Build_TupleNet(self):
		self.net.append(np.zeros(shape=(20, 20, 20, 20, 20, 20), dtype=np.float32))
		self.net.append(np.zeros(shape=(20, 20, 20, 20, 20, 20), dtype=np.float32))
		self.net.append(np.zeros(shape=(20, 20, 20, 20), dtype=np.float32))
		self.net.append(np.zeros(shape=(20, 20, 20, 20), dtype=np.float32))
		
	def Load_TupleNet(self, filename):
		for i in range(4):
			self.net.append(np.load(filename+str(i+1)+".npy"))

	def Save_TupleNet(self):
		for i in range(4):
			np.save("tupleNet/tuple%d" % (i+1), self.net[i])

	def Update_TupleNet(self, tmp, TD_error):
		self.net[0][tmp.Get_Tile(0)][tmp.Get_Tile(4)][tmp.Get_Tile(8)][tmp.Get_Tile(1)][tmp.Get_Tile(5)][tmp.Get_Tile(9)] += TD_error
		self.net[1][tmp.Get_Tile(1)][tmp.Get_Tile(5)][tmp.Get_Tile(9)][tmp.Get_Tile(2)][tmp.Get_Tile(6)][tmp.Get_Tile(10)] += TD_error
		self.net[2][tmp.Get_Tile(2)][tmp.Get_Tile(6)][tmp.Get_Tile(10)][tmp.Get_Tile(14)] += TD_error
		self.net[3][tmp.Get_Tile(3)][tmp.Get_Tile(7)][tmp.Get_Tile(11)][tmp.Get_Tile(15)] += TD_error

	# 返回网络存储的 value 值
	def Get_Value(self, b):
		v = 0
		tmp = Board()
		for i in range(8):
			tmp.Copy_Board(b)
			tmp.Change_Board(i)
			v += self.net[0][tmp.Get_Tile(0)][tmp.Get_Tile(4)][tmp.Get_Tile(8)][tmp.Get_Tile(1)][tmp.Get_Tile(5)][tmp.Get_Tile(9)]
			v += self.net[1][tmp.Get_Tile(1)][tmp.Get_Tile(5)][tmp.Get_Tile(9)][tmp.Get_Tile(2)][tmp.Get_Tile(6)][tmp.Get_Tile(10)]
			v += self.net[2][tmp.Get_Tile(2)][tmp.Get_Tile(6)][tmp.Get_Tile(10)][tmp.Get_Tile(14)]
			v += self.net[3][tmp.Get_Tile(3)][tmp.Get_Tile(7)][tmp.Get_Tile(11)][tmp.Get_Tile(15)]
		return v

	# 创建新的 episode
	def New_Episode(self):
		self.episode = []


	# 更新 value 值，并删除 episode
	def Del_Episode(self):
		tmp = Board()
		top = len(self.episode)
		if top == 0 :
			return

		bf = self.episode[-1]['state']
		S = self.Get_Value(bf)
		for i in range(8) :
			tmp.Copy_Board(bf)
			tmp.Change_Board(i)
			self.Update_TupleNet(tmp, self.alpha*(-20 - S))

		top -= 2
		while top >= 0 :
			bf = self.episode[top]['state']
			S = self.Get_Value(bf)
			af = self.episode[top+1]['state']
			Sp = self.Get_Value(af)		
			R = self.episode[top]['reward']
	
			for i in range(8) :
				tmp.Copy_Board(bf)
				tmp.Change_Board(i)
				self.Update_TupleNet(tmp, self.alpha*(R + Sp - S))

			top -= 1

		self.episode.clear()


	# 比较四个方向，做出决策 
	def Take_Action(self, prev):
		maxV , maxOP = -10000 , -1
		tmp = Board()
		for op in range(4):
			tmp.Copy_Board(prev)
			r = tmp.move(op)
			if r != -5 :
				v = self.Get_Value(tmp)
				if v + r > maxV :
					maxV = v + r
					maxOP = op

		if maxOP != -1 :
			tmp.Copy_Board(prev)
			r = prev.move(maxOP)
			state = {}
			state['state'] = tmp
			state['reward'] = r
			state['action'] = maxOP
			self.episode.append(state)
			return maxOP , r 
		else :
			return -1 , -1

	# 清空各个方块的记录
	def Reset_Count(self):
		self.maxtile = 0
		self.count = [0 for i in range(25)]

	# 新增各个方块的记录
	def Add_Count(self,b):
		mt = 0
		for pos in range(16):
			r = pos // 4
			c = pos % 4
			t = b.tile[r][c]
			if t > mt :
				mt = t
			if mt > self.maxtile :
				self.maxtile = mt
		for idx in range(1,mt+1):
			self.count[idx] += 1
	
	# 输出方块的记录情况
	def Print_Count(self, milestone):
		for i in range(self.maxtile, max(self.maxtile-6,1), -1):
			print("{}: {:.2%}".format((np.int32(1) << np.int32(i)), (self.count[i] / milestone)))

