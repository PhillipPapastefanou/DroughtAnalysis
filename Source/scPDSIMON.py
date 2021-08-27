from MCWDPaper.OMAGeoParser import OMAGeoFile
import  numpy as np
import  pandas

class scPDSIFileMonthly:
    def __init__(self, fname,realFile):
        self.GeoFile = OMAGeoFile(fname)
        self.RealFile = realFile
        self.res = 0.5

    def ChangeResolution(self, res):
        self.res = res

    def Parse(self, yearFrom, yearTo, yearsOfInterest, quantiles):

        self.yearFrom = yearFrom
        self.yearTo = yearTo

        data = pandas.read_csv(self.RealFile,
                                     sep=',',
                                     header=0).values[:, :]


        self.DataSlices = np.zeros((len(quantiles), len(yearsOfInterest), 12))
        qindex = 0


        for q in quantiles:

            anomalyData = np.nanquantile(data, q, axis=0)

            anomalyData[anomalyData > 1000] = np.nan

            self.OverallMean = np.nanmean(np.split(anomalyData, data.shape[1]/12), axis= 0)


            for i in range(0, len(yearsOfInterest)):
                dataSlice = anomalyData[(yearsOfInterest[i] - yearFrom) * 12:
                                        (yearsOfInterest[i] - yearFrom + 1) * 12] - self.OverallMean
                self.DataSlices[qindex, i] = dataSlice

            qindex += 1
