from A02_MCWD_Dataset_Analysis.Pylibs.BaseAnalysis import BaseFile
import numpy as np
from A02_MCWD_Dataset_Analysis.Analysis.OMAGeoParser import OMAGeoFile

class MCWDFile(BaseFile):
    def __init__(self, fileName, res = 0.5):
        super(MCWDFile, self).__init__(fileName, res)
        self.GeoFile = OMAGeoFile(fileName)

    def GetBeginEnd(self):
        return self.GeoFile.year_begin, self.GeoFile.year_end

    def GetData(self, yearFrom, yearTo):
        return self.GeoFile.GetAllGridcellsYearSpan("mcwd", yearFrom, yearTo)

    def GetMonthlyData(self, yearFrom, yearTo):
        return self.GeoFile.GetAllGridcellsYearSpan("cwd", yearFrom, yearTo)







