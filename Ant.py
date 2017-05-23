#!/usr/bin/env python3

from numpy.random import choice
from AntConstants import A, SA

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
		
		#stay on current node if the ant is searching and the node has food or if its delivering and node=HQ
		if not self.decide_to_stay():
			#else decide next node
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




class ScoutAnt(Ant):

	def __init__(self, AG, pos=None):
		self.AG = AG
		if not pos: 
			self.pos = AG.hq
			AG.node[AG.hq].scoutants.add(self)
		else:
			self.pos = pos
			AG.node[pos].scoutants.add(self)
		self.last = None #last node
		self.next = None #next node
		self.state = 'search'
		
		self.afternext = None
		self.nextstate = None
			
	def decide(self):

		try:
			if len(self.pos[0])==2:
				print(self,' can only decide on nodes')
		except:
			pass
			
		#DECIDE NEXT
		neighbors = list(self.AG[self.pos].keys())	
		weights = []
		if self.state == 'search':
			for neighbor in neighbors:
				if neighbor == self.last:
					weights.append(SA.RANDOM_FACTOR)
				else:
					weights.append(self.AG[self.pos][neighbor].p[1] + SA.RANDOM_FACTOR)
		elif self.state == 'gohome':
			for neighbor in neighbors:
				if neighbor == self.last:
					weights.append(SA.RANDOM_FACTOR)
				else:
					weights.append(self.AG[self.pos][neighbor].p[0] + SA.RANDOM_FACTOR)
		wsum = sum(weights)
		probs = [weight/wsum for weight in weights]
		self.next = neighbors[choice(range(len(neighbors)), 1, p=probs)[0]]
		
		#change the state before afternext decision
		if self.next == self.AG.hq:
			self.nextstate = 'search'
		elif self.AG.node[self.next].foodcount > 0:
			self.nextstate = 'gohome'
		else:
			self.nextstate = self.state

		#DECIDE AFTERNEXT
		neighbors = list(self.AG[self.next].keys())	
		weights = []
		if self.nextstate == 'search':
			for neighbor in neighbors:
				if neighbor == self.pos:
					weights.append(SA.RANDOM_FACTOR)
				else:
					weights.append(self.AG[self.next][neighbor].p[1] + SA.RANDOM_FACTOR)
		elif self.nextstate == 'gohome':
			for neighbor in neighbors:
				if neighbor == self.pos:
					weights.append(SA.RANDOM_FACTOR)
				else:
					weights.append(self.AG[self.next][neighbor].p[0] + SA.RANDOM_FACTOR)
		wsum = sum(weights)
		probs = [weight/wsum for weight in weights]
		self.overnext = neighbors[choice(range(len(neighbors)), 1, p=probs)[0]]

	def use_phero(self, p_nr, intensity):
		self.AG[self.last][self.pos].increase_phero(p_nr, intensity)

	def move_on_tic(self):
		self.AG.node[self.pos].scoutants.remove(self)
		self.AG.node[self.next].scoutants.add(self)
		self.last = self.pos
		self.pos = self.next
		#always use_phero after the ant physically moved to the other set and self.last, self.pos are updated
		if self.state == 'search':
			self.use_phero(p_nr=0, intensity=SA.SEARCH_P_INT)
		elif self.state == 'gohome':
			self.use_phero(p_nr=1, intensity=SA.DELIVER_P_INT)
		self.state = self.nextstate
		self.nextstate = None

	def move_on_tac(self):
		self.AG.node[self.pos].scoutants.remove(self)
		self.AG.node[self.overnext].scoutants.add(self)
		self.last = self.pos
		self.pos = self.overnext
		#always use_phero after the ant physically moved to the other set and self.last, self.pos are updated
		if self.state == 'search':
			self.use_phero(p_nr=0, intensity=SA.SEARCH_P_INT)
		elif self.state == 'gohome':
			self.use_phero(p_nr=1, intensity=SA.DELIVER_P_INT)

		if self.pos == self.AG.hq:
			self.state = 'search'
		elif self.AG.node[self.pos].foodcount > 0:
			self.state = 'gohome'
