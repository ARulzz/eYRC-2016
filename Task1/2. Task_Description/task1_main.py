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
*  Filename: task1_main.py
*  Version: 1.0.0  
*  Date: November 11, 2016
*  How to run this file: python task1_main.py
*  Author: e-Yantra Project, Department of Computer Science and Engineering, Indian Institute of Technology Bombay.
* ---------------------------------------------------

* ====================== GENERAL Instruction =======================
* 1. Check for "DO NOT EDIT" tags - make sure you do not change function name of main().
* 2. Return should be board_objects and output_list. Both should be list of tuple 
* 3. Do not keep uncessary print statement, imshow() functions in final submission that you submit
* 4. Do not change the file name
* 5. Your Program will be tested through code test suite designed and graded based on number of test cases passed 
**************************************************************************
'''
import cv2
import numpy as np

# ******* WRITE YOUR FUNCTION, VARIABLES etc HERE


def main(board_filepath, container_filepath):
	'''
This function is the main program which takes image of game-board and
container as argument. Team is expected to insert their part of code as
required to solve the given task (function calls etc).

***DO NOT EDIT THE FUNCTION NAME. Leave it as main****
Function name: main()

******DO NOT EDIT name of these argument*******
Input argument: board_filepath and container_filepath.

Return: 
1 - List of tuples which is the expected final output. See Task1_Description for detail. 
2 - List of tuples for objects on board. See Task1_Description for detail. 
	''' 

	board_objects = [0]*9		# List to store output of board -- DO NOT CHANGE VARIABLE NAME
	output_list = []		# List to store final output 	-- DO NOT CHANGE VARIABLE NAME
	



	##### WRITE YOUR CODE HERE - STARTS

	# cv2.imshow("board_filepath - press Esc to close",cv2.imread(board_filepath))			- For check - remove
	# cv2.imshow("container_filepath - press Esc to close",cv2.imread(container_filepath))

	container_objects = [0]*16
	board=cv2.imread(board_filepath)
	board_images=[[0,0,[0,0,0]]*8100]*9
	container=cv2.imread(container_filepath)
	container_images=[[0,0,[0,0,0]]*8100]*16

	def getColor(midPt):
		b=midPt[0]
		g=midPt[1]
		r=midPt[2]
		if(b>245):
			return "blue"
		elif g>245 and r<10:
			return "green"
		elif r>245 and g<10:
			return "red"
		elif g>245 and r>245:
			return "yellow"
		return ""

	def getShape(image):
		gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		ret,thresh = cv2.threshold(gray,127,255,1)
		contours,h = cv2.findContours(thresh,1,2)
		for cnt in contours:
			approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    		if len(approx)==3:
    			return "Triangle"
    		elif len(approx)==4:
        		return "4-sided"
    		else:
        		return "Circle"

	def getObjects():
		k=0
		for i in range(5,5+container.shape[0],container.shape[0]/4):
			for j in range(5,5+container.shape[1],container.shape[1]/4):
				container_images[k]=container.copy()[i:i+(container.shape[0]/4-10), j:j+(container.shape[1]/4-10)]
				color=getColor(container_images[k][45,45]);
				shape=""
				if color!="":
					shape=getShape(container_images[k])
				container_objects[k]=((k+1),color,shape)
				k=k+1

		k=0
		for i in range(5,5+board.shape[0],board.shape[0]/3):
			for j in range(5,5+board.shape[1],board.shape[1]/3):
				board_images[k]=board.copy()[i:i+(board.shape[0]/3-10), j:j+(board.shape[1]/3-10)]
				color=getColor(board_images[k][45,45]);
				shape=""
				if color!="":
					shape=getShape(board_images[k])
				board_objects[k]=((k+1),color,shape)
				k=k+1


	getObjects()
	for i in range(0,9):
		flag=0
		for j in range(0,16):
			if board_objects[i][1]==container_objects[j][1] and board_objects[i][2]==container_objects[j][2]:
				gray = cv2.cvtColor(board_images[i],cv2.COLOR_BGR2GRAY)
				ret,thresh = cv2.threshold(gray,127,255,1)
				contours,h = cv2.findContours(thresh,1,2)
				cnt = contours[0]
				Ai = cv2.contourArea(cnt)
				Pi = cv2.arcLength(cnt,True)
				gray = cv2.cvtColor(container_images[j],cv2.COLOR_BGR2GRAY)
				ret,thresh = cv2.threshold(gray,127,255,1)
				contours,h = cv2.findContours(thresh,1,2)
				cnt = contours[0]
				Aj = cv2.contourArea(cnt)
				Pj = cv2.arcLength(cnt,True)
				if Ai==Aj and Pi==Pj:
					output_list+=[((i+1),(j+1))]
					flag=1
					break
		if flag==0:
			output_list+=[((i+1),0)]



	# #### NO EDIT AFTER THIS

# DO NOT EDIT
# return Expected output, which is a list of tuples. See Task1_Description for detail.
	return board_objects, output_list	



'''
Below part of program will run when ever this file (task1_main.py) is run directly from terminal/Idle prompt.

'''
if __name__ == '__main__':
    

	board_filepath = "test_images/board_5.jpg"    			# change filename of board provided to you 
	container_filepath = "test_images/container_5.jpg"		# change filename of container as required for testing

	main(board_filepath,container_filepath)

	cv2.waitKey(0)
	cv2.destroyAllWindows()    
