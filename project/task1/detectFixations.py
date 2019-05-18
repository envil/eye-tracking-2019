import numpy as np

from handleWindowPoints import handleWindowPoints

def detectFixations(rowData, SAMPLING_FREQUENCY, DT, SC):
    fixationDuration = []
    fixationCentroid = []
    i=0
    while i+SC <= rowData.shape[0]:
        D = handleWindowPoints(rowData[i:i+SC])
        
        if D>DT:
            i=i+1
        else: 
            j=1
            while D<=DT and i+SC+j <= rowData.shape[0]:
                windowPoints = rowData[i:i+SC+j]
                D = handleWindowPoints(windowPoints)
                j=j+1

            fixationDuration.append( round((SC-1+j)*1/float(SAMPLING_FREQUENCY), 3) ) 
            mean = np.mean(windowPoints, axis=0)
            fixationCentroid.append( np.array([mean[0], mean[1]]) )
            i = i+SC-1+j
            
    output = []
    output.append(fixationDuration)
    output.append(fixationCentroid)
    return output