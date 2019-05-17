def getConfigParameters(settingNumber):
    HORIZONTAL_UNIT = 97
    VERTICAL_UNIT = 56

    # Convert Degree to Unit
    DEGREE_IN_UNIT = HORIZONTAL_UNIT + VERTICAL_UNIT 

    if settingNumber == 1:
        #FIRST SETTING:
        # Choose dispersion-threshold to be 2 degree & duration-threshold to be 50ms = 0.05s
        return (2*DEGREE_IN_UNIT , 0.05)
    elif settingNumber == 2:
        #SECOND SETTING:
        # Choose dispersion-threshold to be 1 degree & duration-threshold to be 70ms = 0.07s
        return (DEGREE_IN_UNIT, 0.07)