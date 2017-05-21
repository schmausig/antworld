#!/usr/bin/env python3

import os
import time, threading
from multiprocessing import Process

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo

from AntGraph import AntGraph, gen, gen2
#from AntDraw import AntDraw
from AntDarea import AntDarea
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
		self.AG.player.set_darea(darea)
		
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
				
	def on_playpause(self, button):
		if not self.AG.finished:
			if button.get_active():
				button.set_stock_id('gtk-media-pause')
				self.AG.player.play()
			else:
				button.set_stock_id('gtk-media-play')		
				self.AG.player.pause()	
	def on_faster(self, button):
		self.AG.player.faster()

	def on_slower(self,button):	
		self.AG.player.slower()

	def on_reset(self,button):
		pass

			
class AntView(Gtk.Window):

	def __init__(self, AG):
		super().__init__()
		self.darea = AntDarea(AG)
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
		#self.set_redraw_on_allocate(False)
		self.connect("delete-event", self.on_delete_event)
		self.scrollwin.connect('key-press-event', self.darea.on_key_event)
		
		self.show_all()
		
	def on_delete_event(self, *args):
		self.darea.AG.player.stop()
		Gtk.main_quit(args)

def main():
	
	#AG = gen({(3,3): 10}, w=range(-1,4), h=range(-1,4))
	#AG = gen({(-5,-5): 20, (5,5) : 20}, w=range(-5,6), h=range(-5,6))
	#AG = gen({(-10,-8): 20, (8,10) : 20, (9,7): 30}, w=range(-10,11), h=range(-10,11))
	
	#AG = gen({(9,9): 500}, w=range(-1,11), h=range(-1,11))
	AG = gen({(5,5): 500, (2,2): 500}, w=range(-1,7), h=range(-1,7))

	
	
	#AG = AntGraph()
	#path = os.path.dirname(os.path.abspath(__file__))+os.sep+'worlds'+os.sep+'standardsize'+'.antgraph'
	#AG.read_from_file(path)
	
	#AG.write_to_file(os.path.dirname(os.path.abspath(__file__))+os.sep+'worlds'+os.sep+AG.name+'.antgraph')
	#antview = AntView(AG)
	#Gtk.main()
	ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, 800, 700)
	AG.init_player()
	AG.player.set_ims(ims)
	AG.player.play()
	AG.player.process.join()

if __name__ == "__main__":    
	main()


'''
print('myrect', self.get_allocation().x, self.get_allocation().y, self.get_allocation().width, self.get_allocation().height)
		print('darea', darea.get_allocation().x, darea.get_allocation().y, darea.get_allocation().width, darea.get_allocation().height)
		print('scrolwindow', scrollwindow.get_allocation().x, scrollwindow.get_allocation().y, scrollwindow.get_allocation().width, scrollwindow.get_allocation().height)
		print(darea.get_parent_window())
'''
