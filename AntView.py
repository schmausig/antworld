#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from AntGraph import AntGraph, gen, gen2
from AntDraw import AntDraw


import time, threading

class AntListBox(Gtk.ButtonBox):

	def __init__(self, darea):
		super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		self.darea = darea


class AntButtonBox(Gtk.ButtonBox):

	def __init__(self, darea):
		super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		self.darea = darea
		
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
		self.tictactime = 0.5
		self.timer = threading.Thread(target=self.run)
	
	def on_playpause(self, button):
		if not button.get_active():
			button.set_stock_id('gtk-media-pause')
			self.running = True
			self.timer.start()
		else:
			button.set_stock_id('gtk-media-play')
			self.running = False
			self.timer = threading.Thread(target=self.run)
	
	def on_faster(self, button):
		self.tictactime *= 11/10

	def on_slower(self,button):
		self.tictactime *= 10/11
	
	def on_reset(self,button):
		pass

			
	def run(self):
		while self.running:
			#print(self.darea.AG.time)
			self.darea.AG.tic()
			self.darea.queue_draw()
			time.sleep(0.3*self.tictactime)
			finished = self.darea.AG.tac()
			if finished:
				self.on_playpause(self.playpause)
				self.running = False
			self.darea.queue_draw()
			time.sleep(0.7*self.tictactime)

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

		self.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(1.,1.,1.,1.))
		self.set_title("AntView")
		self.set_default_size(800, 700)
		#self.maximize()

		#self.set_position(Gtk.WindowPosition.CENTER)
		self.set_redraw_on_allocate(False)
		self.connect("delete-event", self.on_delete_event)
		self.scrollwin.connect('key-press-event', self.darea.on_key_event)
		
		self.show_all()
		
	def on_delete_event(self, *args):
		self.antbuttonbox.running = False
		Gtk.main_quit(args)

def main():
	AG = gen2()
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
