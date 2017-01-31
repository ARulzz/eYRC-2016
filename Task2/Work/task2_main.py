# -*- coding: utf-8 -*-
'''
* Team Id:			#2855
* Author List:		Aarya R. Shankar
* Filename:			Task_2
* Theme:			Launch A Module
* Algorithm used:	A* algorithm
* Functions:		getImages(), getColor(image), getShape(image), getSize(image), getOccupiedObjectsProps(), neighbors(tuple, tuple), cost(tuple, tuple), heuristic(tuple, tuple), a_star(tuple, tuple), main(str)
					class PriorityQueue: __init__(self), empty(self), put(self, tuple priority), get(self)
* Global variables:	board, board_images, occupied_grids, objects, props
'''


'''
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2016)
*                  ================================
*  This software is intended to teach image processing concepts
*  
*  Author: e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*  
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode 
*     
*
*  This software is made available on an “AS IS WHERE IS BASIS”. 
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using 
*  ICT(NMEICT)
*
* ---------------------------------------------------
*  Theme: Launch a Module
*  Filename: task2_main.py
*  Version: 1.0.0  
*  Date: November 28, 2016
*  How to run this file: python task2_main.py
*  Author: e-Yantra Project, Department of Computer Science and Engineering, Indian Institute of Technology Bombay.
* ---------------------------------------------------

* ====================== GENERAL Instruction =======================
* 1. Check for "DO NOT EDIT" tags - make sure you do not change function name of main().
* 2. Return should be a list named occupied_grids and a dictionary named planned_path.
* 3. Do not keep uncessary print statement, imshow() functions in final submission that you submit
* 4. Do not change the file name
* 5. Your Program will be tested through code test suite designed and graded based on number of test cases passed 
**************************************************************************
'''
import cv2
import numpy as np
import heapq

# ******* WRITE YOUR FUNCTION, VARIABLES etc HERE
board=0
board_images=[]
occupied_grids=[]
objects=[]
props={}

'''
* Function Name:	getImages
* Input:			None
* Output:			None
* Logic:			Splits the given input image, and stores each cell in a 10x10 matrix called board_images
* Example Call:		getImages()
'''
def getImages():
	column=[]
	global board_images
	for i in range(1,board.shape[0],board.shape[0]/10):
		for j in range(1,board.shape[1],board.shape[1]/10):
			column+=[board.copy()[j:j+(board.shape[0]/10-1), i:i+(board.shape[1]/10)-1]]
		board_images+=[column]
		column=[]

'''
* Function Name:	getColor
* Input:			image -> variable which stores one of the 60x60 images, present in the cells of the input board
* Output:			returns the color of the pixel at (30,30)
* Logic:			No matter what the image is, its mid-point (ie, pixel at (30,30)) will have the color of its main image.
					If the cell is blank, the mid point will also be white.
					If the cell is black (obstacle), its mid point will also be black.
					If the cell contains a triangle, a circle, or a 4-sided figure of any colour among red, blue, and green, its mid point will be of that colour.
					So by considering the BGR values of that point, we can get the color.
* Example Call:		getColor(image)
'''
def getColor(image):
	b=image[30,30,0]
	g=image[30,30,1]
	r=image[30,30,2]
	if b>245 and g>245 and r>245:
		return 'white'
	elif b<10 and g<10 and r<10:
		return 'black'
	elif b>245:
		return 'blue'
	elif g>245:
		return 'green'
	elif r>245:
		return 'red'

'''
* Function Name:	getShape
* Input:			image -> variable which stores one of the 60x60 images, present in the cells of the input board
* Output:			returns the shape of the object (as "Circle", "4-sided", "Triangle") in the iamge
* Logic:			First, we convert the image into a grayscale image. Then we put a threshold values of 170, and 255, since that will be appropriate for the given green, red, and blue colours.
					Then we find the contours. The number of contour points will be equal to the vertices of the shape.
					If it is 3, it is a triangle.
					If it is 4, it is a 4-sided.
					If it is not either one of these, it is a circle (as the given figues can be only circle, 4-sided, or triangle).
* Example Call:		getShape(image)
'''
def getShape(image):
	#return 'pass shape'
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray,170,255,1)
	contours,h = cv2.findContours(thresh,1,2)
	for cnt in contours:
		approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
		if len(approx)==3:
			return "Triangle"
		elif len(approx)==4:
			return "4-sided"
		else:
			return "Circle"

