import numpy as np

class BaseFile:
    def __init__(self, fname, res = 0.5):
        self.fname = fname
        self.res = res


    def CreateImage(self, data, lat_flip=True):
        return self.GeoFile.CreateImage(self.res, data, lat_flip)

    def GetData(self, yearFrom, yearTo):
        pass

    def GetMonthlyData(self, yearFrom, yearTo):
        pass

    def ParseAbsoluteDeviation(self, yearFrom, yearTo):
        self.yearFrom = yearFrom
        self.yearTo = yearTo
        data = self.GetData(yearFrom, yearTo)
        data_mean = np.mean(data, axis= 1)
        data_T = data.transpose() - data_mean
        return data_T

    def ParseRelativeDeviation(self, yearFrom, yearTo):
        self.yearFrom = yearFrom
        self.yearTo = yearTo
        data = self.GetData(yearFrom, yearTo)
        data_std = np.std(data, axis= 1)
        data_mean = np.mean(data, axis= 1)
        data_T = data.transpose()-  data_mean
        data_T /= data_std
        return data_T

    def ParseRelativeMonthly(self, yearFrom, yearTo):
        self.yearFrom = yearFrom
        self.yearTo = yearTo
        data = self.GetMonthlyData(yearFrom, yearTo)
        data2 = np.reshape(data, (1946,-1, 12))

        data_std = np.std(data2, axis= 1)
        data_mean = np.mean(data2, axis= 1)

        dataT = data.copy()
        for i in range (0, data.shape[1]):
            dataT[:, i] -= data_mean[: , i % 12]
            dataT[:, i] /= data_std [: , i % 12]
        return dataT