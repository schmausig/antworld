#built with
python3/yakkety,now 3.5.1-4 amd64 [installed]
python3-cairo/yakkety,now 1.10.0+dfsg-5build1 amd64 [installed]
python3-gi/yakkety,now 3.22.0-1 amd64 [installed]

execute AntView.py
 

scroll with
	
   u
h  j  k

zoom in/out with Z/z 	
zoom x-axis in/out with X/x 
zoom y-axis in/out with Y/y



#to make the src look better:
set softtabstop=3
set tabstop=3
set shiftwidth=3
(those are vim commands (USE THE BEST TEXT EDITOR: VIM!))



u might notice some instabilities(especially if you accelerate too much):
possible reasons:
	the implementation is not threadsafe (gtk messes that up?)
		this might be because we do not handle enough via gtk signals
	where to put the threading locks?

if you are familiar with gtk+ and/or pycairo i'd be thankful if you got some advice

