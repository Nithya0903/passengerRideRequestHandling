import csv
import time

printB = False  # output print for solution


global dynMemory
dynMemory = []


#
# Importing Network#

def roadInput():
    pathMatrix = open("./newnetwork.csv", 'r')  # open file in read form
    matrixReader = csv.reader(pathMatrix, delimiter=',')  # pull data with , delimiter
    pathData = []

    i = 0                                               # Move data in list of lists
    for row in matrixReader:
        for val in row:
            row[i] = int(row[i])
            i = i + 1
        i = 0
        pathData.append(row)

    global roadSize
    roadSize = len(pathData)
    return pathData


#
# Schedule Import Start#

def scheduleImport():
    pathMatrix = open('./newrequest.csv', 'r')  # open file in read form
    matrixReader = csv.reader(pathMatrix, delimiter=',')  # pull data with , delimeter
    pathData = []
    # Build request list
    i = 0

    for row in matrixReader:  # locations range from 1-50
        row[0] = int(row[0])  # adjusting to 0-49
        row[1] = int(row[1]) - 1
        row[2] = int(row[2]) - 1
        pathData.append(row)

    #print('Schedule Successfulling Stored')
    return pathData


#


#
#  Car Class#
#
class Car:  # Class with data such as...

    def __init__(self, identify):
        self.start = 0  # Location of pickup(Not useful currently)
        self.end = 0  # Location of drop off
        self.dropTime = 0  # Time of current delivery dropoff
        self.identity = identify  # Identifier for car
        self.requests = [] #the requests this particular car catered


def timeFunc(grid, car, request):  # Determine the time to pick up passenger
    pathTime = dijkstras(grid, car.end, int(request[1]))
    if (car.dropTime > request[0]):  # If currently busy
        pathTime = pathTime + car.dropTime - request[0]  # Include time to drop off current pasenger
    return pathTime


#


#
# Dijkstras#
#
def dijkstras(network, start, end):
    check, distFrom = dynCheck(start, end)
    if  check:  # If dynamic storage is available check whehter path has been traversed before
        answer = distFrom
    else:
        # store more fastest time to each point from a chosen point
        distFrom = []
        finalizedSet = []

        count = 0
        while count < len(network):  # Currrently all dist. are unknown
            distFrom.append(float('inf'))  # setting inf. distance away
            finalizedSet.append(False)  # set false to confirmed shortest distance
            count = count + 1
        distFrom[start] = 0  # distance to starting point is now 0

        count = 0
        while count < (len(network)):  # find the shortest path to all points
            minimum = minDistance(distFrom, finalizedSet)  # pick vertex shortest distance from the column
            finalizedSet[minimum] = True  # set picked vertex to True
            j = 0
            while (j < len(network)):  # if a shorter distance is found, update val of finalizedSet
                if (finalizedSet[j] == False and network[minimum][j] and distFrom[minimum] != 2147483647 and distFrom[minimum] + network[minimum][j] < distFrom[j]):
                    distFrom[j] = distFrom[minimum] + network[minimum][j]
                j = j + 1
            count = count + 1
        answer = printSolution(distFrom, start, end)
    return answer


def minDistance(distFrom, finalizedSet):
    min = 2147483647  # Set min to max of int so its not accidentally chosen
    count = 0
    minIndex = 0
    while (count < roadSize):  # Chose minimum distance
        if (finalizedSet[count] == False and distFrom[count] <= min):
            min = distFrom[count]
            minIndex = count
        count = count + 1
    return minIndex


def printSolution(distFrom, start, end):
    # print("Vertex Distance from source \n")
    counter5 = 0
    while (counter5 < roadSize):
        if printB:
            print(counter5 + 1, '   ', distFrom[counter5])
        dynMemory.append([start, counter5, distFrom[counter5]])
        counter5 = counter5 + 1

    distToEnd = distFrom[end]
    return distToEnd
#


###############################################
# Dynamic Val Check
###############################################
def dynCheck(start, end):
    for val in dynMemory:                               #Go through all prev. paths and check if done before
        if ((val[0] == start and val[1] == end) or (val[1]==start and val[0]==end)):
            return True, val[2]
    return False, 0

def carUpdate(car, end, req):
    travelTime = dijkstras(network, car.end, end)
    car.dropTime = req[0] + travelTime
    car.start = car.end
    car.end = end



def main():
    
    numCars=2       #Define the number of cars
    print(" Solution")
    calcRun(numCars)
    



#
# Scheduling#
#
def calcRun(numCars):
    global network
    #numCars = 2                                        #This value defines the number of cars
    listCars = []                                       #Define dynamic # cars variables
    for i in range(numCars):
        listCars.append(Car(i))

    totalTime = 0
    #Val to store total wait time
    network = roadInput()
    requests = scheduleImport()

    for req in requests:
        minTime = 2147483647
        for i in range(numCars):                        #Choose car which can arrive fastest
            pickupTime = timeFunc(network, listCars[i], req)
            if pickupTime < minTime:
                minTime = pickupTime
                minCar = i

        travelTime = dijkstras(network, req[1], req[2]) 
        #Update car locations and trip times
        totalTime = totalTime + minTime
        listCars[minCar].dropTime = req[0] + minTime + travelTime
        listCars[minCar].start = req[1]
        listCars[minCar].end = req[2]
        print('The request - request time :',req[0],' from NODE :',req[1],' to :',req[2],' took ',minTime, 'min to be served and was served by ',minCar)


    print("\nTotal wait time is: ",totalTime)


    


if __name__ == "__main__":
    main()
