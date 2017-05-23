#!/usr/bin/env python3

import math
from ast import literal_eval
import itertools

from AntNode import AntNode, AntHQ
from AntEdge import AntEdge
from Ant import Ant, ScoutAnt
from AntPlayer import AntPlayer
from AntDrawer import AntDrawer
from AntConstants import AG

class AntGraph():

	def __init__(self, name=None, path=None, darea=None, hq=None, foodplaces=None, x_range=None, y_range=None, gen=False):
		self.node = dict()		#dict with keys=nodeposition vals=AntNode
		self.adj  = dict()
		self.name = name
		self.ants = set()
		self.scoutants = set()
		self.time = 0
		self.foodmax = 0
		self.foodsum = 0
		self.finished = False
		if path:
			self.read_from_file(path)
		if hq and foodplaces and x_range and y_range:
			self.rectangle(hq, foodplaces, x_range, y_range)
		if gen:
			self.gen()
		self.drawer = AntDrawer(self, darea=darea)
		self.player = AntPlayer(self, darea=darea)

	def add_node(self, pos, foodcount=0, flag=None):
		if pos not in self:
			if flag == 'hq':
				antnode = AntHQ(collected=foodcount)
				self.hq = pos
			else:
				antnode = AntNode(foodcount=foodcount)
			self.node[pos] = antnode
			self.adj[pos] = dict()
			self.foodmax = max(self.foodmax, foodcount)
			self.foodsum += foodcount
		else:
			print('There is already a node at pos '+str(pos))
			
	def add_edge(self, pos1, pos2, shutup=True):
		antedge = AntEdge()
		if pos1 not in self:  
			if not shutup: print('Add a node at pos '+str(pos1)+' first.')
		elif pos2 not in self:  
			if not shutup: print('Add a node at pos '+str(pos2)+' first.')
		elif pos2 in self[pos1]:
			if not shutup: print('There is already an edge between '+str(pos2)+' and '+str(pos2))
		else:
			self.adj[pos1][pos2] = antedge
			self.adj[pos2][pos1] = antedge
	
	def __iter__(self):
		#be aware that this only returns an iter over the pos aka node keys in the dict
		#get the Antnode object with AG.node[pos] then
		return iter(self.node)

	def __contains__(self, n):
		try:
			return n in self.node
		except TypeError:
			return False

	def __getitem__(self, n):
		#like in networkx
		return self.adj[n]
	
	def edges(self, obj=False):
		visited = dict()
		nnodes = self.adj.items()
		for n, nodes in nnodes:
			for node in nodes:
				if node not in visited:
					if obj == False:
						yield (n,node)
					elif obj == True:
						yield self[n][node]
					else:
						print('obj should a boolean')
			visited[n] = 1
		del visited 
	
	#######happenings########
	def spawn_ant(self, amount):
		for i in range(amount):
			new_ant = Ant(self)
			self.ants.add(new_ant)
	
	def spawn_scoutant(self, amount):
		for i in range(amount):
			new_ant = ScoutAnt(self)
			self.scoutants.add(new_ant)

	
	def vaporize(self, intensity):
		for antedge in self.edges(obj=True):
			antedge.vaporize(intensity)


	#######what happens on a tic######
	def tic(self):
		for ant in self.scoutants:
			ant.decide()
		for ant in self.ants:
			ant.decide()
		for ant in self.scoutants:
			ant.move_on_tic()
		for ant in self.ants:
			ant.move_on_tic()
		self.time+=1/2

	#######what happens on a tac######
	def tac(self):
		self.vaporize(AG.VAPO_INT)
		for ant in self.scoutants:
			ant.move_on_tac()
		for ant in self.ants:
			ant.move_on_tac()
		self.time+=1/2
		if self.node[self.hq].collected == self.foodsum:
			self.finished = True

	#provide absolute pathes for these two
	#this format is easier to customize since there is no editor yet
	def read_from_file(self, path, encoding='utf-8'):
		'''
	
		firstline: nodecount edgecount graphname
		then:		n/hq position foodcount
					e position phero
		nodes before edges and exactly 1 hq pls
		no space in the tuples!


		5 4 Example
		hq (0,0) 0
		n (0,2) 30
		n (0,1) 0
		n (0,-1) 0
		n (1,0) 0
		e ((0,0),(0,1)) (0.7,0.8)
		e ((0,0),(0,-1))
		e ((0,0),(1,0))
		e ((0,1),(0,2))
		'''
		file = open(path, 'r')
		nodecount, edgecount, self.name = file.readline().split()
		for x in range(int(nodecount)):
			klass, pos, foodcount, *attr = file.readline().split()
			pos = literal_eval(pos)
			foodcount = int(foodcount)
			if klass == 'hq':
				self.add_node(pos, foodcount=foodcount, flag='hq')
			elif klass == 'n':
				self.add_node(pos, foodcount=foodcount)
			else:
				x-=1
		for x in range(int(edgecount)):	
			klass, pos, *attr = file.readline().split()
		
			pos = literal_eval(pos)
			if klass == 'e':
				self.add_edge(*pos)
				if attr:
					p = list(literal_eval(attr[0]))
					self[pos[0]][pos[1]].p = p
			else:
				x-=1

	def write_to_file(self, path, encoding='utf-8'):
		firstline = (len(self.node), len(list(self.edges())), self.name)
		file = open(path, 'w')
		file.write(' '.join(map(str, firstline))+'\n')
		for node in self:
			antnode = self.node[node]
			if type(antnode).__name__ == 'AntHQ':
				file.write(' '.join(('hq', str(node).replace(' ',''), str(antnode.collected)))+'\n')
			else:
				file.write(' '.join(('n', str(node).replace(' ',''), str(antnode.foodcount)))+'\n')
		for edge in self.edges():
			file.write(' '.join(('e', str(edge).replace(' ','')))+'\n')
		file.close()

	def rectangle(self, hq, foodplaces, x_range, y_range):
		self.name=str(len(x_range))+'x'+str(len(y_range))
		for pos in itertools.product(x_range, y_range):
			if pos in foodplaces:
				if pos == hq:
					self.add_node(pos, flag='hq', foodcount=foodplaces[pos])
				else:
					self.add_node(pos, foodcount=foodplaces[pos])
			else:
				if pos == (0,0):
					self.add_node(pos, flag='hq')
				else:
					self.add_node(pos)

		for node in self:		
			i, j = node
			self.add_edge((i,j),(i-1,j))
			self.add_edge((i,j),(i+1,j))
			self.add_edge((i,j),(i,j-1))
			self.add_edge((i,j),(i,j+1))

	def gen(self):
		foodplaces = {(5,0): 20, (0,2) : 20}	
		self.name = 'maze'
		nodes = [(0,2),(-1,1),(0,1),(1,1),(-1,0),(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(1,-1),(2,-1),(1,-2),(-2,0),(-3,1),(-3,2),(-3,3),(-3,4),(-2,4),(-1,4),(0,4),(0,3),(5,-1),(5,-2),(5,-3),(5,-4),(4,-3),(3,-3),(2,-3),(2,-2),(1,-3),(3,-1),(3,-2),(4,-2)]
		for pos in nodes:
			if pos in foodplaces:
				if pos == (-1,0):
					self.add_node(pos, flag='hq', foodcount=foodplaces[pos])
				else:
					self.add_node(pos, foodcount=foodplaces[pos])
			else:
				if pos == (-1,0):
					self.add_node(pos, flag='hq')
				else:
					self.add_node(pos)
		
		for node in self:		
			i, j = node
			self.add_edge((i,j),(i-1,j))
			self.add_edge((i,j),(i+1,j))
			self.add_edge((i,j),(i,j-1))
			self.add_edge((i,j),(i,j+1))







'''
H = AntWorld()
H.add_nodes_from(range(2))
H.add_edge(0,1)
print(H.node.__class__)
print(H[0][1].__class__)

print('---------------')


'''
