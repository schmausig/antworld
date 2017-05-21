#!/usr/bin/env python3

from numpy.random import choice

class A():

	RANDOM_FACTOR = 1/10 #this must be > 0 to avoid division by zero and smaller for bigger 'alpha'
	SEARCH_P_INT = 1/50 #intensity of search pheromone between 0 and 1
	DELIVER_P_INT = 1/50	#intensity of deliver pheromone
	
class Ant():

	def __init__(self, AG, pos=None):
		self.AG = AG
		if not pos: 
			self.pos = AG.hq
			AG.node[AG.hq].ants.add(self)
		else:
			self.pos = pos
			AG.node[pos].ants.add(self)
		self.last = None #last node
		self.next = None #next node
		self.state = 'search'
		self.food = 0

	def decide(self):
		try:
			if len(self.pos[0])==2:
				print(self,' can only decide on nodes')
		except:
			pass
		
		antnode = self.AG.node[self.pos] 
		#and the current one if the ant is searching and the node has food or if its delivering and node=HQ
		if not self.decide_to_stay():
			neighbors = list(self.AG[self.pos].keys())	
			weights = []
			if self.state == 'search':
				for neighbor in neighbors:
					if neighbor == self.last:
						weights.append(A.RANDOM_FACTOR)
					else:
						weights.append(self.AG[self.pos][neighbor].p[1] + A.RANDOM_FACTOR)
			elif self.state == 'deliver':
				for neighbor in neighbors:
					if neighbor == self.last:
						weights.append(A.RANDOM_FACTOR)
					else:
						weights.append(self.AG[self.pos][neighbor].p[0] + A.RANDOM_FACTOR)
			wsum = sum(weights)
			probs = [weight/wsum for weight in weights]
			self.next = neighbors[choice(range(len(neighbors)), 1, p=probs)[0]]
		
		
	def decide_to_stay(self): #to pick up or lay down
		#this is kinda deterministic atm and at least laying down food should remain like that
		antnode = self.AG.node[self.pos]
		if antnode.foodcount > 0 and self.state == 'search':
			if len(antnode.ants)-1 < antnode.foodcount: #TODO better
				self.state = 'pickup'
				return True
		elif self.state == 'deliver' and type(antnode).__name__ == 'AntHQ' :
			self.state = 'laydown'
			return True
		return False
	
	def use_phero(self, p_nr, intensity):
		self.AG[self.pos[0]][self.pos[1]].increase_phero(p_nr, intensity)

	def move_on_tic(self):
		#print(self.pos)
		#print(self.state)
		if self.state == 'search':
			self.AG.node[self.pos].ants.remove(self)
			self.AG[self.pos][self.next].ants.add(self)
			self.pos = (self.pos, self.next)
			self.use_phero(p_nr=0, intensity = A.SEARCH_P_INT)
		elif self.state == 'deliver':
			self.AG.node[self.pos].ants.remove(self)
			self.AG[self.pos][self.next].ants.add(self)
			self.pos = (self.pos, self.next)
			self.use_phero(p_nr=1, intensity = A.DELIVER_P_INT)
		
	def move_on_tac(self):
		#print(self.pos)
		#print(self.state)

		if self.state == 'search' or self.state == 'deliver':
			self.AG[self.pos[0]][self.pos[1]].ants.remove(self)
			self.AG.node[self.pos[1]].ants.add(self)
			self.last = self.pos[0]
			self.pos = self.pos[1]
			self.next = None
		elif self.state == 'pickup':
			antnode = self.AG.node[self.pos]
			self.food = antnode.get_food()
			self.state = 'deliver'
			self.last = self.pos
		elif self.state == 'laydown':
			antnode = self.AG.node[self.pos]
			antnode.add_food(self.food)
			self.food = 0
			self.state = 'search'
			self.last = self.pos

				


