#!/usr/bin/env python3

from AntGraph import gen
import cairo

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


