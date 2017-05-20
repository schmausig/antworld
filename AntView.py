#!/usr/bin/env python3

import os
import time, threading

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo

from AntGraph import AntGraph, gen, gen2
from AntDraw import AntDraw
import sys
from helperfuns import *


class AntListBox(Gtk.ListBox):

	def __init__(self, darea):
		super().__init__()
		self.darea = darea


class AntButtonBox(Gtk.ButtonBox):

	def __init__(self, darea):
		super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		self.darea = darea
		self.AG = darea.AG
		
		#buttons
		self.reset = Gtk.ToolButton()
		self.reset.set_stock_id('gtk-media-previous')
		self.reset.connect('clicked', self.on_reset)

		self.slower = Gtk.ToolButton()
		self.slower.set_stock_id('gtk-media-rewind')
		self.slower.connect('clicked', self.on_slower)
		self.playpause = Gtk.ToggleToolButton()
		self.playpause.set_stock_id('gtk-media-play')
		self.playpause.connect('toggled', self.on_playpause)
		self.faster = Gtk.ToolButton()
		self.faster.set_stock_id('gtk-media-forward')
		self.faster.connect('clicked', self.on_faster)
		
		self.set_layout(Gtk.ButtonBoxStyle.CENTER)
		self.add(self.reset)
		self.add(self.slower)
		self.add(self.playpause)
		self.add(self.faster)
		self.set_hexpand(True)
		self.tictactime = 1/2
		self.timer = threading.Thread(target=self.run)
	
	def on_playpause(self, button):
		if not self.AG.finished:
			if button.get_active():
				button.set_stock_id('gtk-media-pause')
				self.timer.start()
			else:
				button.set_stock_id('gtk-media-play')		
				self.timer = threading.Thread(target=self.run)

	def on_faster(self, button):
		self.tictactime = self.tictactime*(10/11)

	def on_slower(self,button):
		self.tictactime = self.tictactime*(11/10)
	
	def on_reset(self,button):
		pass

			
	def run(self, animate=1, savetofile=0):
		while self.playpause.get_active() and not self.AG.finished:
			if savetofile >= 1/2:
				ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.darea.get_allocated_width(), self.darea.get_allocated_height())
				cr = cairo.Context(ims)
				self.darea.on_draw(self, cr)
				path = os.path.dirname(os.path.abspath(__file__))+os.sep+'log'+os.sep+self.AG.name+'_'+str(self.AG.time)+'png'
				ims.write_to_png(path)

			self.AG.tic()
			if animate == 1/2:
				self.darea.queue_draw()
			'''
			if savetofile == 1:
				ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.darea.get_allocated_width(), self.darea.get_allocated_height())
				cr = cairo.Context(ims)
				self.darea.on_draw(self, cr)
				path = os.path.dirname(os.path.abspath(__file__))+os.sep+'log'+os.sep+self.AG.name+'_'+str(self.AG.time)+'png'
				ims.write_to_png(path)
			'''

			time.sleep(0.3*self.tictactime)
			self.AG.tac()
			if animate >= 1/2:
				self.darea.queue_draw()
			
			time.sleep(0.7*self.tictactime)
			if self.darea.AG.finished:
				self.playpause.set_active(False)
				self.playpause.set_stock_id('gtk-media-stop')
				if savetofile >= 1/2:	
					self.darea.on_draw(self, cr)
					path = os.path.dirname(os.path.abspath(__file__))+os.sep+'log'+os.sep+self.AG.name+'_'+str(self.AG.time)+'png'
					ims.write_to_png(path)


class AntView(Gtk.Window):

	def __init__(self, AG):
		super().__init__()
		self.darea = AntDraw(AG)
		self.antbuttonbox = AntButtonBox(self.darea)
		self.scrollwin = Gtk.ScrolledWindow()
		self.scrollwin.add_with_viewport(self.darea)
		self.scrollwin.set_vexpand(True)
		self.scrollwin.set_hexpand(True)
		self.scrollwin.props.hscrollbar_policy = Gtk.PolicyType.NEVER
		self.scrollwin.props.vscrollbar_policy = Gtk.PolicyType.NEVER
		self.antlistbox = AntListBox(self.darea)
		self.grid = Gtk.Grid()
		self.grid.set_vexpand(True)
		self.grid.set_hexpand(True)
		self.grid.attach(self.antlistbox, 0, 0, 1, 1)
		self.grid.attach(self.scrollwin, 1, 0, 1, 1)
		self.grid.attach(self.antbuttonbox, 1, 1, 1, 1)
		self.add(self.grid)

		#self.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1.,1.,1.,1.))
		self.set_title("AntView")
		self.set_default_size(800, 700)
		#self.maximize()

		#self.set_position(Gtk.WindowPosition.CENTER)
		self.set_redraw_on_allocate(False)
		self.connect("delete-event", self.on_delete_event)
		self.scrollwin.connect('key-press-event', self.darea.on_key_event)
		
		self.show_all()
		
	def on_delete_event(self, *args):
		self.antbuttonbox.playpause.set_active(False)
		Gtk.main_quit(args)

def main():
	AG = AntGraph()
	#AG2 = gen2()
	AG3 = gen(w=range(-5,6), h=range(-5,6))
	#AG2.write_to_file(os.path.dirname(os.path.abspath(__file__))+os.sep+'worlds'+os.sep+AG2.name+'.antgraph')
	AG3.write_to_file(os.path.dirname(os.path.abspath(__file__))+os.sep+'worlds'+os.sep+AG3.name+'.antgraph')

	path = os.path.dirname(os.path.abspath(__file__))+os.sep+'worlds'+os.sep+'Example'+'.antgraph'
	AG.read_from_file(path)
	antview = AntView(AG)
	Gtk.main()

if __name__ == "__main__":    
	main()


'''
print('myrect', self.get_allocation().x, self.get_allocation().y, self.get_allocation().width, self.get_allocation().height)
		print('darea', darea.get_allocation().x, darea.get_allocation().y, darea.get_allocation().width, darea.get_allocation().height)
		print('scrolwindow', scrollwindow.get_allocation().x, scrollwindow.get_allocation().y, scrollwindow.get_allocation().width, scrollwindow.get_allocation().height)
		print(darea.get_parent_window())
'''
