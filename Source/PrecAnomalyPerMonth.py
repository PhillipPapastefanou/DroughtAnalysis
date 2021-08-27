from A02_MCWD_Dataset_Analysis.Analysis.OMAGeoParser import OMAGeoFile
import  numpy as np

class PrecAnomalyMonthFile:

    def __init__(self, fname):
        self.GeoFile = OMAGeoFile(fname)
        self.res = 0.5

    def ChangeResolution(self, res):
        self.res = res


    def Parse(self, yearFrom, yearTo, yearsOfInterest, quantiles):

        self.yearFrom = yearFrom
        self.yearTo = yearTo

        data = self.GeoFile.GetAllGridcellsYearSpan("prec", yearFrom, yearTo)

        self.DataSlices = np.zeros((len(quantiles), len(yearsOfInterest), 12))
        qindex = 0

        for q in quantiles:


            nyears = yearTo - yearFrom + 1

            # mean calculation
            #anomalyData = np.mean(data, axis=0)

            # quantile calculation
            anomalyData = np.quantile(data, q, axis=0)

            self.OverallMean = np.mean(np.split( anomalyData, data.shape[1]/12), axis= 0)
            self.OverallStd = np.std(np.split( anomalyData, data.shape[1]/12), axis= 0)

            for i in range(0, len(yearsOfInterest)):
                dataSlice = (anomalyData[(yearsOfInterest[i] - yearFrom) * 12: (yearsOfInterest[
                                                                                   i] - yearFrom + 1) * 12] - self.OverallMean)/self.OverallStd
                self.DataSlices[qindex, i] = dataSlice

            qindex += 1

