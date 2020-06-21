import csv
import time

printB = False 


global dynMemory
dynMemory = []



def roadInput():
    pathMatrix = open("./newnetwork.csv", 'r')                                    
    matrixReader = csv.reader(pathMatrix, delimiter=',')
    pathData = []

    i = 0                                            
    for row in matrixReader:
        for val in row:
            row[i] = int(row[i])
            i = i + 1
        i = 0
        pathData.append(row)

    global roadSize
    roadSize = len(pathData)
    return pathData



def scheduleImport():
    pathMatrix = open('./indexed_req.csv', 'r')  
    matrixReader = csv.reader(pathMatrix, delimiter=',')  
    pathData = []
    i = 0

    for row in matrixReader: 
        row[0] = int(row[0])
        row[1] = int(row[1])  
        row[2] = int(row[2]) - 1
        row[3] = int(row[3]) - 1
     
        pathData.append(row)

    return pathData


          


          

          
class Car:

    def __init__(self, identify):
        self.start = 0 
        self.end = 0  
        self.dropTime = 0  
        self.identity = identify  
        self.requests = [] 


def timeFunc(grid, car, request): 
    pathTime = dijkstras(grid, car.end, int(request[2]))
    if (car.dropTime > request[1]):  
        pathTime = pathTime + car.dropTime - request[1]  
    return pathTime


          


          

          
def dijkstras(network, start, end):
    check, distFrom = dynCheck(start, end)
    if  check:  
        answer = distFrom
    else:
       
        distFrom = []
        finalizedSet = []

        count = 0
        while count < len(network):  
            distFrom.append(float('inf'))  
            finalizedSet.append(False)  
            count = count + 1
        distFrom[start] = 0  

        count = 0
        while count < (len(network)):  
            minimum = minDistance(distFrom, finalizedSet)  
            finalizedSet[minimum] = True  
            j = 0
            while (j < len(network)):  
                if (finalizedSet[j] == False and network[minimum][j] and distFrom[minimum] != 2147483647 and distFrom[minimum] + network[minimum][j] < distFrom[j]):
                    distFrom[j] = distFrom[minimum] + network[minimum][j]
                j = j + 1

            count = count + 1
        answer = printSolution(distFrom, start, end)
    return answer


def minDistance(distFrom, finalizedSet):
    min = 2147483647  
    count = 0
    while (count < roadSize):  
        if (finalizedSet[count] == False and distFrom[count] <= min):
            min = distFrom[count]
            minIndex = count
        count = count + 1
    return minIndex


def printSolution(distFrom, start, end):
   
    counter5 = 0
    while (counter5 < roadSize):
     
        dynMemory.append([start, counter5, distFrom[counter5]])
        counter5 = counter5 + 1

    distToEnd = distFrom[end]
    return distToEnd
          



def dynCheck(start, end):
    for val in dynMemory:                               
        if ((val[0] == start and val[1] == end) or (val[1]==start and val[0]==end)):
            return True, val[2]
    return False, 0
          

          

          
def carUpdate(car, end, req):
    travelTime = dijkstras(network, car.end, end)
    car.dropTime = req[0] + travelTime
    car.start = car.end
    car.end = end


def main():
    


    numCars = int(input("Enter no of cars:"))    
    calcRun(numCars)
    




def calcRun(numCars):
    global network
  
    drivenBy =[]                                       
    listCars = []                                       
    for i in range(numCars):
        listCars.append(Car(i))

    totalTime = 0
  
    network = roadInput()
    requests = scheduleImport()

                              
    for req in requests:
        minTime = 2147483647
        for i in range(numCars):                     
            pickupTime = timeFunc(network, listCars[i], req)
            if pickupTime < minTime:
                minTime = pickupTime
                minCar = i
        drivenBy.append(minCar)
        travelTime = dijkstras(network, req[2], req[3]) 
        totalTime = totalTime + minTime
        listCars[minCar].dropTime = req[1] + minTime + travelTime
        listCars[minCar].start = req[2]
        listCars[minCar].end = req[3]
        
    

   
    
    l = len(drivenBy)
    print("request no  driven by")
    for i in range(0,l):
        
        print("    {}          {}    ".format(requests[i][0],drivenBy[i]))
    print("\nTotal wait time is: ",totalTime)


    


if __name__ == "__main__":
    main()
