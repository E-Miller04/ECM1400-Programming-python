# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification

import numpy as np
from matplotlib import pyplot as mat_plot

def find_red_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """
    Loads an image and finds the red pixels based on rbg values and writes a 2D array to a jpeg as well as returning
    @param map_filename: name of the file with the different pavement types
    @param upper_threshold: used to determine if a pixel is red for red values
    @param lower_threshold: used to determine if a pixel is red for blue and green values
    @return red_img: 2D array of 1s and 0s representing the red paths
    """

    try:
        rgb_img = mat_plot.imread("data/" + map_filename)

        rgb_img = rgb_img * 255

        dimensions = (rgb_img.shape)
        
        rowAmount = dimensions[0]       #1140
        columnAmount = dimensions[1]    #1053
        
        #set all pixels to black
        red_img = np.zeros([rowAmount, columnAmount])       #2D array to return
        red_img_3D = np.zeros([rowAmount, columnAmount, 3]) #3D array for matplotlib to get correct amount of values (3 values per pixel)

        for row in range(rowAmount):
            for column in range(columnAmount):
                r = rgb_img[row, column, 0]
                g = rgb_img[row, column, 1]
                b = rgb_img[row, column, 2]

                if r > upper_threshold and g < lower_threshold and b < lower_threshold:
                    #white pixels added
                    red_img[row, column] = 1
                    red_img_3D[row, column] = 1
                

        mat_plot.imsave("map-red-pixels.jpeg", red_img_3D)
        return red_img
    except:
        print("Error handling map file")

        

def find_cyan_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """
    Loads an image and finds the cyan pixels based on rbg values and writes a 2D array to a jpeg as well as returning
    @param map_filename: name of the file with the different pavement types
    @param upper_threshold: used to determine if a pixel is cyan for blue and green values
    @param lower_threshold: used to determine if a pixel is cyan for red values
    @return cyan_img: 2D array of 1s and 0s representing the cyan paths
    """
    
    try:
        rgb_img = mat_plot.imread("data/" + map_filename)

        rgb_img = rgb_img * 255

        dimensions = (rgb_img.shape)
        
        rowAmount = dimensions[0]       #1140
        columnAmount = dimensions[1]    #1053
        
        #set all pixels to black
        cyan_img = np.zeros([rowAmount, columnAmount])
        cyan_img_3D = np.zeros([rowAmount, columnAmount, 3])

        for row in range(rowAmount):
            for column in range(columnAmount):
                r = rgb_img[row, column, 0]
                g = rgb_img[row, column, 1]
                b = rgb_img[row, column, 2]

                if r < lower_threshold and g > upper_threshold and b > upper_threshold:
                    #white pixels added
                    cyan_img[row, column] = 1
                    cyan_img_3D[row, column] = 1
                

        mat_plot.imsave("map-cyan-pixels.jpeg", cyan_img_3D)
        return cyan_img
    except:
        print("Error handling map file")



def detect_connected_components(IMG):
    """
    reads IMG returned from Task MI-1, returns a 2D array in numpy MARK and writes the number of pixels inside each connected component region into a text file cc-output-2a.txt
    @param IMG: 2D array of 1s and 0s representing if a pathway of a certain colour (Red or cyan) is present
    @return MARK: 2D array of visted pixels when finding connected components - 0 for no path and other numbers for connected component number
    """
    print("in connected")

    dimensions = (IMG.shape)
    rowAmount = dimensions[0]
    columnAmount = dimensions[1]
    
    #all caps for MARK and Q is interpreted as a constant so changed to variable 
    Mark = np.zeros([rowAmount, columnAmount])
    q = []

    ConnectedList = []
    ConNum = 0

    for row in range(rowAmount):
        for column in range(columnAmount):
            if IMG[row, column] == 1 and Mark[row, column] == 0:

                ConNum += 1
                #each connected component identifiable by number
                Mark[row, column] = ConNum

                #new connected segment
                connected = 1
                

                q = np.append(q, (int(row), int(column)))
                while q.size != 0:
                    first = q[:2]   #first coord
                    q = q[2:]       #other coords

                    for neighbour in range(8):
                        #x coord = column
                        along = first[1]
                        #y coord = row
                        down = first[0]

                        coord = nextCoord(along, down, neighbour)
                        x,y = coord.split(",")
                        x = int(x)
                        y = int(y)

                        #check valid coord
                        if x >= 0 and y >= 0 and x < columnAmount and y < rowAmount:

                            if IMG[y,x] == 1 and Mark[y,x] == 0:
                                #each connected component identifiable by number
                                Mark[y, x] = ConNum
                                q = np.append(q, (y, x))

                                connected += 1
                ConnectedList = np.append(ConnectedList, connected)

    fileName = "cc-output-2a.txt"
    file = open(fileName, "w")
    
    for components in range(len(ConnectedList)):
        print("Connected Component " + str(components + 1) + ", number of pixels = " + str(int(ConnectedList[components])))
        file.writelines("Connected Component " + str(components + 1) + ", number of pixels = " + str(int(ConnectedList[components]))+ "\n")

    print("Total number of connected components = " + str(len(ConnectedList)))
    file.writelines("Total number of connected components = " + str(len(ConnectedList)) + "\n")

    file.close()

    return Mark  


