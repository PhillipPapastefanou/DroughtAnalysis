from MCWDPaper.OMAGeoParser import OMAGeoFile
import  numpy as np

class CWDFile:
    def __init__(self, fname):
        self.GeoFile = OMAGeoFile(fname)
        self.res = 0.5

    def ChangeResolution(self, res):
        self.res = res

    def Parse(self, yearFrom, yearTo, yearsOfInterest, quantiles):

        self.yearFrom = yearFrom
        self.yearTo = yearTo

        data = self.GeoFile.GetAllGridcellsYearSpan("cwd", yearFrom, yearTo)

        self.DataSlices = np.zeros((len(quantiles), len(yearsOfInterest), 12))
        qindex = 0


        for q in quantiles:

            anomalyData = np.quantile(data, q, axis=0)

            anomalyData[anomalyData > 1] = np.nan

            self.OverallMean = np.nanmean(np.split(anomalyData, data.shape[1]/12), axis= 0)


            for i in range(0, len(yearsOfInterest)):
                dataSlice = anomalyData[(yearsOfInterest[i] - yearFrom) * 12:
                                        (yearsOfInterest[i] - yearFrom + 1) * 12] - self.OverallMean
                self.DataSlices[qindex, i] = dataSlice

            qindex += 1

