from A02_MCWD_Dataset_Analysis.Analysis.OMAGeoParser import OMAGeoFile
import  numpy as np

class MCWDFile:
    def __init__(self, fname):
        self.GeoFile = OMAGeoFile(fname)
        self.res = 0.5

    def ChangeResolution(self, res):
        self.res = res

    def Parse(self, yearFrom, yearTo, yearExceptList, exclude = True):

        self.yearFrom = yearFrom
        self.yearTo = yearTo

        data = self.GeoFile.GetAllGridcellsYearSpan("mcwd", yearFrom, yearTo)
        dataExcept = data

        if(exclude):
            for i in range(0, len(yearExceptList)):
                indexExcept = yearExceptList[i] - yearFrom
                dataExcept = np.delete(dataExcept, indexExcept - i, axis=1)

        self.MeanIntervallExcept = np.mean(dataExcept, axis= 1)

        self.Images= []
        self.DataSlices = []
        for i in range(0, len(yearExceptList)):
            dataSlice = data[:, yearExceptList[i] - yearFrom] - self.MeanIntervallExcept
            self.DataSlices.append(dataSlice)
            self.Images.append(self.GeoFile.CreateImage(self.res, dataSlice, False))

    def ParseRange(self, yearFrom, yearTo, yearMeanFrom, yearMeanTo):

        dataMean = self.GeoFile.GetAllGridcellsYearSpan("mcwd", yearMeanFrom, yearMeanTo)
        self.MeanIntervallExcept = np.mean(dataMean, axis=1)

        data = self.GeoFile.GetAllGridcellsYearSpan("mcwd", yearFrom, yearTo)

        #self.DataSlices = []
        #for i in range(0, yearTo-yearFrom+1):
        #    dataSlice = data[:, i] - self.MeanIntervallExcept
        #    self.DataSlices.append(dataSlice)

        return  data - self.MeanIntervallExcept[:, np.newaxis]

    def ParseSingle(self, year, yearMeanFrom, yearMeanTo):

        dataMean = self.GeoFile.GetAllGridcellsYearSpan("mcwd", yearMeanFrom, yearMeanTo)
        self.MeanIntervallExcept = np.mean(dataMean, axis=1)

        data = self.GeoFile.GetAllGridcellsYearSpan("mcwd", year, year)

        #self.DataSlices = []
        #for i in range(0, yearTo-yearFrom+1):
        #    dataSlice = data[:, i] - self.MeanIntervallExcept
        #    self.DataSlices.append(dataSlice)

        return  data - self.MeanIntervallExcept


    def CreateImage(self, data):
        return self.GeoFile.CreateImage(self.res, data, lat_flip=False)


