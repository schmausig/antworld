#!/usr/bin/env python3

import itertools
from helperfuns import *
import networkx as nx
import math


from AntNode import AntNode, AntHQ
from AntEdge import AntEdge
from Ant import Ant

class AG():

	VAPO_INT = 1/100

class AntGraph():

	def __init__(self, G=None, show=False, name=None):
		self.node = dict()		#dict with keys=nodeposition vals=AntNode
		self.adj  = dict()
		self.name = name
		self.ants = set()
		self.time = 0
	
	def add_node(self, pos, antnode):
		if pos not in self:
			if type(antnode).__name__ == 'AntHQ':
				self.hq = pos
			self.node[pos] = antnode
			self.adj[pos] = dict()
		else:
			print('There is already a node at pos '+str(pos))
			
	def add_edge(self, pos1, pos2, antedge=None, shutup=True):
		if not antedge:
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
	def tic(self):
		if self.time<20:
			self.spawn_ant(1)
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
		









def gen(w=11,h=11):
	G = AntGraph(name=str(w)+'x'+str(h))
	for pos in itertools.product(range(w),range(h)):
		if pos == (math.floor(w/2),math.floor(h/2)):
			antnode = AntHQ()
		else:
			antnode = AntNode()
		G.add_node(pos, antnode)

	for node in G:		
		i, j = node
		G.add_edge((i,j),(i-1,j))
		G.add_edge((i,j),(i+1,j))
		G.add_edge((i,j),(i,j-1))
		G.add_edge((i,j),(i,j+1))
	
	G.node[(9,8)].foodcount = 20

	return G

def gen2():
	G = AntGraph()
	nodes = [(0,2),(-1,1),(0,1),(1,1),(-1,0),(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(1,-1),(2,-1),(1,-2)]
	for pos in nodes:
		if pos == (1,0):
			antnode = AntHQ()
		else:
			antnode = AntNode()
		G.add_node(pos, antnode)

	for node in G:		
		i, j = node
		G.add_edge((i,j),(i-1,j))
		G.add_edge((i,j),(i+1,j))
		G.add_edge((i,j),(i,j-1))
		G.add_edge((i,j),(i,j+1))

	G.node[(5,0)].foodcount = 20
	G.node[(-1,0)].foodcount = 20
	G.node[(0,2)].foodcount = 30

	return G






'''
H = AntWorld()
H.add_nodes_from(range(2))
H.add_edge(0,1)
print(H.node.__class__)
print(H[0][1].__class__)

print('---------------')

'''

