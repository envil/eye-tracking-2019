import math
import csv
import copy
from pathlib import Path
from pointClass import Point
from detectFixations import detectFixations

base_path = Path(__file__).parent
file_path = (base_path / '../data/train.csv').resolve()

# Load assigned data for group 7 to variable 'data'
with file_path.open() as dataFile:
    rawData = []
    for row in csv.reader(dataFile, delimiter=','):
        if (row[0] == 's7') or (row[0] == 's17') or (row[0] == 's27') or (row[0] == 's3') or (row[0] == 's13') or (row[0] == 's23'):
            rawData.append(row)


# Initially process Points            
pointsData = [] # Raw data without sid & known; x & y stored as Point class
for row in rawData:
    k = (len(row)-2)/2  # Number of Points in current processing Row
    rowPoints = []  
    for i in range(2, k+2):
        x=float(row[i])
        y=float(row[i+k])
        rowPoints.append(Point(x,y))
    pointsData.append(rowPoints)

pointsDataCopy = copy.deepcopy(pointsData) #To be used in the SECOND SETTING
#FIRST SETTING:
# Choose duration-threshold to be 50ms & dispersion-threshold to be 2 degree
# Data generated at 1000Hz, hence the moving window spans about 50 points 
SC = 50 # spanning capacity: Number of Points that moving window initially span
DT = 2*math.sqrt(97**2+56**2) # dispersion-threshold

for rowPoints in pointsData:
    rowPoints = detectFixations(rowPoints, DT, SC)

# Printout result of centroid and duration of fixations
# m=0
# for rowPoints in pointsData:  
#     m=m+1  
#     print(rowPoints[len(rowPoints)-1])
#     print(rowPoints[len(rowPoints)-2])
#     print(m)
#     print('-----')


#SECOND SETTING:
# Choose duration-threshold to be 70ms & dispersion-threshold to be 1 degree
# Data generated at 1000Hz, hence the moving window spans about 70 points 
SC = 70 # spanning capacity: Number of Points that moving window initially span
DT = math.sqrt(97**2+56**2) # dispersion-threshold

for rowPoints in pointsDataCopy:
    rowPoints = detectFixations(rowPoints, DT, SC)

# Printout result of centroid and duration of fixations
# m=0
# for rowPoints in pointsDataCopy:  
#     m=m+1  
#     print(rowPoints[len(rowPoints)-1])
#     print(rowPoints[len(rowPoints)-2])
#     print(m)
#     print('-----')
            