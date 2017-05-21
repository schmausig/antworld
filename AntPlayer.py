#!/usr/bin/env python3

import threading
from multiprocessing import Process
import time
import cairo
import os
from AntDrawer import AntDrawer

class AntPlayer():

	def __init__(self, AG):
		self.process = threading.Thread(target=self.run, daemon=True)
		self.AG = AG
		self.tictactime = 1/2	
		self.playing = False
		self.darea = None
		self.drawer = AntDrawer(AG)

	def set_darea(self, darea):
		self.darea = darea
	
	def set_ims(self, ims):
		self.ims = ims
	
	def play(self, *kwargs):
		print('play')
		self.playing = True
		self.process.start()
			
	def run(self, animate_mod=1, saveimg_mod=20, spawn_mod=2, spawn_amount=4, spawn_until=20, until=100000):
		while self.playing and threading.main_thread().is_alive() and self.AG.time<until:
			if self.ims and self.AG.time % saveimg_mod == 0:
				cr = cairo.Context(self.ims)
				self.drawer.draw(self, cr)
				path = os.path.dirname(os.path.abspath(__file__))+os.sep+'log'+os.sep+self.AG.name+'_'+str(self.AG.time)+'png'
				self.ims.write_to_png(path)

			if self.AG.finished:
				self.stop()
				#self.playpause.set_active(False)
				#self.playpause.set_stock_id('gtk-media-stop')
				break

			#spawning behavior
			if spawn_until > self.AG.time and self.AG.time % spawn_mod == 0:
				ants = spawn_amount
			else:
				ants = 0
			self.AG.tic(spawnants=ants)
			if self.darea and self.AG.time % animate_mod == 0:
				self.darea.queue_draw()

			'''
			if savetofile == 1:
				ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.darea.get_allocated_width(), self.darea.get_allocated_height())
				cr = cairo.Context(ims)
				self.darea.on_draw(self, cr)
				path = os.path.dirname(os.path.abspath(__file__))+os.sep+'log'+os.sep+self.AG.name+'_'+str(self.AG.time)+'png'
				ims.write_to_png(path)
			'''

			if self.darea:
				time.sleep(0.3*self.tictactime)
			self.AG.tac()
			
			if self.darea and self.AG.time % animate_mod == 0:
				self.darea.queue_draw()
			if self.darea:
				time.sleep(0.7*self.tictactime)
		
	def pause(self):
		print('pause')
		self.playing = False
		self.process.join()
		self.process = threading.Thread(target=self.run, daemon=True)
		
	def stop(self):
		self.playing = False

	def faster(self, *button):
		self.tictactime = self.tictactime*(10/11)
		
	def slower(self, *button):
		self.tictactime = self.tictactime*(11/10)
	
	def reset(self, *button):
		pass


