from A02_MCWD_Dataset_Analysis.Pylibs.MCWD_Analysis21 import MCWDFile
from A02_MCWD_Dataset_Analysis.Setup2016 import Setup2016
import numpy as np
#import matplotlib.pylab as plt
import pandas

rawData = pandas.read_csv(r"F:\Dropbox\ClimateData\Coords\SA_Amazon_basin\Amazon_basin_05_area.txt",
                     sep = ',',
                     header=0).values
areasRelative = rawData[:,4]
areasAbs = rawData[:,3]

setup = Setup2016()
MCWDrootPAth =setup.MCWDrootPAth
files = setup.files



MCWDFiles = []
data2016 = np.zeros((len(files), 1946))


for file in files:
    MCWDFiles.append(MCWDFile(MCWDrootPAth + "\\" + file[1]))

i = 0
for MCWDFile in MCWDFiles:
    data = MCWDFile.ParseRelativeDeviation(2001, 2016)
    data2016[i] = data[2016-2001]
    i += 1




dataCount = np.zeros((3, 1946))
#dataCount[0] = ((-100 < dataSlice) & (dataSlice < -25)).sum(axis = 0)
#dataCount[1]  = ((-150 < dataSlice) & (dataSlice  < -100)).sum(axis = 0)
#dataCount[2]  = (dataSlice < -150).sum(axis = 0)

dataSlice = data2016
dataCount[0] = (dataSlice < -0.5).sum(axis = 0)
dataCount[1]  = (dataSlice < -2.0).sum(axis = 0)
dataCount[2]  = (dataSlice < -2.5).sum(axis = 0)


years = []

df  = pandas.DataFrame()
acc = np.zeros((len(files), 6))

for d in range(0, 3):
    for j in range(0, len(files)):
        indexes = dataCount[d] == (j + 1)
        acc[j,d] = np.sum(areasAbs[indexes])

        subdf = pandas.DataFrame({"Year": 2016,
                                  'Dataset': files[j][0],
                                  'Condition': d % 3,
                                  'TotalArea': acc[j,d],
                                  'RelativeArea': np.sum(areasRelative[indexes])
                                  }, index=[0])
        df = df.append(subdf)


df.to_csv(r'2016Agreement.tsv', sep= '\t', header = True)


