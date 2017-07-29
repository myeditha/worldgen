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

def genImage(inputarr):
	divfactor = twoDMax(inputarr)/255
	img = Image.new('RGB', (len(inputarr), len(inputarr[0])),"black")
	pixels = img.load()
	for i in range(img.size[1]):
		for j in range(img.size[0]):
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
	return setCorners(output)

def genrand(itr):
	global maxElev
	return (maxElev/(itr+1)) * (random.random()-0.5)*2

def square(squaredim, arr, itr):
	# print('entered square')
	for i in range(0, ((len(arr)//(squaredim))) if (squaredim==1) else ((len(arr)//(squaredim))+1)):
		xcoord = i * squaredim
		if(i % 2 == 0):
			for j in range(0, (len(arr)//((squaredim) * 2))):
				# print('square 1')
				ycoord = j * squaredim * 2 + squaredim
				# print(xcoord, ycoord)
				midpoint = 0
				if(i==0):
					midpoint = (arr[xcoord+squaredim][ycoord] + arr[xcoord][ycoord-squaredim] + arr[xcoord][ycoord-squaredim])/3
				elif(i==(len(arr)//((squaredim))) or i==len(arr)-1):
					midpoint = (arr[xcoord-squaredim][ycoord] + arr[xcoord][ycoord-squaredim] + arr[xcoord][ycoord-squaredim])/3
				else:
					midpoint = (arr[xcoord-squaredim][ycoord] + arr[xcoord+squaredim][ycoord] + arr[xcoord][ycoord-squaredim] + arr[xcoord][ycoord+squaredim])/4
				arr[xcoord][ycoord] = midpoint + genrand(itr)
				# print(arr)
				# print(arr[xcoord][ycoord])
		else:
			for j in range(0, (len(arr)//((squaredim) * 2))+1):
				# print('square 2')
				ycoord = j * squaredim * 2
				midpoint = 0
				# print(xcoord, ycoord)
				if(j==0):
					midpoint = (arr[xcoord-squaredim][ycoord] + arr[xcoord+squaredim][ycoord] + arr[xcoord][ycoord+squaredim])/3
				elif(j==(len(arr)//((squaredim)*2))):
					midpoint = (arr[xcoord-squaredim][ycoord] + arr[xcoord+squaredim][ycoord] + arr[xcoord][ycoord-squaredim])/3
				else:
					midpoint = (arr[xcoord-squaredim][ycoord] + arr[xcoord+squaredim][ycoord] + arr[xcoord][ycoord-squaredim] + arr[xcoord][ycoord+squaredim])/4
				arr[xcoord][ycoord] = midpoint + genrand(itr)
				# print(arr[xcoord])
				# print(arr[xcoord][ycoord ])

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
			# print(arr[multX + squaredim//2][multY + squaredim//2])
			# print('diamond')
			# print(arr)
			# print(multX + squaredim//2, multY + squaredim//2)

	return square(squaredim//2,arr,itr)

def diamondsquare(dim):
	initArray = createInitial2DArray(dim)
	return diamond(dim-1,initArray,1)


def main():
	rawterrain = diamondsquare(2049)
	# print(rawterrain)
	genImage(rawterrain)

main()
