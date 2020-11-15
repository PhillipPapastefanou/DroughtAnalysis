import numpy as np
from enum import  Enum
from datetime import datetime
from datetime import timedelta

from netCDF4 import Dataset

class TimeDomain(Enum):
    Daily = 3
    Monthly = 2
    Annually = 1

class Dimension:
    def __init__(self, name, id, size):
        self.id = id
        self.name = name
        self.size = size

class OMAFile:
    def __init__(self, path):
        self.path = path
        self.nc = Dataset(path, 'r')

        foundTimeDim = False
        foundGridcellDim = False

        for dim in self.nc.dimensions:
            if dim.lower() == 'time':
                ncTimeDim = self.nc.dimensions[dim]
                self.timeDim = Dimension(ncTimeDim.name, ncTimeDim._dimid, ncTimeDim.size)
                foundTimeDim = True

            if dim.lower() == 'station':
                ncGridcellDim = self.nc.dimensions[dim]
                self.gridcellDim = Dimension(ncGridcellDim.name, ncGridcellDim._dimid, ncGridcellDim.size)
                foundGridcellDim = True

        if foundTimeDim == False:
            print("No Time dimension found")
            exit(1)

        if foundGridcellDim == False:
            print("No Gridcell dimension found")
            exit(1)


        foundTimeVar = False
        for var in self.nc.variables:
            if var.lower() == 'time':
                timeVar = self.nc.variables[var]
                foundTimeVar = True


        if foundTimeVar == False:
            print("No Time variable found")
            exit(1)


        sinceString  = timeVar.units
        timeStringData = str.split(sinceString, ' since ')
        timeToken = timeStringData[0]
        beginDate= timeStringData[1]

        beginDateData = str.split(beginDate, '.')

        if len(beginDateData) == 3:
            self.yearBegin = int(beginDateData[2])
            self.monthBegin = int(beginDateData[1])
            self.dayBegin = int(beginDateData[0])

        #check is splitting was sucessfull, if not parse datetime in another way
        elif len(beginDateData) == 1:
            beginDateData = str.split(beginDate,'-')

            #todo improve the following section
            if  int(beginDateData[0]) > 99:
                self.yearBegin = int(beginDateData[0])
                self.monthBegin = int(beginDateData[1])
                self.dayBegin = 1
            else:
                self.yearBegin = int(beginDateData[2])
                self.monthBegin = int(beginDateData[1])
                self.dayBegin = 1


        if (timeToken == "days"):
            self.multiplier = 365
            self.timeDomain = TimeDomain.Daily
        elif (timeToken == "months"):
            self.multiplier = 12
            self.timeDomain = TimeDomain.Monthly
        elif(timeToken == "years"):
            self.multiplier = 1
            self.timeDomain = TimeDomain.Annually

        else:
            print('Invalid TimeDomain')

        timeData = timeVar[:]

        self.timeSteps = timeData.size

        self.yearEnd = self.yearBegin + int(timeData[self.timeSteps-1] / self.multiplier)

        #self.nc.close()


    def GetTime(self, yearBegin, yearEnd):
        return self.split(yearBegin, yearEnd + 1, (yearEnd-yearBegin + 1)*self.multiplier)

    def GetYear(self, varName, gridcellBegin, gridcellEnd, yearBeginOfInterest, yearEndOfInterest):

        timeOffset= (yearBeginOfInterest - self.yearBegin)*self.multiplier
        timeEnd = (yearEndOfInterest - self.yearBegin + 1)*self.multiplier

        ncVariable = self.nc.variables[varName]

        offset = np.zeros(ncVariable.ndim,int)
        end = np.zeros(ncVariable.ndim, int)

        id = 0
        for varDim in ncVariable.dimensions:
            if (varDim == self.gridcellDim.name):
                offset[id] = gridcellBegin
                end[id] = gridcellEnd + 1
            if (varDim == self.timeDim.name):
                offset[id] = timeOffset
                end[id] = timeEnd
            id+=1

        data = ncVariable[offset[0]:end[0], offset[1]: end[1]]
        return np.squeeze(data)

    def GetDay(self, varName, gridcellBegin, gridcellEnd, yearBeginOfInterest, day):

        timeOffset= (yearBeginOfInterest - self.yearBegin)*self.multiplier + day
        timeEnd = timeOffset + 1

        ncVariable = self.nc.variables[varName]

        offset = np.zeros(ncVariable.ndim,int)
        end = np.zeros(ncVariable.ndim, int)

        id = 0
        for varDim in ncVariable.dimensions:
            if (varDim == self.gridcellDim.name):
                offset[id] = gridcellBegin
                end[id] = gridcellEnd + 1
            if (varDim == self.timeDim.name):
                offset[id] = timeOffset
                end[id] = timeEnd
            id+=1

        data = ncVariable[offset[0]:end[0], offset[1]: end[1]]
        return np.squeeze(data)


    def Close(self):
        self.nc.close()


    def split(self, x, y, n):
        vals = np.zeros(n)
        for i in range(0,n):
            vals[i] = x + i*(y-x)/n
        return vals













