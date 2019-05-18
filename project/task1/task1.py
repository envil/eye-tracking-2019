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
                row = np.array(row[2:])
                row = row.astype(np.float)
                rawData.append(np.reshape(row, (int(row.shape[0]/2), 2)))

    SAMPLING_FREQUENCY = 1000 #(Hz)
    
    #parameters[0] is DISPERSION_THRESHOLD
    #parameter[1] is DURATION_THRESHOLD
    parameters = getConfigParameters(settingNumber)
    
    # spanning capacity: Number of Points that moving window initially span
    SC = int(parameters[1] * SAMPLING_FREQUENCY)

    result = []
    for rowPoints in rawData:
        result.append(detectFixations(rowPoints, SAMPLING_FREQUENCY, parameters[0], SC))

    # RETURN array contains 152 rows/samples (array); 
    # each row contains: duration of fixations in s (array)
    # and centroid-point of fixations (array) stored in numpy array.
    return result
    
                