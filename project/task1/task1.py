import math, csv, copy
import numpy as np
from pathlib import Path

from detectFixations import detectFixations
from getConfigParameters import getConfigParameters

base_path = Path(__file__).parent
file_path = (base_path / '../data/train.csv').resolve()

def task1(settingNumber):

    # Load assigned data for group 7 to variable 'rawData'
    with file_path.open() as dataFile:
        rawData = []
        for row in csv.reader(dataFile, delimiter=','):
            if (row[0] == 's7') or (row[0] == 's17') or (row[0] == 's27') or (row[0] == 's3') or (row[0] == 's13') or (row[0] == 's23'):
                rawData.append(row)

    # Initially process Points            
    pointsData = [] # Raw data without sid & known; x & y stored in numpy array
    for row in rawData:
        rowPoints = []
        i=2
        while i < len(row)-1:
            x=float(row[i])
            y=float(row[i+1])
            i=i+2
            rowPoints.append(np.array([x,y]))
        np_rowPoints = np.array(rowPoints)
        pointsData.append(np_rowPoints)

    SAMPLING_FREQUENCY = 1000 #(Hz)
    
    #parameters[0] is DISPERSION_THRESHOLD
    #parameter[1] is DURATION_THRESHOLD
    parameters = getConfigParameters(settingNumber)
    
    # spanning capacity: Number of Points that moving window initially span
    SC = int(parameters[1] * SAMPLING_FREQUENCY)

    result = []
    for rowPoints in pointsData:
        result.append(detectFixations(rowPoints, SAMPLING_FREQUENCY, parameters[0], SC))

    # RETURN array contains 152 rows/samples (array); 
    # each row contains: duration of fixations in s (array)
    # and centroid-point of fixations (array) stored in numpy array.
    return result
    
                