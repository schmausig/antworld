#!/usr/bin/env python3

import gi
from gi.repository import Gtk
import cairo

class AntButtonBox(Gtk.ButtonBox):

	def __init__(self, parent):
		super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		self.parent = parent
				
		#buttons
		self.animate = Gtk.CheckButton('Animate')
		self.animate.connect('toggled', self.on_animate)
		self.animate.set_active(parent.AG.player.animate)

		self.saveimg = Gtk.CheckButton('Save Img')
		self.saveimg.connect('toggled', self.on_saveimg)
		

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
		self.add(self.animate)
		self.add(self.saveimg)
		self.add(self.reset)
		self.add(self.slower)
		self.add(self.playpause)
		self.add(self.faster)
		self.set_hexpand(True)
			
	def on_playpause(self, button):
		if not self.parent.AG.finished:
			if button.get_active():
				button.set_stock_id('gtk-media-pause')
				self.parent.AG.player.play()
			else:
				button.set_stock_id('gtk-media-play')		
				self.parent.AG.player.pause()	

	def on_faster(self, button):
		self.parent.AG.player.faster()

	def on_slower(self,button):	
		self.parent.AG.player.slower()

	def on_reset(self,button):
		pass

	def on_saveimg(self,button):
		if button.get_active():
			self.parent.AG.player.set_ims()
		else:
			self.parent.AG.player.unset_ims()
	
	def on_animate(self,button):		
		if button.get_active():
			self.parent.AG.player.animate=True
		else:
			self.parent.AG.player.animate=False
			