'''
* Function Name:	getSize(image)
* Input:			image -> variable which stores one of the 60x60 images, present in the cells of the input board
* Output:			(area, perimeter) -> returns a tuple containing the area, and perimeter of the figure in the image
* Logic:			The size of a particular shaped object can be characterized by its area and perimeter.
					Therefore, the area, and the perimeter of the contour using the corresponding functions.
* Example Call:		getSize(image)
'''
def getSize(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray,170,255,1)
	contours,h = cv2.findContours(thresh,1,2)
	cnt = contours[0]
	A = cv2.contourArea(cnt)
	P = cv2.arcLength(cnt,True)
	return (A,P)

'''
* Function Name:	getOccupiedObjectsProps
* Input:			None
* Output:			None
* Logic:			We have already split and the whole image, and stored it in an array.
					If the color of the image is white, that co-ordinate is not occupied.
					Else, it is. The co-ordinates of the occupied cells are stored in the list occupied_grids.
					If the colour of the image is not black either, then it is not an obstacle, meaning it has an object.
					If it has an object, we store its indices in a list called objects and 
					we store its proerties which defines it (ie, color, shape and size) in a dictionary props with the indices as the key.
* Example Call:		getOccupiedObjectsProps()
'''
def getOccupiedObjectsProps():
	global occupied_grids
	global objects
	global props
	for i in range(0,10):
		for j in range(0,10):
			image = board_images[i][j]
			color = getColor(image)
			if color != 'white':
				occupied_grids += [(i+1,j+1)]
				if color != 'black':
					objects += [(i,j)]
					props[(i,j)] = (color,getShape(image),getSize(image))


# class for implementing Priority Queue for A* algorithm
class PriorityQueue:

	'''
	* Function Name:	__init__
	* Input:			None
	* Output:			None
	* Logic:			Creates an instance of this class, and initializes it to an empty list.
	* Example Call:		a = PriorityQueue()
						Here a is an instance of PriorityQueue
	'''
	def __init__(self):
		self.elements = []
    
	'''
	* Function Name:	empty
	* Input:			None
	* Output:			Returns the length of the list. By default, it will return zero.
	* Logic:			If the number of elements in the list is zero, then it is empty
	* Example Call:		a.empty() where a in an object of PriorityQueue class
	'''
	def empty(self):
		return len(self.elements) == 0

	'''
	* Function Name:	put
	* Input:			item -> The data to be inserted into the priority queue. In this case, it is a tuple containing the indices of a cell.
						priority -> The priority of the data to be inserted. In this case, it is the sum of the total cost of travelling from the 
						starting point to the indices in item and the distance of the goal from the indices in the item.
	* Output:			None
	* Logic:			The item will be inserted to the list in such a way that it remains sorted in the ascending order of the priorities of the data in it
	* Example Call:		frontier.put((2,3),2)
	'''
	def put(self, item, priority):
		heapq.heappush(self.elements, (priority, item))

	'''
	* Function Name:	get
	* Input:			None
	* Output:			Returns the second element of the first item in the list.
	* Logic:			An item is popped from the priority queue, which is the one with the least priority.
						The second element of the first item in the list is the tuple or location, while the first one is its priority.
	* Example Call:		frontier.get()
	'''
	def get(self):
		return heapq.heappop(self.elements)[1]

'''
* Function Name:	neighbors
* Input:			node -> A tuple containing the indices of the current node under consideration in A* algorithm
* Output:			Returns a list containg tuples, which are the indices of the neighbors of the node in the input grid.
* Logic:			The neighbors of the node (x, y) can be (x+1, y), (x, y+1), (x-1, y), and (x, y-1).
					The one within the boundaries of the input grid image are the valid neighbors.
* Example Call:		neighbors((2,3)
'''
def neighbors(node):
    possibleDirections = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    result = []
    for dir in possibleDirections:
        neighbor = (node[0] + dir[0], node[1] + dir[1])
        if 0 <= neighbor[0] < 10 and 0 <= neighbor[1] < 10:
            result.append(neighbor)
    return result

