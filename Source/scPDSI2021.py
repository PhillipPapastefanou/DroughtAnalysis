from A02_MCWD_Dataset_Analysis.Pylibs.BaseAnalysis import BaseFile
import numpy as np
from A02_MCWD_Dataset_Analysis.Analysis.OMAGeoParser import OMAGeoFile
import pandas as pd

class scPDSI(BaseFile):
    def __init__(self, fileName, res = 0.5):
        super(scPDSI, self).__init__(fileName, res)
        self.GeoFile = OMAGeoFile(r"F:\Dropbox\ClimateData\AmazonBasin\MonthlyPrec\CHRIPS_AB_monthly_05.nc")
        self.RealFile = fileName


    def GetData(self, yearFrom, yearTo):

        data = pd.read_csv(self.RealFile,
                                     sep=',',
                                     header=0).values[:, :]
        monstart = 6
        monendInclusive = 8

        nYears = int(data.shape[1]/12)
        nyears = yearTo - yearFrom + 1
        anomalyData = np.zeros((self.GeoFile.lons.shape[0], nyears +1))
        for i in range (0, nYears):

            iStart = monstart + 12*i
            iEnd= monendInclusive + 1 + 12*i

            u = data[:, iStart:iEnd]
            anomalyData[:, i] = np.mean(u, axis = 1)

        return anomalyData


    def GetMonthlyData(self, yearFrom, yearTo):
        data = pd.read_csv(self.RealFile,
                           sep=',',
                           header=0).values[:, :]


        return data