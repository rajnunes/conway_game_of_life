import json
import numpy as np

# setting up the values for the grid
ON=255
OFF=0
vals=[ON,OFF]


def randomGrid(heigth,width):
	"""returns a grid of NxN random values"""
	return np.random.choice(vals,heigth*width,p=[0.2,0.8]).reshape(heigth,width)


def addGlider(i,j,grid):
	"""adds a glider with top left cell at (i, j)"""
	glider=np.array([[0,0,255],
					 [255,0,255],
					 [0,255,255]])
	grid[i:i+3,j:j+3]=glider


def addGosperGliderGun(i,j,grid):
	"""adds a Gosper Glider Gun with top left
	   cell at (i, j)"""
	gun=np.zeros(11*38).reshape(11,38)
	
	gun[5][1]=gun[5][2]=255
	gun[6][1]=gun[6][2]=255
	
	gun[3][13]=gun[3][14]=255
	gun[4][12]=gun[4][16]=255
	gun[5][11]=gun[5][17]=255
	gun[6][11]=gun[6][15]=gun[6][17]=gun[6][18]=255
	gun[7][11]=gun[7][17]=255
	gun[8][12]=gun[8][16]=255
	gun[9][13]=gun[9][14]=255
	
	gun[1][25]=255
	gun[2][23]=gun[2][25]=255
	gun[3][21]=gun[3][22]=255
	gun[4][21]=gun[4][22]=255
	gun[5][21]=gun[5][22]=255
	gun[6][23]=gun[6][25]=255
	gun[7][25]=255
	
	gun[3][35]=gun[3][36]=255
	gun[4][35]=gun[4][36]=255
	
	grid[i:i+11,j:j+38]=gun


def update(grid,heigth,width):
	# copy grid since we require 8 neighbors
	# for calculation and we go line by line
	newGrid=grid.copy()
	for i in range(heigth):
		for j in range(width):
			
			# compute 8-neghbor sum
			# using toroidal boundary conditions - x and y wrap around
			# so that the simulaton takes place on a toroidal surface.
			total=int((grid[i,(j-1)%width]+grid[i,(j+1)%width]+
					   grid[(i-1)%heigth,j]+grid[(i+1)%heigth,j]+
					   grid[(i-1)%heigth,(j-1)%width]+grid[(i-1)%heigth,(j+1)%width]+
					   grid[(i+1)%heigth,(j-1)%width]+grid[(i+1)%heigth,(j+1)%width])/255)
			
			# apply Conway's rules
			if grid[i,j]==ON:
				if (total<2) or (total>3):
					newGrid[i,j]=OFF
			else:
				if total==3:
					newGrid[i,j]=ON
	
	# update data
	# img.set_data(newGrid)
	grid[:]=newGrid[:]
	print(newGrid)


def main():
	with open('setup.json','r') as f:
		array=json.load(f)
	
	print(array['game'])
	heigth=array['game'][0]['heigth']
	width=array['game'][0]['width']
	iteration=array['game'][0]['iteration']
	gosper=array['game'][0]['gosper']
	interval=array['game'][0]['interval']#update interval
	mov_file=array['game'][0]['mov-file']
	glider=array['game'][0]['glider']
	
	# declare grid
	grid=np.array([])
	# print(type(gosper))
	if glider is True:
		grid=np.zeros(heigth*width).reshape(heigth,width)
		addGlider(1,1,grid)
	elif gosper is True:
		grid=np.zeros(heigth*width).reshape(heigth,width)
		addGosperGliderGun(10,10,grid)
	
	else:   # populate grid with random on/off -
		# more off than on
		grid=randomGrid(heigth,width)
	for i in range(1,iteration):
		update(grid,heigth,width)


if __name__=='__main__':
	main()
