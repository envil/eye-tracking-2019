def handleWindowPoints(windowPoints): 
    xList = []
    yList = []
    for p in windowPoints:
        xList.append(p.getX())
        yList.append(p.getY())
    maxX = max(xList)
    minX = min(xList)
    maxY = max(yList)
    minY = min(yList)
    D = maxX - minX + maxY - minY
    return (D, xList, yList)