'''
* Function Name:	cost
* Input:			next -> tuple containing the indices of a location that our path may move to.
					goal -> tuple conatining the indices of the current end point.
* Output:			Returns the cost of the movement to indices stored in next.
* Logic:			Since for a particular starting point, all the occupied grids excluding its goal, are obstacles, the movement to any obstacle is given a
					hige value (say, 10000) so that while considering the cost, it won't be the least if there is another longer but obstacle free path,
					and the rest are given the cost of 1. The movement to the goal is given as 0 (not necessary).
* Example Call:		cost((2,3),(4,5))
'''
def cost(next, goal):
	if next == goal:
		return 0
	elif (next[0] + 1, next[1] + 1) in occupied_grids:
		return 10000
	return 1

'''
* Function Name:	heuristic
* Input:			a -> a tuple containing a pair of indices
					b -> a tuple containing the indices of the location of our goal
* Output:			Returns the estimated distance from a to b.
* Logic:			We need to calculate the distance so that we can prioritise the location the path should go to.
					It is calculated by the taking the difference of the corresponding x-coordinates and corresponding y-coordinates of a and b
* Example Call:		heuristic((1,2),(4,5))
'''
# implementing heuristic function and A*
def heuristic(a, b):
	distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
	return distance

'''
* Function Name:	a_star
* Input:			start -> tuple that contains the indices of the starting point
					goal -> tuple that contains the indices of the end point
* Output:			returns a tuple containing the path as a list having the coordinates of the locations in the path,
					and the number of movements that happens while following the path.
* Logic:			We need to find the shortest path between start and goal, which excludes all obstacles and other objects. For this, we use A* algorithm.
					We create an instance of the class PriorityQueue, named frontier. We start from start, so first we put start with the priority 0 into frontier.
					We declare a dictionary came_from with a location as its key, and the location where it came from as the value, so that we can retrace the path later on.
					We declare a dictioanry cost_so_far, with a location as its key, and the total cost to come to that location from start as the value, so that we can choose the cheapest path while traversing and get the total cost at the end.
					We will save start as the key and none as the value in the dictionary came_from, as start did come from nowhere.
					We will save start as the key and 0 as the value in the dictionary cost_so_far, as cost of getting to start from start is zero.
					While our priority queue, ie frontier is not empty, we will do the following:
						1. Pop an element with the least priority from frontier, and store it in current.
						2. Compare it to the goal, if it we got our path, so we'll break from the loop.
						3. We will get the neighbors of the location current, and we will iterate throught them, saving the current neighbor under assessment as next..
						4. During each iteration:
							i.   We calculate the new_cost, ie the cost of getting to the neighbor next from start, which is the sum of cost_so_far of theo current location, and the cost of next by using the funtion next(next ,goal).
							ii.  if next is not in the dictionary cost_so_far (ie if next has not been visited yet) or if the new_cost is less than cost_so_far of next (ie if the new cost we calculated is less than the cost of getting to next from start), we do:
							     	a. assign the cost_so_far of next as new_cost
							     	b. calculate the priority of next as the sum of new_cost and the distance between goal and enxt using the function heuristic(goal, next)
							     	c. we add next to the frontier with the calculated priority
							     	d. we also add that the next came from current to the came_from dictionary.
					The usage of priority queue ensures that we always choose the path with the least cost and distance.
					Now we will calculate the total cost of getting to the goal from start. Since the cost is manipulated in such a way that, if it goes through atleast one obstacle,
					the cost will be 10000, we know that if the total cost of the path exceeds 10000, there is no obstacle free path to our goal.
					To calculate the toal cost, we take the location from where the goal came in our path. Then take the cost so far of that location.
					If it exceeds 10000, we will return a tuple an empty list and an integer 0, signifying that there is no path available.
					Else, we trace back our path, using the came_from dictionary, and appending the right location to the list path.
					We add one to each element of the location indice, because our co-ordinates are 1 greater than out indices.
					Now we have our path from the goal to the starting point. We need to reverse it to get the path from starting point to the goal.
					Once we do that, we return a tuple conating the list path, and the total number of movements.
					The total number of movements is always one grater than the total elements of our path. So we return length of path + 1 as the total number of movements.					
* Example Call:		a_star((2,3),(7,8))
'''
def a_star(start, goal):
	frontier = PriorityQueue()
	frontier.put(start, 0)
	came_from = {}
	cost_so_far = {}
	came_from[start] = None
	cost_so_far[start] = 0
	# finding the shortest path
	while not frontier.empty():
		current = frontier.get()
		if current == goal:
			break
		for next in neighbors(current):
			new_cost = cost_so_far[current] + cost(next, goal)
			if next not in cost_so_far or new_cost < cost_so_far[next]:
				cost_so_far[next] = new_cost
				priority = new_cost + heuristic(goal, next)
				frontier.put(next, priority)
				came_from[next] = current
				
	# reconstructing the path
	path = []
	total_cost=cost_so_far[came_from[goal]]
	if total_cost >= 1000:
		return([],0)
	else:
		while came_from[current] != start:
			current = came_from[current]
			path.append((current[0]+1,current[1]+1))
		path.reverse()
		return (path, len(path)+1)

