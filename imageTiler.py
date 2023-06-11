#this script is designed to make tiles from any input image


# importing functions
import sys
import os
import math
from PIL import Image

# source path
img_path = sys.argv[1]

#output tile directory
tile_path = 'tiles'

# tile size
tile_size = 256

# ajust image size to tile size
def adjustImage(src_img):
	#get image size
	img_w , img_h = src_img.size
	
	# calculate tilable img size
	out_w = img_w + (tile_size - img_w % tile_size)
	out_h = img_h + (tile_size - img_h % tile_size)
	
	# create transparent  extra background
	out_img = Image.new('RGBA', (out_w, out_h))
	
	# combine src image and background
	out_img.paste(src_img, (0,0))
	
	return out_img
	
img = Image.open(img_path)
w, h = img.size[0], img.size[1]	


# calculate max zoom level
max_zoom = int(math.ceil(math.log((max(w , h)/ tile_size), 2)))

#main loop for all zoom levels
for z in range (max_zoom, -1, -1):
	#adjusting image
	adj_img = adjustImage(img)
	#calculating number of rows and columns of tiles
	n_cols = int(adj_img.size[0] / tile_size)
	n_rows = int(adj_img.size[1] / tile_size)
	# print(n_cols,n_rows)
	#loop for creating directories and tiles
	for x in range (n_cols):
		
		# create z/x directory
		path = os.path.join(tile_path, str(z), str(x))
		if not os.path.isdir(path):
			os.makedirs(path)
		
		# cut tiles
		for y in range (n_rows):
			bounds = (x * tile_size, y * tile_size , (x + 1)* tile_size, (y + 1)* tile_size)
			tile = adj_img.crop(bounds)
			tile.save('%s/%s.png' % (path,y))
	
	# resize image - go to next zoom level
	w, h = img.size[0] , img.size[1]
	img = img.resize((int(w/2), int(h/2)), Image.ANTIALIAS)