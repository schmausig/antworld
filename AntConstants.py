#!/usr/bin/env python3

__all__= ['AD', 'A', 'SA', 'AG', 'RC']

class AD:
	#FOR THE DRAWER
	NSIZE = 1/3
	ANTSIZE = (2/3)*NSIZE/3 #so that 3x3 ants fit on a node

	#pipewidth + #pheromones*max_pline_width should be smaller than NSIZE
	SPACING = ANTSIZE/8 #spacing between ants
	PIPEWIDTH = ANTSIZE + SPACING
	PLINE_WIDTH = NSIZE/6

class A():
	#for ants
	RANDOM_FACTOR = 1/100 #this must be > 0 to avoid division by zero and smaller for bigger 'alpha'
	SEARCH_P_INT = 1/100 #intensity of search pheromone between 0 and 1
	DELIVER_P_INT = 1/100	#intensity of deliver pheromone

class SA():
	#for scoutants
	RANDOM_FACTOR = 1/50 #this must be > 0 to avoid division by zero and smaller for bigger 'alpha'
	SEARCH_P_INT = 1/100 #intensity of search pheromone between 0 and 1
	DELIVER_P_INT = 1/100	#intensity of deliver pheromone

class AG():

	VAPO_INT = 1/1200

class RC():
	animate_mod=5
	saveimg_mod=50
	#spawning behaviour for ants
	spawn_mod=1
	spawn_amount=1 
	spawn_from=0 
	spawn_until=50
	#spawning behaviour for scoutants
	sspawn_mod=1
	sspawn_amount=0
	sspawn_from=0
	sspawn_until=2
	
