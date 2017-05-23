#!/usr/bin/env python3

import cairo
import threading
import math
import copy
from AntConstants import *

class AntDrawer():
	
	def __init__(self, AG, darea=None):
		self.AG = AG
		self.darea = darea

		#boundaries of the graph (xmax,ymax,xmin,ymin)
		self.AGbbox = {'xmax': max(node[0] for node in AG),'ymax': max(node[1] for node in AG),
							'xmin': min(node[0] for node in AG),'ymin': min(node[1] for node in AG)}
		self.AGcenter = (	(self.AGbbox['xmax'] + self.AGbbox['xmin'])/2,
								(self.AGbbox['ymax'] + self.AGbbox['ymin'])/2	)
		self.AGwidth = self.AGbbox['xmax'] - self.AGbbox['xmin']
		self.AGheight = self.AGbbox['ymax'] - self.AGbbox['ymin']
		self.selected = None
		self.text = True
		self.lock = threading.Lock()
		
		initial_scale = 60
		text_offset = 200
		initial_font_size = initial_scale/10
		self.ctm = cairo.Matrix(xx = initial_scale, yx = 0.0, xy = 0.0, yy = -initial_scale, x0=text_offset+25)
		self.ctm.translate(-self.AGbbox['xmin'], -self.AGbbox['ymax']-1)
		self.font_matrix = cairo.Matrix(xx = initial_font_size/initial_scale, yy = -initial_font_size/initial_scale)

	def draw(self, wid, cr):
		self.lock.acquire()
		cr.set_matrix(self.ctm)
		cr.rectangle(self.AGbbox['xmin']-20, self.AGbbox['ymin']-20, self.AGwidth+40, self.AGheight+40)
		cr.set_source_rgb(1, 1, 1)
		cr.fill()
		cr.set_font_matrix(self.font_matrix)

		if self.text:
			cr.move_to(self.AGbbox['xmin'], self.AGbbox['ymax'])
			cr.save()
			cr.identity_matrix()
			cr.set_font_matrix(cairo.Matrix(xx=12, yy=12))

			cr.set_source_rgb(0, 0, 0)
			attr = ( 'Time: '+str(self.AG.time),
						'Antcount: '+str(len(self.AG.ants)),	
						'Scoutantcount: '+str(len(self.AG.scoutants)),
						'Foodsum: '+str(self.AG.foodsum),
						'Collected: '+str(self.AG.node[self.AG.hq].collected),
						'',
						'AG:',
						'',
						'VAPO_INT: '+str(AG.VAPO_INT),
						'',
						'A:',
						'',
						'RANDOM_FACTOR: '+str(A.RANDOM_FACTOR),
						'SEARCH_P_INT: '+str(A.SEARCH_P_INT),
						'DELIVER_P_INT: '+str(A.DELIVER_P_INT),
						'',
						'SA:',
						'',
						'RANDOM_FACTOR: '+str(SA.RANDOM_FACTOR),
						'SEARCH_P_INT: '+str(SA.SEARCH_P_INT),
						'DELIVER_P_INT: '+str(SA.DELIVER_P_INT))

			cr.rel_move_to(-200,0)
			for i in range(len(attr)):
				xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(attr[i])
				cr.show_text(attr[i])
				cr.rel_move_to(-xadvance, height+yadvance)
				if attr[i] == '':
					cr.rel_move_to(0,10)
			cr.restore()

		
		
			
		#antgrid coords on nodes
		ngrid = self.get_grid_points(width=(2/3)*AD.NSIZE, height=(2/3)*AD.NSIZE, spacing=AD.SPACING, itemsize=AD.ANTSIZE)
		for node in self.AG: 
			self.draw_node(node, ngrid, cr)
		
		#antgrid coords on edges
		vwidth = AD.PIPEWIDTH
		vheight = 1-AD.NSIZE
		hwidth = 1-AD.NSIZE
		hheight = AD.PIPEWIDTH
		vgrid = self.get_grid_points(width=vwidth, height=vheight, spacing=AD.SPACING, itemsize=AD.ANTSIZE)
		hgrid = self.get_grid_points(width=hwidth, height=hheight, spacing=AD.SPACING, itemsize=AD.ANTSIZE)
		
		for edge in self.AG.edges():
			self.draw_edge(edge, cr, vgrid, hgrid)
	
		self.lock.release()

	
	def draw_node(self, node, grid, cr):
		#with our y-axis mirrored rectangles now start in the lower left corner
		antnode = self.AG.node[node]
		x,y = node
		cr.set_source_rgb(0, 0, 0)
		if node == self.selected:
			cr.set_source_rgb(1, 0.4, 0)
		cr.rectangle(x - AD.NSIZE/2, y - AD.NSIZE/2, AD.NSIZE, AD.NSIZE)
		cr.save()
		cr.identity_matrix()
		cr.set_line_width(1)
		#cr.set_line_join(cairo.LINE_JOIN_ROUND) #NO EFFECT :(
		#HQ stuff
		cr.set_source_rgb(0, 0, 0)
		if node == self.AG.hq:
			cr.stroke_preserve()
			cr.restore()
			cr.set_source_rgb(0.92, 0.84, 0.43)
			cr.fill()

			#draw collected food bar
			relval = antnode.collected/self.AG.foodsum
			cr.set_source_rgb(*self.food_to_rgb(relval))
			cr.rectangle(	x + AD.NSIZE/4,
								y - AD.NSIZE/2,
								AD.NSIZE/4,	AD.NSIZE*relval)
			cr.fill()
		else:
			cr.stroke()
			cr.restore()

		#draw the foodbar
		if antnode.foodcount>0:
			relval = antnode.foodcount/self.AG.foodmax
			cr.set_source_rgb(*self.food_to_rgb(relval))
			cr.rectangle(	x + AD.NSIZE/4,
								y - AD.NSIZE/2,
								AD.NSIZE/4,	AD.NSIZE*relval)
			cr.fill()

					
		#draw nodepos in the lower left corner
		cr.set_source_rgb(0, 0, 0)

		cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
		xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(str(x)+','+str(y))
		cr.move_to(	x - AD.NSIZE/2.2 + xbearing,
						y - AD.NSIZE/2.2)
		cr.show_text(str(x)+','+str(y))
		

		x_anchor = x - AD.NSIZE/2
		y_anchor = y - AD.NSIZE/6
		antcount = len(antnode.ants)
		scoutantcount = len(antnode.scoutants)
		if antcount+scoutantcount > grid[-1]:
			#draw antcount in the upper left corner		
			xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(str(antcount))
			cr.move_to(	x - AD.NSIZE/2.2 + xbearing,
							y + AD.NSIZE/2.2 - height)
			cr.show_text(str(antcount))
		else:
			coords = grid[0]
			for a in range(antcount):
				cr.set_source_rgb(0, 0, 0)
				cr.rectangle(	x_anchor + coords[a][0],
									y_anchor + coords[a][1],
									AD.ANTSIZE, AD.ANTSIZE)
				cr.fill()
			for s in range(antcount,antcount+scoutantcount):
				cr.set_source_rgb(1, 0, 1)
				cr.rectangle(	x_anchor + coords[s][0],
									y_anchor + coords[s][1],
									AD.ANTSIZE, AD.ANTSIZE)
				cr.fill()

		
	def draw_edge(self, edge, cr, vgrid, hgrid):
		node1, node2 = edge
		antedge = self.AG[node1][node2]
		antcount = len(antedge.ants)
		anchor, orient = self.edge_anchor(edge)
		x,y = anchor

		
		if orient[0]==0: #vertical edge
			grid = vgrid
			width = AD.PIPEWIDTH
			height = 1-AD.NSIZE

		else: #horizontal edge
			grid = hgrid
			width = 1-AD.NSIZE
			height = AD.PIPEWIDTH

		#antpipe in black
		x_pipe_anchor = x - orient[1]*AD.PIPEWIDTH/2
		y_pipe_anchor = y - orient[0]*AD.PIPEWIDTH/2
		cr.rectangle(	x_pipe_anchor, y_pipe_anchor,
							width, height)
		cr.save()
		cr.identity_matrix()
		cr.set_source_rgb(0, 0, 0)
		cr.set_line_width(1)
		cr.stroke()
		cr.restore()
		#ants in pipe
		if antcount > grid[-1]:
			#draw antcount in the upper left corner
			cr.set_source_rgb(0, 0, 0)
			xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(str(antcount))
			cr.move_to(	x + orient[0]*(1-AD.NSIZE)/2 -width/2,
							y + orient[1]*(1-AD.NSIZE)/2 -orient[1]*height/2)
			cr.show_text(str(antcount))
		else:
			coords = []
			uncentered_coords = grid[0]
			middle = math.floor(grid[-1]/2)
			for zipped in zip(reversed(uncentered_coords[:middle]), uncentered_coords[middle:2*middle]):
				for zipp in zipped:
					coords.append(zipp)
			if len(uncentered_coords)%2 == 1:
				coords = append(uncentered_coords[-1])
			for a in range(antcount):
				cr.rectangle(	x_pipe_anchor + coords[a][0],
									y_pipe_anchor + coords[a][1],
									AD.ANTSIZE, AD.ANTSIZE)
				cr.fill()


		#pheromone lines
		for p_nr in range(len(antedge.p)):
			if orient[0]==0: #vertical edge
				width = AD.PLINE_WIDTH #*antedge.p[p_nr]
				height = 1-AD.NSIZE
			else: #horizontal edge
				width = 1-AD.NSIZE
				height = AD.PLINE_WIDTH #*antedge.p[p_nr]
			cr.set_source_rgba(*self.phero_to_rgba(p_nr, antedge.p[p_nr]))
			cr.rectangle(	x + orient[1]*(self.p_nr_to_offset(p_nr) - AD.PLINE_WIDTH/2),
								y + orient[0]*(self.p_nr_to_offset(p_nr)- AD.PLINE_WIDTH/2),
								width, height)
			cr.fill()
		
		'''	
		#draw edge LINE instead of the pipe
		cr.set_source_rgb(0, 0, 0)
		cr.move_to(x,y)
		cr.rel_line_to(orient[0]*AD.NSIZE, orient[1]*AD.NSIZE)
		cr.save()
		cr.identity_matrix()
		cr.stroke()
		cr.restore()

		'''
	def get_grid_points(self, width, height, spacing, itemsize):
		act_itemsize = itemsize + spacing
		x_cap = math.floor(width/act_itemsize)
		y_cap = math.floor(height/act_itemsize)
		cap = x_cap*y_cap
		x_offset = (width/act_itemsize - y_cap)*act_itemsize
		y_offset = (height/act_itemsize - y_cap)*act_itemsize
		coords = []
		for x in range(x_cap):
			for y in range(y_cap-1, -1, -1):
				coords.append((act_itemsize*x + spacing/2, act_itemsize*y + spacing/2))
		return (coords, x_offset, y_offset, cap)



	def p_nr_to_offset(self, p_nr):
		offset = AD.PIPEWIDTH/2 + AD.PLINE_WIDTH/2*(math.floor(p_nr/2)+1)
		if p_nr % 2 == 0:
			offset = (-1)*offset
		return offset

	def phero_to_rgba(self, p_nr, int):
		if p_nr == 0:
			return (1, 0, 0, int)
		elif p_nr == 1:
			return (0, 1, 0, int)
		elif p_nr == 2:
			return (0, 0, 1, int)
		elif p_nr == 3:
			return (0, 1, 1, int)


	def edge_anchor(self, edge): 
		# we draw bottom up or left to right
		node1, node2 = edge
		x1, y1 = node1
		x2, y2 = node2
		diff = (x1 - x2, y1 - y2) #one of these is always ZERO
		orient = (abs(diff[0]),abs(diff[1]))
		if -1 in diff:
			anchor = (x1 + orient[0]*AD.NSIZE/2, y1 + orient[1]*AD.NSIZE/2)
		else:
			anchor = (x2 + orient[0]*AD.NSIZE/2, y2 + orient[1]*AD.NSIZE/2)
		return anchor, orient 

	def food_to_rgb(self, relval):
		
		#node colors change from green to red for a decreasing foodcount
		#i.e. a foodsource half the size is yellow
		#only the maximum of all food counts on the antworld map should be considered 100%, 
		#hence fully green, for better distinction

		red = max(-relval+1,1/2)
		green = max(1/2,relval)
		return (red, green, 0.0)

	def translate(self, x, y):
		self.lock.acquire()
		self.ctm.translate(x,y)
		self.lock.release()  #these locks dont help ;(

	def scale(self, x, y):
		self.lock.acquire()
		self.ctm.scale(x,y)
		self.lock.release()



