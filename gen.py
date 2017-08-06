from PIL import Image
import random

maxElev = 2048

def twoDMax(inputarr):
	maxvals = []
	for i in range(len(inputarr)):
		maxvals.append(max(inputarr[i]))
	return max(maxvals)

def twoDMin(inputarr):
	minvals = []
	for j in range(len(inputarr)):
		minvals.append(min(inputarr[i]))
	return min(minvals)

def postprocessing(inputarr):
	return inputarr

def genImage(inputarr, colorChange = False):
	divfactor = twoDMax(inputarr)/255
	img = Image.new('RGB', (len(inputarr), len(inputarr[0])),"black")
	pixels = img.load()
	for i in range(img.size[1]):
		for j in range(img.size[0]):
			if(inputarr[i][j]<=0 and colorChange):
				pixels[i,j] = (30,144,255)
			else:	
				pixels[i,j] = (int(inputarr[i][j]/divfactor), int(inputarr[i][j]/divfactor), int(inputarr[i][j]/divfactor))
	img.show()

def setCorners(arr, rand=True):
	global maxElev
	arr[len(arr)-1][len(arr)-1] = random.random() * maxElev if rand else 0
	arr[0][len(arr)-1] = random.random() * maxElev if rand else 0
	arr[len(arr)-1][0] = random.random() * maxElev if rand else 0
	arr[0][0] = random.random() * maxElev if rand else 0
	return arr

def createInitial2DArray(size):
	output = [[0 for x in range(size)] for y in range(size)]
	return setCorners(output, False)

def genrand(itr):
	global maxElev
	return (maxElev/(itr+1)) * (random.random()-0.5)*2

def checks(i,j,squaredim,arr, itr):
	xcoord = i * squaredim
	ycoord = j * squaredim * 2
	if(i % 2 == 0):
		ycoord = j * squaredim * 2 + squaredim
	if(i==0):
		midpoint = (arr[xcoord+squaredim][ycoord] + arr[xcoord][ycoord-squaredim] + arr[xcoord][ycoord-squaredim])/3
	elif(i==(len(arr)//((squaredim))) or i==len(arr)-1):
		midpoint = (arr[xcoord-squaredim][ycoord] + arr[xcoord][ycoord-squaredim] + arr[xcoord][ycoord-squaredim])/3
	elif(j==0):
		midpoint = (arr[xcoord-squaredim][ycoord] + arr[xcoord+squaredim][ycoord] + arr[xcoord][ycoord+squaredim])/3
	elif(j==(len(arr)//((squaredim)*2))):
		midpoint = (arr[xcoord-squaredim][ycoord] + arr[xcoord+squaredim][ycoord] + arr[xcoord][ycoord-squaredim])/3		
	else:
		midpoint = (arr[xcoord-squaredim][ycoord] + arr[xcoord+squaredim][ycoord] + arr[xcoord][ycoord-squaredim] + arr[xcoord][ycoord+squaredim])/4
	arr[xcoord][ycoord] = midpoint + genrand(itr)

def square(squaredim, arr, itr):
	for i in range(0, ((len(arr)//(squaredim))) if (squaredim==1) else ((len(arr)//(squaredim))+1)):
		xcoord = i * squaredim
		upbound = (len(arr)//((squaredim) * 2))+1
		if(i % 2 == 0):
			upbound = (len(arr)//((squaredim) * 2))
		for j in range(0, upbound):	
			checks(i,j,squaredim,arr, itr)
	return diamond(squaredim,arr,itr+1)

def diamond(squaredim, arr, itr):
	if(squaredim == 1):
		return arr
	global maxElev
	for i in range(0,len(arr)//squaredim):
		for j in range(0,len(arr)//squaredim):
			multX = i * squaredim
			multY = j * squaredim

			midpoint = (arr[multX][multY+squaredim] + arr[multX][multY] + arr[multX+squaredim][multY] + arr[multX+squaredim][multY+squaredim])/4

			arr[multX + squaredim//2][multY + squaredim//2] = midpoint + genrand(itr)

	return square(squaredim//2,arr,itr)

def diamondsquare(dim):
	initArray = createInitial2DArray(dim)
	return diamond(dim-1,initArray,1)


def main():
	rawterrain = diamondsquare(4097)
	genImage(postprocessing(rawterrain))

main()
