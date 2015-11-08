# Display 2D Fourplay Board 

import matplotlib.pyplot as plt
import numpy as np



def displayBoardSingleFrame(grid):
	dim_x, dim_y = grid.shape
	column_labels = range(dim_x)
	row_labels = range(dim_y)
	fig, ax = plt.subplots()
	print(plt.cm.Blues)
	heatmap = ax.pcolor(grid, cmap = 'YlGnBu')
	ax.set_xticks(np.arange(grid.shape[0]), minor = False)
	ax.set_yticks(np.arange(grid.shape[1]), minor = False)
	ax.invert_yaxis()
	plt.grid()
	plt.show()


# red = 1, blue = 2
grid = np.array([[0,2,2,1], [2,2,2,1], [2,2,2,1], [2,1,2,2]])
displayBoardSingleFrame(grid)