#!/usr/bin/env python3

import gi
from gi.repository import Gtk, Gdk
import cairo

import math
import copy

class AV:
	
	NSIZE = 1/3
	ANTSIZE = (2/3)*NSIZE/4 #so that 4x4 ants fit on a node

	#pipewidth + #pheromones*max_pline_width should be smaller than NSIZE
	SPACING = ANTSIZE/8
	PIPEWIDTH = ANTSIZE + SPACING
	PLINE_WIDTH = NSIZE/6
	
class AntDraw(Gtk.DrawingArea):

	def __init__(self, AG):
		super().__init__()
		#gtk stuff
		self.set_vexpand(True)
		self.set_hexpand(True)
		self.connect('draw', self.on_draw)
		self.connect('realize', self.on_realize)
		self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.connect('button-press-event', self.select)
		self.connect('key-press-event', self.on_key_event)
		self.text = True

		self.AG = AG
		#boundaries of the graph (xmax,ymax,xmin,ymin)
		self.AGbbox = {'xmax': max(node[0] for node in AG),'ymax': max(node[1] for node in AG),
							'xmin': min(node[0] for node in AG),'ymin': min(node[1] for node in AG)}
		self.AGcenter = (	(self.AGbbox['xmax'] + self.AGbbox['xmin'])/2,
								(self.AGbbox['ymax'] + self.AGbbox['ymin'])/2	)
		self.AGwidth = self.AGbbox['xmax'] - self.AGbbox['xmin']
		self.AGheight = self.AGbbox['ymax'] - self.AGbbox['ymin']
		self.selected = None

			
		#self.set_size_request(500,400)
		#self.center = (self.size[0]/2, self.size[1]/2)
		#self.shift = (AV.SCALE * (-1) * self.AGbbox['xmin'] + AV.OFFSET, AV.SCALE * self.AGbbox['ymax'] + AV.OFFSET)
		
		
	def on_realize(self, wid):
		super().realize()
		#cairo stuff
		initial_scale = 100 #change this one
		initial_font_size = initial_scale/10

		#self.set_preferred_width(initial_scale*self.AGwidth)	
		#self.set_preferred_height(initial_scale*self.AGheight)
		#self.mirror_y_axis = cairo.Matrix(xx = 1, yy = -1)
		x0 = self.get_allocated_width()/2
		y0 = self.get_allocated_height()/2

		self.ctm = cairo.Matrix(xx = initial_scale, yx = 0.0, xy = 0.0, yy = -initial_scale, x0 = x0, y0 = y0)
		# x0 = self.AGcenter[0], y0 = self.AGcenter[1])
		self.ctm.translate(-self.AGcenter[0], -self.AGcenter[1])
		self.font_matrix = cairo.Matrix(xx = initial_font_size/initial_scale, yy = -initial_font_size/initial_scale)


	def on_draw(self, wid, cr):
		cr.identity_matrix()
		cr.set_font_matrix(cairo.Matrix(xx=12, yy=12))
		
		cr.rectangle(0, 0, self.get_allocated_width(), self.get_allocated_height())
		cr.set_source_rgb(0, 0, 0)
		cr.set_line_width(1)
		cr.stroke_preserve()
		cr.set_source_rgb(1, 1, 1)
		cr.fill()

		if self.text:
			cr.set_source_rgb(0, 0, 0)
			attr = ( 'Time: '+str(self.AG.time),'Antcount: '+str(len(self.AG.ants)), 'Foodsum: '+str(self.AG.foodsum),'Collected: '
					+str(self.AG.node[self.AG.hq].collected))
			for i in range(len(attr)):
				xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(attr[i])
				cr.move_to(0, (i+1)*height )
				cr.show_text(attr[i])
		

		cr.set_matrix(self.ctm)
		cr.set_font_matrix(self.font_matrix)
				
		#antgrid coords on nodes
		ngrid = self.get_grid_points(width=(2/3)*AV.NSIZE, height=(2/3)*AV.NSIZE, spacing=AV.SPACING, itemsize=AV.ANTSIZE)
		for node in self.AG: 
			self.draw_node(node, ngrid, cr)
		
		#antgrid coords on edges
		vwidth = AV.PIPEWIDTH
		vheight = 1-AV.NSIZE
		hwidth = 1-AV.NSIZE
		hheight = AV.PIPEWIDTH
		vgrid = self.get_grid_points(width=vwidth, height=vheight, spacing=AV.SPACING, itemsize=AV.ANTSIZE)
		hgrid = self.get_grid_points(width=hwidth, height=hheight, spacing=AV.SPACING, itemsize=AV.ANTSIZE)
		
		for edge in self.AG.edges():
			self.draw_edge(edge, cr, vgrid, hgrid)
		#for node in [(0,0),(0,1),(1,0)]:
		#for edge in [((0,0),(0,1)),((0,0),(1,0))]:
		#	self.draw_edge(edge, cr, vgrid, hgrid)
		

	
	def draw_node(self, node, grid, cr):
		#with our y-axis mirrored rectangles now start in the lower left corner
		antnode = self.AG.node[node]
		x,y = node
		cr.set_source_rgb(0, 0, 0)
		if node == self.selected:
			cr.set_source_rgb(1, 0.4, 0)
		cr.rectangle(x - AV.NSIZE/2, y - AV.NSIZE/2, AV.NSIZE, AV.NSIZE)
		cr.save()
		cr.identity_matrix()
		#cr.set_line_join(cairo.LINE_JOIN_ROUND) no effect?
		cr.stroke()
		cr.restore()

		
		#draw the foodbar
		if antnode.foodcount>0:
			relval = antnode.foodcount/self.AG.foodmax
			cr.set_source_rgb(*self.food_to_rgb(relval))
			cr.rectangle(	x + AV.NSIZE/4,
								y - AV.NSIZE/2,
								AV.NSIZE/4,	AV.NSIZE*relval)
			cr.fill()

		#HQ stuff
		if type(antnode).__name__ == 'AntHQ':
			cr.set_source_rgb(1, 0.4, 0)
			cr.rectangle(x - AV.NSIZE/12 , y - AV.NSIZE/12,	AV.NSIZE/6, AV.NSIZE/6);
			cr.fill()
			#draw collected food bar
			relval = antnode.collected/self.AG.foodsum
			cr.set_source_rgb(*self.food_to_rgb(relval))
			cr.rectangle(	x + AV.NSIZE/4,
								y - AV.NSIZE/2,
								AV.NSIZE/4,	AV.NSIZE*relval)
			cr.fill()

				
		#draw nodepos in the lower left corner
		cr.set_source_rgb(0, 0, 0)

		cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
		xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(str(x)+','+str(y))
		cr.move_to(	x - AV.NSIZE/2.2 + xbearing,
						y - AV.NSIZE/2.2)
		cr.show_text(str(x)+','+str(y))
		

		x_anchor = x - AV.NSIZE/2
		y_anchor = y - AV.NSIZE/6
		antcount = len(self.AG.node[node].ants)
		if antcount > grid[-1]:
			#draw antcount in the upper left corner		
			xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(str(antcount))
			cr.move_to(	x - AV.NSIZE/2.2 + xbearing,
							y + AV.NSIZE/2.2 - height)
			cr.show_text(str(antcount))
		else:
			coords = grid[0]
			for a in range(antcount):
				cr.rectangle(	x_anchor + coords[a][0],
									y_anchor + coords[a][1],
									AV.ANTSIZE, AV.ANTSIZE)
				cr.fill()
		
	def draw_edge(self, edge, cr, vgrid, hgrid):
		node1, node2 = edge
		antedge = self.AG[node1][node2]
		antcount = len(antedge.ants)
		anchor, orient = self.edge_anchor(edge)
		x,y = anchor

		
		if orient[0]==0: #vertical edge
			grid = vgrid
			width = AV.PIPEWIDTH
			height = 1-AV.NSIZE

		else: #horizontal edge
			grid = hgrid
			width = 1-AV.NSIZE
			height = AV.PIPEWIDTH

		#antpipe in black
		x_pipe_anchor = x - orient[1]*AV.PIPEWIDTH/2
		y_pipe_anchor = y - orient[0]*AV.PIPEWIDTH/2
		cr.set_source_rgb(0, 0, 0)
		cr.rectangle(	x_pipe_anchor, y_pipe_anchor,
							width, height)
		cr.save()
		cr.identity_matrix()
		cr.stroke()
		cr.restore()
		#ants in pipe
		if antcount > grid[-1]:
			#draw antcount in the upper left corner
			cr.set_source_rgb(0, 0, 0)
			xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(str(antcount))
			cr.move_to(	x + orient[0]*(1-AV.NSIZE)/2 -width/2,
							y + orient[1]*(1-AV.NSIZE)/2 -orient[1]*height/2)
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
									AV.ANTSIZE, AV.ANTSIZE)
				cr.fill()


		#pheromone lines
		cr.save()
		for p_nr in range(len(antedge.p)):
			if orient[0]==0: #vertical edge
				width = AV.PLINE_WIDTH #*antedge.p[p_nr]
				height = 1-AV.NSIZE
			else: #horizontal edge
				width = 1-AV.NSIZE
				height = AV.PLINE_WIDTH #*antedge.p[p_nr]
			cr.set_source_rgba(*self.phero_to_rgba(p_nr, antedge.p[p_nr]))
			cr.rectangle(	x + orient[1]*(self.p_nr_to_offset(p_nr) - AV.PLINE_WIDTH/2),
								y + orient[0]*(self.p_nr_to_offset(p_nr)- AV.PLINE_WIDTH/2),
								width, height)
			cr.fill()
		
		'''	
		#draw edge LINE instead of the pipe
		cr.set_source_rgb(0, 0, 0)
		cr.move_to(x,y)
		cr.rel_line_to(orient[0]*AV.NSIZE, orient[1]*AV.NSIZE)
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
		offset = AV.PIPEWIDTH/2 + AV.PLINE_WIDTH/2*(math.floor(p_nr/2)+1)
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
			anchor = (x1 + orient[0]*AV.NSIZE/2, y1 + orient[1]*AV.NSIZE/2)
		else:
			anchor = (x2 + orient[0]*AV.NSIZE/2, y2 + orient[1]*AV.NSIZE/2)
		return anchor, orient 

	def food_to_rgb(self, relval):
		
		#node colors change from green to red for a decreasing foodcount
		#i.e. a foodsource half the size is yellow
		#only the maximum of all food counts on the antworld map should be considered 100%, 
		#hence fully green, for better distinction

		red = max(-relval+1,1/2)
		green = max(1/2,relval)
		return (red, green, 0.0)
		
	def select(self, wid, event):
		if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
			#print(event.x, event.y)
			#print(self.get_window())
			#print(self.get_window().device_to_user(event.x, event.y))
			pass
			
	def on_key_event(self, wid, event):
		#print(event.keyval)
		#scroll left with h
		if event.keyval == 104:
			self.ctm.translate(1,0)
			self.queue_draw()
		#scroll up with u
		elif event.keyval == 117:
			self.ctm.translate(0,-1)
			self.queue_draw()
		#scroll right with k
		elif event.keyval == 107:
			self.ctm.translate(-1,0)
			self.queue_draw()
		#scroll down with j
		elif event.keyval == 106:
			self.ctm.translate(0,1)
			self.queue_draw()
		
		#zoom in/out with Z/z 
		if event.keyval == 90:
			self.ctm.scale(11/10,11/10)
			self.queue_draw()
		elif event.keyval == 122:
			self.ctm.scale(10/11,10/11)
			self.queue_draw()
		
		#zoom x-axis in/out with X/x 
		if event.keyval == 88:
			self.ctm.scale(11/10,1)
			self.queue_draw()
		elif event.keyval == 120:
			self.ctm.scale(10/11,1)
			self.queue_draw()
		
		#zoom y-axis in/out with Y/y
		if event.keyval == 89:
			self.ctm.scale(1,11/10)
			self.queue_draw()
		elif event.keyval == 121:
			self.ctm.scale(1,10/11)
			self.queue_draw()

