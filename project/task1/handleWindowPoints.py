import numpy as np

def handleWindowPoints(windowPoints): 
    max = np.amax(windowPoints, axis=0)
    min = np.amin(windowPoints, axis=0)
    
    return (np.sum(max) + np.sum(min))