'''
* Function Name:	main
* Input:			image_filename
* Output:			returns the co-ordinates of the occupied grids as a list named occupied_grids, 
					and a dictionary named planned_path which contains the locations of the objects in the grid as the key, and
					a tuple of their nearest match, list containing shortest path, and the length of the path, as the values.
* Logic:			First we the image with the filename image_filename. Then we split it and the save the each cells of the image into board_images using the function get_images().
					Then we get the co-ordinates of the occupied grids as a list, and co-ordinates of the  objects as a list, properties of the objects in a dictionary using the functions getOccupiedObjectsProps().
					Then we iterate through the list objects, and find out the locations of all of its matching objects, and store the matchs in the list matches and the number of matches in nmatches.
					If nmatches=0, we say there is "No Match".
					If there is atleast one match, we pass the current object, and its first match to the function a_star and stores the returning path and length of path in path and pathLen. The first match is stored under match.
					If there are more than one match, we iterate through the remaining matches, and we pass our current object, and the current matching object to the funtion a_star and store the returning path and its length
					under nextPath and nextPathLen. We find the smallest length of the path, and store that matching object location indice, the corresponsing path and path length under match, path, and pathLen respectively.
					If the pathLen==0, when there is at least one match, we say there is "No Path"
					After storing the coordinates of the objects as the keys and a tuple having its nearest match, path and path length as the value in the dictionary planned_path,
					we return it.
* Example Call:		main("tes_image5.jpg")
'''
def main(image_filename):
	'''
This function is the main program which takes image of test_images as argument. 
Team is expected to insert their part of code as required to solve the given 
task (function calls etc).

***DO NOT EDIT THE FUNCTION NAME. Leave it as main****
Function name: main()

******DO NOT EDIT name of these argument*******
Input argument: image_filename

Return:
1 - List of tuples which is the coordinates for occupied grid. See Task2_Description for detail. 
2 - Dictionary with information of path. See Task2_Description for detail.
	'''
	global board
	global occupied_grids
	
	occupied_grids = []		# List to store coordinates of occupied grid -- DO NOT CHANGE VARIABLE NAME
	planned_path = {}		# Dictionary to store information regarding path planning  	-- DO NOT CHANGE VARIABLE NAME
	
	##### WRITE YOUR CODE HERE - STARTS
	board=cv2.imread(image_filename)
	getImages()
	getOccupiedObjectsProps()
	
	# iterating through the objects
	for i in objects:
		nmatches=0
		matches=[]
		# finding the matches if any
		for j in objects:
			if i != j and props[i] == props[j]:
				nmatches += 1
				matches += [j]
		# key is the coordinates of the current object
		key = (i[0]+1,i[1]+1)
		if nmatches == 0:
			planned_path[str(key)] = [ "NO MATCH", [], 0 ]
		else:
			(path, pathLen) = a_star(i, matches[0])
			match = matches[0]
			if nmatches != 1:
				for k in range(1, nmatches):
					(nextPath, nextPathLen) = a_star(i, matches[k])
					if nextPathLen < pathLen:
						pathLen = nextPathLen
						path = nextPath
						match = matches[k]
			match = (match[0]+1,match[1]+1)
			if pathLen==0:
				planned_path[str(key)] = [ match, "NO PATH", 0 ]
			else:
				planned_path[str(key)] = [ match, path, pathLen ]

	print occupied_grids
	print planned_path

	# #### NO EDIT AFTER THIS

# DO NOT EDIT
# return Expected output, which is a list of tuples. See Task1_Description for detail.
	return occupied_grids, planned_path



'''
Below part of program will run when ever this file (task1_main.py) is run directly from terminal/Idle prompt.

'''
if __name__ == '__main__':

    # change filename to check for other images
    image_filename = "test_images/test_image1.jpg"

    main(image_filename)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
