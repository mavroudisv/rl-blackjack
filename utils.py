from random import randrange, randint
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def draw(color=None):
	if not color:
		color = 'red' if randrange(3)> 1 else 'black' #1/3 chances of being red, 2/3 chances of being black
	number = randint(1,10)
	#print("Card:", color, number)
	return (color, number)
	

def is_bust(sum):
	if sum > 21 or sum < 1:
		return True
	else:
		return False
		
def plot_3d(array, label1="", label2="", label3="", title=""):
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	#Dealer's first card (10x2 options), gambler's sum (21 options)
	X = np.arange(0,10,1)
	Y = np.arange(0,21,1)
	X, Y = np.meshgrid(X, Y)
	Z = array[X,Y]

	# Plot a basic wireframe
	#ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
	ax.plot_surface(X, Y, Z)
	ax.set_title(title)
	ax.set_xlabel(label1)
	ax.set_ylabel(label2)
	ax.set_zlabel(label3)
	
	plt.xticks(np.arange(1, 11+1, 1.0))
	plt.yticks(np.arange(1, 22+1, 1.0))
	ax.set_zticks(np.arange(-1, 1+.1, 0.1))
	plt.show()

def plot_2d(array, label1="", label2="", title=""):	
	fig, ax = plt.subplots()
	im = ax.imshow(array)
	
	for i in range(10):
		for j in range(21):
			if array[i, j] == 0:
				text = ax.text(j, i, "H", ha="center", va="center", color="w")
			else:
				text = ax.text(j, i, "S", ha="center", va="center", color="b")

	ax.set_title(title)
	ax.set_xlabel(label1)
	ax.set_ylabel(label2)

	plt.yticks(np.arange(0, 11, 1.0))
	plt.xticks(np.arange(0, 22, 1.0))	
	plt.show()