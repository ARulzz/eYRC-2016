'''
* Team Id:			#2855
* Author List:		Aarya R. Shankar
* Filename:			Task_2
* Theme:			Launch A Module
* Functions:		getImages(), getColor(), getShape(), getSize(), getOccupiedObjectsProps() 
* Global variables:	
'''

# -*- coding: utf-8 -*-
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
def getImages():
	column=[]
	global board_images
	for i in range(1,board.shape[0],board.shape[0]/10):
		for j in range(1,board.shape[1],board.shape[1]/10):
			column+=[board.copy()[j:j+(board.shape[0]/10-1), i:i+(board.shape[1]/10)-1]]
		board_images+=[column]
		column=[]

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

def getSize(image):
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray,170,255,1)
	contours,h = cv2.findContours(thresh,1,2)
	cnt = contours[0]
	A = cv2.contourArea(cnt)
	P = cv2.arcLength(cnt,True)
	return (A,P)

def getOccupiedObjectsProps():
	global occupied_grids
	global objects
	global props
	for i in range(0,10):
		for j in range(0,10):
			image=board_images[i][j]
			color=getColor(image)
			if color != 'white':
				occupied_grids += [(i+1,j+1)]
				if color != 'black':
					objects += [(i,j)]
					props[(i,j)] = (color,getShape(image),getSize(image))


# implementing Priority Queue
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def neighbors(node, goal):
    possibleDirections = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    result = []
    for dir in possibleDirections:
        neighbor = (node[0] + dir[0], node[1] + dir[1])
        if 0 <= neighbor[0] < 10 and 0 <= neighbor[1] < 10:
            result.append(neighbor)
    return result

def cost(next, goal):
	if next == goal:
		return 0
	elif (next[0]+1,next[1]+1) in occupied_grids:
		return 10000
	return 1

# implementing heuristic function and A*
def heuristic(a, b):
	distance = abs(a[0] - b[0]) + abs(a[1] - b[1])
	return distance
	
def a_star_search(start, goal):
	frontier = PriorityQueue()
	frontier.put(start, 0)
	came_from = {}
	cost_so_far = {}
	came_from[start] = None
	cost_so_far[start] = 0
	while not frontier.empty():
		current = frontier.get()
		
		if current == goal:
			break
		
		for next in neighbors(current, goal):
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
	
	for i in objects:
		nmatches=0
		matches=[]
		for j in objects:
			if i != j and props[i] == props[j]:
				nmatches += 1
				matches += [j]
		key = (i[0]+1,i[1]+1)
		if nmatches == 0:
			planned_path[str(key)] = [ "NO MATCH", [], 0 ]
		else:
			(path, pathLen) = a_star_search(i, matches[0])
			match = matches[0]
			if nmatches != 1:
				for k in range(1, nmatches):
					(nextPath, nextPathLen) = a_star_search(i, matches[k])
					if nextPathLen < pathLen:
						pathLen = nextPathLen
						path = nextPath
						match = matches[k]
			match = (match[0]+1,match[1]+1)
			if pathLen==0:
				planned_path[str(key)] = [ match, "NO PATH", 0 ]
			else:
				planned_path[str(key)] = [ match, path, pathLen ]



	



	# #### NO EDIT AFTER THIS

# DO NOT EDIT
# return Expected output, which is a list of tuples. See Task1_Description for detail.
	return occupied_grids, planned_path



'''
Below part of program will run when ever this file (task1_main.py) is run directly from terminal/Idle prompt.

'''
if __name__ == '__main__':

    # change filename to check for other images
    image_filename = "test_images/test_image7.jpg"

    main(image_filename)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
