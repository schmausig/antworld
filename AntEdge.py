#!/usr/bin/env python3

class AntEdge():
		
	def __init__(self):
		self.p = [0,0]
		self.ants = set()
		self.scoutants = set()
	
	def vaporize(self, intensity):
		for p_nr in range(len(self.p)):
			self.decrease_phero(p_nr, intensity)

	def increase_phero(self, p_nr, intensity):
		self.p[p_nr] = min(self.p[p_nr] + intensity, 1)
	
	def decrease_phero(self, p_nr, intensity):
		self.p[p_nr] = max(self.p[p_nr] - intensity, 0)
