from A02_MCWD_Dataset_Analysis.Analysis.OMAGeoParser import OMAGeoFile
import  numpy as np
import  pandas


class scPDSIFile:
    def __init__(self, fname, realFile):
        self.GeoFile = OMAGeoFile(fname)
        self.RealFile = realFile
        self.res = 0.5

    def ChangeResolution(self, res):
        self.res = res

    def Parse(self, yearsOfInterest, dataBegin, monstart = 6, monendInclusive = 8):


        data = pandas.read_csv(self.RealFile,
                                     sep=',',
                                     header=0).values[:, :]

        nYears = int(data.shape[1]/12)


        anomalyData = np.zeros((self.GeoFile.lons.shape[0], nYears))



        for i in range (0, nYears):

            iStart = monstart + 12*i
            iEnd= monendInclusive + 1 + 12*i

            u = data[:, iStart:iEnd]
            anomalyData[:, i ] = np.mean(u, axis = 1)
            #anomalyData[:, i ] = np.mean(data[:, 0 + 12*i : 3 + 12*i], axis = 1)

        self.Images= []
        self.DataSlices = []
        for i in range(0, len(yearsOfInterest)):
            dataSlice = anomalyData[:, yearsOfInterest[i] - dataBegin]
            self.DataSlices.append(dataSlice)
            self.Images.append(self.GeoFile.CreateImage(self.res, dataSlice, lat_flip=False))

    def CreateImage(self, data):
        return self.GeoFile.CreateImage(self.res, data, lat_flip=False)
