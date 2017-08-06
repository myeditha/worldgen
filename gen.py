from PIL import Image
import random
import sys
import argparse

maxElev = 2048

class Error(Exception):
	pass

class SizeError(Error):
	def __init__(self, message):
		self.message = message

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

def saveArray(inputarr, fileName = 'image.txt'):
	writeTo = open(fileName, 'w')
	for x in inputarr:
		for y in x:
			writeTo.write('%s', y)
		writeTo.write('\n')

def setCorners(arr, rand=True):
	global maxElev
	arr[len(arr)-1][len(arr)-1] = random.random() * maxElev if rand else 0
	arr[0][len(arr)-1] = random.random() * maxElev if rand else 0
	arr[len(arr)-1][0] = random.random() * maxElev if rand else 0
	arr[0][0] = random.random() * maxElev if rand else 0
	return arr

def createInitial2DArray(size, ocean):
	output = [[0 for x in range(size)] for y in range(size)]
	return setCorners(output, ocean)

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

def diamondsquare(dim, height, ocean):
	global maxElev
	maxElev = height
	initArray = createInitial2DArray(dim, ocean)
	return diamond(dim-1,initArray,1)

def main():
	parser = argparse.ArgumentParser(description='Randomized terrain generation')
	parser.add_argument('size', metavar = 'S', type=int, help='size of the image (multiples of two plus one)')
	parser.add_argument('height', metavar = 'H', type=int, help='height of the image')
	parser.add_argument('-ocean', action = 'store_true', help='ocean-y')
	parser.add_argument('--bitmap', action='store_true',help='generate bitmap representation')
	parser.add_argument('--textfile', action = 'store_true', help = 'generate file representation')

	args = parser.parse_args()
	
	if((args.size-1) & (args.size-2)!=0):
		raise SizeError('Size is not a power of 2 plus 1.')

	rawterrain = diamondsquare(args.size, args.height, args.ocean)
	resarr = postprocessing(rawterrain)

	if(args.bitmap):
		genImage(resarr)
	if(args.textfile):
		saveArray(resarr)

main()
