#!/usr/bin/env python3

import itertools
from helperfuns import *
import networkx as nx
from AntPlotter import AntPlotter
from AntNode import AntNode
from AntEdge import AntEdge

class AntWorld(nx.Graph):

	node_dict_factory = dict
	adjlist_outer_dict_factory = dict
	adjlist_inner_dict_factory = dict
	edge_attr_dict_factory = AntEdge 

	def init(self, show=False):
		if show:
			self.plotter = AntPlotter(self)
		self.clock = AntClock(self)

	def run(self):
		self.clock.run()

	def add_ant(self):
		ant = Ant(node)
def gen(w=11,h=11):

	G = AntWorld(name=str(w)+'x'+str(h))
	for coord in itertools.product(range(w),range(h)):
		attr = AntNode()
		G.add_node(coord, attr)

	for node in G:
		i, j = node
		if i > 0: 	G.add_edge((i,j),(i-1,j))
		if i < w-1: G.add_edge((i,j),(i+1,j))
		if j > 0: 	G.add_edge((i,j),(i,j-1))
		if j < h-1: G.add_edge((i,j),(i,j+1))
	G.node[(5,5)]['flag'] = 'hq'
	G.node[(9,8)]['food'] = 20

	#pathtofile = get_worlds_dir()+str(w)+'x'+str(h)+'.xml'
	#nx.write_graphml(G, pathtofile)
	return G

AW = gen(11,11)
#AW = AntWorld(data=AW) #the nx converter somehow messes sth up and doesnt consider antnode factory
AW.show()

print(AW[(0,0)][(1,0)].__class__)
print(AW.node[(0,0)].__class__)
print(AW.node.__class__)







'''
H = AntWorld()
H.add_nodes_from(range(2))
H.add_edge(0,1)
print(H.node.__class__)
print(H[0][1].__class__)

print('---------------')

'''

