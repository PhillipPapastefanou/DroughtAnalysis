
from A02_MCWD_Dataset_Analysis.Analysis.OMAGeoParser import OMAGeoFile
import  numpy as np

class PrecAnomalyFile:

    def __init__(self, fname):
        self.GeoFile = OMAGeoFile(fname)
        self.res = 0.5

    def ChangeResolution(self, res):
        self.res = res


    def Parse(self, yearFrom, yearTo, yearExceptList, exclude = True):

        self.yearFrom = yearFrom
        self.yearTo = yearTo

        data = self.GeoFile.GetAllGridcellsYearSpan("prec", yearFrom, yearTo)


        nyears = yearTo - yearFrom + 1
        anomalyData = np.zeros((self.GeoFile.lons.shape[0], nyears))


        for i in range (0, nyears):
            anomalyData[:, i ] = np.mean(data[:, 6 + 12*i : 9 + 12*i], axis = 1)

        dataExceptAnomaliy = anomalyData

        if (exclude):
            for i in range(0, len(yearExceptList)):
                indexExcept = yearExceptList[i] - yearFrom
                dataExceptAnomaliy = np.delete(dataExceptAnomaliy, indexExcept - i, axis=1)

        self.MeanIntervallExcept = np.mean(dataExceptAnomaliy, axis= 1)
        self.SD  = np.std(dataExceptAnomaliy, axis= 1, ddof= 1)  # same as mathematica




        self.Images= []
        self.DataSlices = []
        for i in range(0, len(yearExceptList)):
            dataSlice = (anomalyData[:, yearExceptList[i] - yearFrom] - self.MeanIntervallExcept)/self.SD
            self.DataSlices.append(dataSlice)
            self.Images.append(self.GeoFile.CreateImage(self.res, dataSlice, lat_flip=False))

    def CreateImage(self, data):
        return self.GeoFile.CreateImage(self.res, data, lat_flip=True)