def nextCoord(x, y, neighbourNum):
    """
    Gets the coordinates of the 8 neighbours of a pixel
    @param x: column number of selected pixel
    @param y: row number of selected pixel
    @param neighbourNum: which coordinate to return
    """
    #n_ from Figure 3b
    if neighbourNum == 0:
        #n0
        coord = str(int(x + 1)) + ","+ str(int(y))
    elif neighbourNum == 1:
        #n1
        coord = str(int(x + 1)) + ","+ str(int(y + 1))
    elif neighbourNum == 2:
        #n2
        coord = str(int(x)) + ","+  str(int(y + 1))
    elif neighbourNum == 3:
        #n3
        coord = str(int(x - 1))+ "," + str(int(y + 1))
    elif neighbourNum == 4:
        #n4
        coord = str(int(x - 1))+ "," + str(int(y))
    elif neighbourNum == 5:
        #n5
        coord = str(int(x - 1)) + ","+ str(int(y - 1))
    elif neighbourNum == 6:
        #n6
        coord = str(int(x)) + "," + str(int(y - 1))
    elif neighbourNum == 7:
        #n7
        coord = str(int(x + 1)) + "," + str(int(y - 1))

    return coord
    


def detect_connected_components_sorted(MARK):
    """
    reads MARK returned from Task MI-2a, writes all connected components in decreasing order into a text file cc-output-2b.txt, and writes the top two largest connected components into a file named as cc-top-2.jpg
    @param MARK: 2D array of visted pixels when finding connected components - 0 for no path and other numbers for connected component number
    """
    print("in sorted")
    

    dimensions = (MARK.shape)
    rowAmount = dimensions[0]
    columnAmount = dimensions[1]

    
    #find how many connected components there are as each has a value (1-223 for red)
    totalConnected = 0
    for row in range(rowAmount):
        for column in range(columnAmount):
            if MARK[row,column] > totalConnected:
                totalConnected = int(MARK[row,column])


    #created a 2D array with ConNum and amount of pixels
    #e.g. [[1, 892]
    #      [2, 700]
    #      [3, 208]
    #        ....  ]
    connectedList = np.zeros([totalConnected, 2], np.int32)

    #set first column to 1-223 (or how many connected components there are)
    for rows in range(totalConnected + 1):
        connectedList[rows - 1, 0] = rows

    for row in range(rowAmount):
        for column in range(columnAmount):
            value = MARK[row, column]
            
            if int(value) != 0:
                connectedList[int(value) - 1, 1] += 1



    #bubble sort

    length = len(connectedList)
    swapped = True
    passes = 0

    while swapped == True or length == 0:
        swapped = False
        length -= 1
        passes += 1
        for a in range(length):
            if connectedList[a,1] < connectedList[a + 1, 1]:
                tempVal = connectedList[a,1]
                tempConNum = connectedList[a, 0]

                connectedList[a,1] = connectedList[a+1, 1]
                connectedList[a, 0] = connectedList[a+1, 0]

                connectedList[a+1, 1] = tempVal
                connectedList[a+1, 0] = tempConNum

                swapped = True

    

    
    #file saving and output part
    fileName = "cc-output-2b.txt"
    file = open(fileName, "w")
    
    for components in range(len(connectedList)):
        print("Connected Component " + str(connectedList[components, 0]) + ", number of pixels = " + str(connectedList[components, 1]))
        file.writelines("Connected Component " + str(connectedList[components, 0]) + ", number of pixels = " + str(connectedList[components, 1])+ "\n")

    print("Total number of connected components = " + str(len(connectedList)))
    file.writelines("Total number of connected components = " + str(len(connectedList)) + "\n")

    file.close()
    


    #printing 2 largest components
    largestConNum = connectedList[0,0]
    secondLargestConNum = connectedList[1,0]

    largest_img_3D = np.zeros([rowAmount, columnAmount, 3])

    for row in range(rowAmount):
        for column in range(columnAmount):
            value = MARK[row, column]

            if int(value) == int(largestConNum) or int(value) == int(secondLargestConNum):
                largest_img_3D[row, column] = 1

    mat_plot.imsave("cc-top-2.jpeg", largest_img_3D)

