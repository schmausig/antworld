#!/usr/bin/env python3

import gi
from gi.repository import Gtk, Gdk

import cairo
from AntDrawer import AntDrawer

class AntDarea(Gtk.DrawingArea):

	def __init__(self, AG):
		super().__init__()
		#gtk stuff
		self.AG = AG
		self.set_vexpand(True)
		self.set_hexpand(True)
		
		self.connect('realize', self.on_realize)
		self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
		self.connect('button-press-event', self.select)
		self.connect('key-press-event', self.on_key_event)
		
	def on_realize(self, wid):
		super().realize()	
		self.drawer = AntDrawer(self.AG, darea=self)
		self.connect('draw', self.drawer.draw)
		
		#self.set_preferred_width(initial_scale*self.AGwidth)	
		#self.set_preferred_height(initial_scale*self.AGheight)
		#self.mirror_y_axis = cairo.Matrix(xx = 1, yy = -1)
		
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
			self.drawer.translate(1,0)
			self.queue_draw()
		#scroll up with u
		elif event.keyval == 117:
			self.drawer.translate(0,-1)
			self.queue_draw()
		#scroll right with k
		elif event.keyval == 107:
			self.drawer.translate(-1,0)
			self.queue_draw()
		#scroll down with j
		elif event.keyval == 106:
			self.drawer.translate(0,1)
			self.queue_draw()
		
		#zoom in/out with Z/z 
		if event.keyval == 90:
			self.drawer.scale(11/10,11/10)
			self.queue_draw()
		elif event.keyval == 122:
			self.drawer.scale(10/11,10/11)
			self.queue_draw()
		
		#zoom x-axis in/out with X/x 
		if event.keyval == 88:
			self.drawer.scale(11/10,1)
			self.queue_draw()
		elif event.keyval == 120:
			self.drawer.ctm.scale(10/11,1)
			self.queue_draw()
		
		#zoom y-axis in/out with Y/y
		if event.keyval == 89:
			self.drawer.scale(1,11/10)
			self.queue_draw()
		elif event.keyval == 121:
			self.drawer.scale(1,10/11)
			self.queue_draw()
	

