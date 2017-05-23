#!/usr/bin/env python3

import threading
from multiprocessing import Process
import time
import cairo
import os
from AntConstants import RC

class AntPlayer():

	def __init__(self, AG, darea=None):
		self.process = threading.Thread(target=self.run, daemon=True)
		self.AG = AG
		self.tictactime = 1/2	
		self.playing = False
		self.darea = darea
		self.ims = None
		self.drawer = AG.drawer
		self.animate = True

	def set_ims(self):
		self.ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.darea.get_allocated_width(), self.darea.get_allocated_height())	
		#self.ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, (self.darea.drawer.AGwidth+2)*60+150, (self.darea.drawer.AGheight+2)*60)
	def unset_ims(self):
		self.ims = None
			
	def play(self, *kwargs):
		print('play')
		self.playing = True
		self.process.start()

	#important: KEYWORDS IN THIS FUNCTION CONTROL THE SPAWNING AND DRAWING OUTPUT BEHAVIOUR
	def run(self, until=100000):
		while self.playing and threading.main_thread().is_alive() and self.AG.time<until:
			print(self.AG.time)
			if self.ims and (self.AG.time % RC.saveimg_mod == 0 or self.AG.finished):
				cr = cairo.Context(self.ims)
				self.drawer.draw(self, cr)
				path = os.path.dirname(os.path.abspath(__file__))+os.sep+'log'+os.sep+self.AG.name+'_'+str(int(self.AG.time))+'.png'
				self.ims.write_to_png(path)

			if self.AG.finished:
				self.stop()
				#self.playpause.set_active(False)
				#self.playpause.set_stock_id('gtk-media-stop')
				break

			#spawning
			if RC.spawn_from <= self.AG.time and self.AG.time <= RC.spawn_until and self.AG.time % RC.spawn_mod == 0:
				self.AG.spawn_ant(RC.spawn_amount)
			if RC.sspawn_from <= self.AG.time and self.AG.time <= RC.sspawn_until and self.AG.time % RC.sspawn_mod == 0:
				self.AG.spawn_scoutant(RC.sspawn_amount)
			
			self.AG.tic()
			if self.animate and self.AG.time % RC.animate_mod == 0:
				self.darea.queue_draw()

			'''
			if savetofile == 1:
				ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.darea.get_allocated_width(), self.darea.get_allocated_height())
				cr = cairo.Context(ims)
				self.darea.on_draw(self, cr)
				path = os.path.dirname(os.path.abspath(__file__))+os.sep+'log'+os.sep+self.AG.name+'_'+str(self.AG.time)+'png'
				ims.write_to_png(path)
			'''

			if self.animate:
				time.sleep(0.3*self.tictactime)
			
			self.AG.tac()
			if self.animate and self.AG.time % RC.animate_mod == 0:
				self.darea.queue_draw()
			if self.animate:
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


