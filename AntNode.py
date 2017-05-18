#!/usr/bin/env python3

class AntNode():

	def __init__(self, foodcount=0):		
		self.foodcount = foodcount
		self.ants = set()
		
	def get_food(self):
		if self.foodcount > 0:
			self.foodcount -= 1
			return 1
		else: return 0
	
class AntHQ(AntNode):

	def __init__(self):
		super().__init__()
		self.collected = 0
			
	def add_food(self, amount):
		self.collected += amount
		
		

