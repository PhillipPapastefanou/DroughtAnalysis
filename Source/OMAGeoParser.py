import numpy as np
from enum import Enum
from Source.Scaling import ScalerListToArray

from Source.OMAoutput import OMAFile
from Source.OMAoutput import TimeDomain

class OMAGeoFile:
    def __init__(self, path):
        self.path = path
        file = OMAFile(self.path)
        self.lons = file.nc.variables['lon'][:]
        self.lats = file.nc.variables['lat'][:]
        file.Close()




    def GetAllGridcellsYearSpan(self, var, yearBegin, yearEnd):
        file = OMAFile(self.path)
        data = file.GetYear(var, yearBeginOfInterest=yearBegin, yearEndOfInterest= yearEnd, gridcellBegin=0, gridcellEnd=file.gridcellDim.size)
        file.Close()
        return data

    def GetYearSpan(self, var, gbegin, gend, yearBegin, yearEnd):
        file = OMAFile(self.path)
        data = file.GetYear(var, yearBeginOfInterest=yearBegin, yearEndOfInterest= yearEnd, gridcellBegin=gbegin, gridcellEnd=gend)
        file.Close()
        return data

    def GetAllGridcellsDay(self, var, yearBegin, day):
        file = OMAFile(self.path)
        data = file.GetDay(var, yearBeginOfInterest=yearBegin, day=day, gridcellBegin=0, gridcellEnd=file.gridcellDim.size)
        file.Close()
        return data


    def CreateImage(self, res, data):

        lonScaler = ScalerListToArray(self.lons, res, False)
        latScaler = ScalerListToArray(self.lats, res, False)
        lonIndexes = lonScaler.Indexes
        latIndexes = latScaler.Indexes
        xlen = lonScaler.len
        ylen = latScaler.len
        self.IMG_extent = [lonScaler.min, lonScaler.max, latScaler.min, latScaler.max]

        image = np.empty((ylen + 1, xlen + 1,)) * np.nan
        for i in range(len(self.lons)):
            image[latIndexes[i], lonIndexes[i]] = data[i]

        return image
