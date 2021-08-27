from A02_MCWD_Dataset_Analysis.Setup2016 import Setup2016
from A02_MCWD_Dataset_Analysis.Pylibs.MCWD_Analysis21 import MCWDFile
from A02_MCWD_Dataset_Analysis.Pylibs.scPDSI2021 import scPDSI
from A02_MCWD_Dataset_Analysis.Pylibs.PrecAnomalyDry21 import PrecAnomaly


import numpy as np
#import matplotlib.pylab as plt
import pandas
import os

rawData = pandas.read_csv(r"F:\Dropbox\ClimateData\Coords\SA_Amazon_basin\Amazon_basin_05_area.txt",
                     sep = ',',
                     header=0).values
areasRelative = rawData[:,4]
areasAbs = rawData[:,3]

years =[2005, 2010, 2016]


setup = Setup2016()
files = setup.files

def conditions(arr, i):
    if i == 1:
        return (arr < -0.5) & (arr > -2)
    if i == 2:
        return (arr <= -2) & (arr > -2.5)
    if i == 3:
        return (arr <= -2.5)
    return -1


df  = pandas.DataFrame()

for j in range(0, len(files)):

    fileSCPDSI = os.path.join(setup.scPDSIrootPAth, setup.files[j][2])
    fileMCWD = os.path.join(setup.MCWDrootPAth, setup.files[j][1])
    filePREC = os.path.join(setup.PRECrootPAth, setup.files[j][3])

    scPDSIfile = scPDSI(fileSCPDSI)
    absSCPSIData = scPDSIfile.ParseRelativeDeviation(2000, 2016)

    fileMcwd2 = MCWDFile(fileMCWD)
    yBegin, yEnd = fileMcwd2.GetBeginEnd()
    relMcwdData = fileMcwd2.ParseRelativeDeviation(yBegin, yEnd)
    absMcwdData = fileMcwd2.ParseAbsoluteDeviation(yBegin, yEnd)

    precFile = PrecAnomaly(filePREC)
    absPrecData = precFile.ParseRelativeDeviation(2001, 2016)


    for t in years:

        totalAreasMCWD = np.zeros((3))
        relAreasMCWD = np.zeros((3))

        totalAreasSCPDSI = np.zeros((3))
        relAreasSCPDSI = np.zeros((3))

        totalAreasPREC = np.zeros((3))
        relAreasPREC = np.zeros((3))



        for c in range(1, 4):
            arr = relMcwdData[t - yBegin]
            indexes = conditions(arr, c)

            arr_abs = absMcwdData[t - yBegin]
            mcwdLessZero = arr_abs[arr_abs < 0]
            biomassLoss = 0.3778 - 0.052* mcwdLessZero
            areaLessZero = areasAbs[arr_abs < 0]

            biomassLossPerSm = biomassLoss*areaLessZero*1000**2*100
            totalBiomassLossInPG = np.sum(biomassLossPerSm)/(10**15)

            totalAreasMCWD[c - 1] = np.sum(areasAbs[indexes])
            relAreasMCWD[c - 1] = np.sum(areasRelative[indexes])

            arr2 = absSCPSIData[t - 2000]
            indexes2 = conditions(arr2, c)
            totalAreasSCPDSI[c - 1] = np.sum(areasAbs[indexes2])
            relAreasSCPDSI[c - 1] = np.sum(areasRelative[indexes2])

            arr3 = absPrecData[t - 2001]
            indexes3 = conditions(arr3, c)
            totalAreasPREC[c - 1] = np.sum(areasAbs[indexes3])
            relAreasPREC[c - 1] = np.sum(areasRelative[indexes3])


            subdf = pandas.DataFrame({"Year": t,
                                  'Dataset': files[j][0],
                                  'Condition': range(1, 4),
                                  'TotalAreaMCWD': totalAreasMCWD,
                                  'RelativeAreaMCWD': relAreasMCWD,
                                  'DeltaAGB in PG per SM': totalBiomassLossInPG,
                                    'TotalAreaSCPDSI': totalAreasSCPDSI,
                                    'RelativeAreaSCPDSI': relAreasSCPDSI,
                                      'TotalAreaPrec': totalAreasPREC,
                                      'RelativeAreaPrec': relAreasPREC
                                  })

        df = df.append(subdf)


df.to_csv(r'2005-2010-2016Areas_var_baseline.tsv', sep= '\t', header = True)