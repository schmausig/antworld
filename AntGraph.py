#!/usr/bin/env python3

import math
from ast import literal_eval
import itertools

from AntNode import AntNode, AntHQ
from AntEdge import AntEdge
from Ant import Ant
from AntPlayer import AntPlayer


class AG():

	VAPO_INT = 1/250

class AntGraph():

	def __init__(self, name=None):
		self.node = dict()		#dict with keys=nodeposition vals=AntNode
		self.adj  = dict()
		self.name = name
		self.ants = set()
		self.time = 0
		self.foodmax = 0
		self.foodsum = 0
		self.finished = False
		
	def init_player(self):
		self.player = AntPlayer(self)

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
	def spawn_ant(self, nr):
		for i in range(nr):
			new_ant = Ant(self)
			self.ants.add(new_ant)
	
	def vaporize(self, intensity):
		for antedge in self.edges(obj=True):
			antedge.vaporize(intensity)


	#######what happens on a tic######
	def tic(self, spawnants=0):
		self.spawn_ant(spawnants)
		for ant in self.ants:
			ant.decide()
		for ant in self.ants:
			ant.move_on_tic()
		self.time+=1/2

	#######what happens on a tac######
	def tac(self):
		self.vaporize(AG.VAPO_INT)
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
		then: class position foodcount
		nodes before edges and exactly 1 hq pls


		5 4 Example
		hq (0,0) 0
		n (0,2) 30
		n (0,1) 0
		n (0,-1) 0
		n (1,0) 0
		e ((0,0),(0,1))
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







def gen(foodplaces, w=range(-2,3),h=range(-2,3)):
	G = AntGraph(name=str(len(w))+'x'+str(len(h)))
	for pos in itertools.product(w,h):
		if pos in foodplaces:
			if pos == (0,0):
				G.add_node(pos, flag='hq', foodcount=foodplaces[pos])
			else:
				G.add_node(pos, foodcount=foodplaces[pos])
		else:
			if pos == (0,0):
				G.add_node(pos, flag='hq')
			else:
				G.add_node(pos)

		

	for node in G:		
		i, j = node
		G.add_edge((i,j),(i-1,j))
		G.add_edge((i,j),(i+1,j))
		G.add_edge((i,j),(i,j-1))
		G.add_edge((i,j),(i,j+1))
	
	return G

def gen2():
	foodplaces ={(5,0): 20, (0,2) : 20}	
	G = AntGraph(name='Custom')
	nodes = [(0,2),(-1,1),(0,1),(1,1),(-1,0),(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(1,-1),(2,-1),(1,-2)]
	for pos in nodes:
		if pos in foodplaces:
			if pos == (-1,0):
				G.add_node(pos, flag='hq', foodcount=foodplaces[pos])
			else:
				G.add_node(pos, foodcount=foodplaces[pos])
		else:
			if pos == (-1,0):
				G.add_node(pos, flag='hq')
			else:
				G.add_node(pos)
	

	for node in G:		
		i, j = node
		G.add_edge((i,j),(i-1,j))
		G.add_edge((i,j),(i+1,j))
		G.add_edge((i,j),(i,j-1))
		G.add_edge((i,j),(i,j+1))

	return G







'''
H = AntWorld()
H.add_nodes_from(range(2))
H.add_edge(0,1)
print(H.node.__class__)
print(H[0][1].__class__)

print('---------------')


'''
