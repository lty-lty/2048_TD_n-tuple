import numpy as np
import random
import copy

class Board():
	def __init__(self) :
		self.tile = np.zeros((4, 4), dtype = np.uint32)
		self.Start_New_Game()

	def Copy_Board(self, tmp):
		self.tile = tmp.tile.copy()	

	# 寻找空位生成新的随机块
	def Gen_New_Tile(self) :
		rank = [ i for i in range(16) ]
		random.shuffle(rank)
		for idx in range(16) :
			r = rank[idx] // 4
			c = rank[idx] % 4
			if self.tile[r][c] == 0 :
				break

		rd = random.random()
		if rd < 0.9 :
			self.tile[r][c] = 1
		else :
			self.tile[r][c] = 2		


	def Get_Tile(self, pos):
		r = pos // 4
		c = pos % 4
		return self.tile[r][c]

	# 开始新游戏，随机生成两个初始块	
	def Start_New_Game(self) :
		self.tile = np.zeros((4, 4), dtype = np.uint32)
		self.Gen_New_Tile()
		self.Gen_New_Tile()

	# 判断是否游戏结束
	def End_Of_Game(self):
		tmp = Board()
		tmp.Copy_Board(self)
		if tmp.move(0) == -5 and tmp.move(1) == -5 and tmp.move(2) == -5 and tmp.move(3) == -5 :
			return True
		else:
			return False

	# 向指定方向移动并返回分数
	def move(self,direction) :
		if direction == 0 : 
			return self.move_up()		
		if direction == 1 : 
			return self.move_right()
		if direction == 2 : 
			return self.move_down()
		if direction == 3 : 
			return self.move_left()
		return -5
		
	# 向上移动并返回分数	
	def move_up(self):
		score = 1
		cur = self.tile.copy()
		self.tile = np.zeros((4, 4), dtype = np.uint32)
		for c in range(4) :
			top = 0
			block = [0,0,0,0]
			for idx in range(4) :
				if cur[idx][c] != 0 :
					if top > 0 and self.tile[top-1][c] == cur[idx][c] and block[top-1] == 0 :
						self.tile[top-1][c] += 1
						block[top-1] = 1
						score += (1 << self.tile[top-1][c])
					else :
						self.tile[top][c] = cur[idx][c]
						top += 1

		if np.array_equal(cur, self.tile):
			return -5
		else:
			return score

	def move_down(self):
		self.up_side_down()
		score = self.move_up()
		self.up_side_down()
		return score

	def move_left(self):
		self.rotate_right()
		score = self.move_up()
		self.rotate_left()
		return score

	def move_right(self):
		self.rotate_left()
		score = self.move_up()
		self.rotate_right()
		return score

	# 向右旋转 90°
	def rotate_right(self):
		cur = self.tile.copy()
		for r in range(4):
			for c in range(4):
				self.tile[r][c] = cur[3-c][r]

	def rotate_left(self):
		self.rotate_right()
		self.rotate_right()
		self.rotate_right()

	# 上下翻转
	def left_side_right(self):
		cur = self.tile.copy()
		for r in range(4):
			for c in range(4):
				self.tile[r][c] = cur[r][3-c]
	
	# 左右翻转
	def up_side_down(self):
		cur = self.tile.copy()
		for r in range(4):
			for c in range(4):
				self.tile[r][c] = cur[3-r][c]

	# 将盘面转化为 8 种等价状态
	def Change_Board(self, i):
		#if i == 0: keep the same board
		if i & 4 > 0 :
			self.rotate_right()
		if i & 2 > 0 :
			self.left_side_right()
		if i & 1 > 0 :
			self.up_side_down()
