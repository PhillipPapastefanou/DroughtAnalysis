from A02_MCWD_Dataset_Analysis.Pylibs.BaseAnalysis import BaseFile
import numpy as np
from A02_MCWD_Dataset_Analysis.Analysis.OMAGeoParser import OMAGeoFile

class PrecAnomaly(BaseFile):
    def __init__(self, fileName, res = 0.5):
        super(PrecAnomaly, self).__init__(fileName, res)
        self.GeoFile = OMAGeoFile(fileName)


    def GetData(self, yearFrom, yearTo):
        data = self.GeoFile.GetAllGridcellsYearSpan("prec", yearFrom, yearTo)
        nyears = yearTo - yearFrom + 1
        anomalyData = np.zeros((self.GeoFile.lons.shape[0], nyears))
        for i in range (0, nyears):
            anomalyData[:, i] = np.mean(data[:, 6 + 12*i : 9 + 12*i], axis = 1)

        return anomalyData

    def GetData(self, yearFrom, yearTo):
        data = self.GeoFile.GetAllGridcellsYearSpan("prec", yearFrom, yearTo)
        nyears = yearTo - yearFrom + 1
        anomalyData = np.zeros((self.GeoFile.lons.shape[0], nyears))
        for i in range (0, nyears):
            anomalyData[:, i] = np.mean(data[:, 6 + 12*i : 9 + 12*i], axis = 1)

        return anomalyData

    def GetMonthlyData(self, yearFrom, yearTo):
        data = self.GeoFile.GetAllGridcellsYearSpan("prec", yearFrom, yearTo)
        return data

