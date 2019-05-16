import statistics
from pointClass import Point
from handleWindowPoints import handleWindowPoints

def detectFixations(rowData, DT, SC):
    fixationDuration = []
    fixationCentroid = []
    i=0
    while i+SC-1 <= len(rowData)-1:
        D = handleWindowPoints(rowData[i:i+SC])[0]
        compareDispersion = D > DT
        if compareDispersion:
            i=i+1
        else: 
            j=1
            while D<=DT and i+SC-1+j<=len(rowData)-1:
                output = handleWindowPoints(rowData[i:i+SC+j])
                D = output[0]
                j=j+1

            fixationDuration.append( round((SC-1+j)*0.001, 3) ) 
            x = statistics.mean(output[1])
            y = statistics.mean(output[2])
            fixationCentroid.append(Point(x,y))
            i = i+SC-1+j
    
    rowData.append(fixationDuration)
    rowData.append(fixationCentroid)
    return rowData