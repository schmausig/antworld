#!/usr/bin/env python3

import os
import time, threading
from multiprocessing import Process

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
from AntButtonBox import AntButtonBox

from AntGraph import AntGraph
from AntDarea import AntDarea
import sys
from helperfuns import *

class AntListBox(Gtk.ListBox):

	def __init__(self, darea):
		super().__init__()
		self.darea = darea


class AntView(Gtk.Window):

	def __init__(self):
		super().__init__()
		self.darea = AntDarea(self)

		path = get_worlds_dir()+'12x12_maze'+'.antgraph'
		self.AG = AntGraph(path=path, darea=self.darea)
		#self.AG = AntGraph(darea=self.darea, hq=None, foodplaces=None, x_range=None, y_range=None, gen=True) 
	#	self.AG = AntGraph(darea=self.darea, hq=(0,0), foodplaces={(5,5) : 300, (-5,5) : 300, (0,-5) : 200}, x_range=range(-5,7), y_range=range(-5,7)) 
		
		self.antbuttonbox = AntButtonBox(self)
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
		self.grid.attach(self.antlistbox, 0, 1, 1, 1)
		self.grid.attach(self.scrollwin, 1, 1, 1, 1)
		self.grid.attach(self.antbuttonbox, 1, 2, 1, 1)

		self.init_menubar()

		self.set_title("AntView")
		self.set_default_size(920, 680)
		#self.maximize()

		#self.set_position(Gtk.WindowPosition.CENTER)
		self.set_redraw_on_allocate(False)
		self.connect("delete-event", self.on_delete_event)
		self.scrollwin.connect('key-press-event', self.darea.on_key_event)
		
		
		self.add(self.grid)
		self.show_all()

	def init_menubar(self):
		action_group = Gtk.ActionGroup("my_actions")
		
		#self.add_file_menu_actions(action_group)
		#self.add_edit_menu_actions(action_group)
		
	
		menubar = Gtk.MenuBar()

		#the filemenu
		filemenu = Gtk.MenuItem("File")
		filem = Gtk.Menu()
		filemenu.set_submenu(filem)
		fileopen = Gtk.MenuItem("Open File")
		fileopen.connect("activate", self.on_filemenu_open)
		filesave = Gtk.MenuItem("Save File")
		filesave.connect("activate", self.on_filemenu_save)

		filequit = Gtk.MenuItem("Quit")
		filequit.connect("activate", self.on_delete_event)

		filem.append(fileopen)
		filem.append(filesave)
		filem.append(Gtk.SeparatorMenuItem())
		filem.append(filequit)
		
		menubar.append(filemenu)
		#menubar.pack_start(menub, True, True, 1)
		self.grid.attach(menubar, 0, 0, 2, 1)
		
	def on_filemenu_open(self, widget):
		fcd = Gtk.FileChooserDialog(Gtk.FileChooserAction.OPEN)
		fcd.add_button("Open", Gtk.ResponseType.OK)
		fcd.set_current_folder(get_worlds_dir())

		response = fcd.run()
		if response == Gtk.ResponseType.OK:
			filename = fcd.get_filename()
			self.AG = AntGraph(path=filename, darea=self.darea)
			self.darea.connect("draw", self.AG.drawer.draw)
			self.darea.queue_draw()
		fcd.destroy()

	def on_filemenu_save(self, widget):
		fsd = Gtk.FileChooserDialog("Save File", self, Gtk.FileChooserAction.SAVE)
		fsd.add_button("Save", Gtk.ResponseType.OK)
		fsd.set_current_folder(get_worlds_dir())
		fsd.set_current_name(self.AG.name+'.antgraph')
		response = fsd.run()
		if response == Gtk.ResponseType.OK:
			filename = fsd.get_filename()
			self.AG.write_to_file(filename)
		fsd.destroy()

	
	def on_delete_event(self, *args):
		self.AG.player.stop()
		Gtk.main_quit(args)

def main():
	
	#AG = gen({(3,3): 10}, w=range(-1,4), h=range(-1,4))
	#AG = gen({(-5,-5): 20, (5,5) : 20}, w=range(-5,6), h=range(-5,6))
	#AG = gen({(-10,-8): 20, (8,10) : 20, (9,7): 30}, w=range(-10,11), h=range(-10,11))
	
	#AG = gen({(9,9): 500}, w=range(-1,11), h=range(-1,11))
	#AG = gen({(5,5): 400}, w=range(-1,7), h=range(-1,7))

	
			
	#AG.write_to_file(os.path.dirname(os.path.abspath(__file__))+os.sep+'worlds'+os.sep+AG.name+'.antgraph')
	antview = AntView()
	
	Gtk.main()
	#ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, (antview.darea.drawer.AGwidth+2)*60+150, (antview.darea.drawer.AGheight+2)*60)

	#AG.init_player()
	#AG.player.set_ims(ims)
	#AG.player.play()
	#AG.player.process.join()

if __name__ == "__main__":    
	main()


'''
print('myrect', self.get_allocation().x, self.get_allocation().y, self.get_allocation().width, self.get_allocation().height)
		print('darea', darea.get_allocation().x, darea.get_allocation().y, darea.get_allocation().width, darea.get_allocation().height)
		print('scrolwindow', scrollwindow.get_allocation().x, scrollwindow.get_allocation().y, scrollwindow.get_allocation().width, scrollwindow.get_allocation().height)
		print(darea.get_parent_window())
'''
