from A02_MCWD_Dataset_Analysis.Pylibs.PrecAnomalyPerMonth import PrecAnomalyMonthFile
from A02_MCWD_Dataset_Analysis.Analysis.OMAGeoParser import OMAGeoFile
import  numpy as np
from scipy import stats
import pandas as pd

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from A02_MCWD_Dataset_Analysis.Setup2016 import Setup2016

def ecdf(sample):

    # convert sample to a numpy array, if it isn't already
    sample = np.atleast_1d(sample)

    # find the unique values and their corresponding counts
    quantiles, counts = np.unique(sample, return_counts=True)

    # take the cumulative sum of the counts and divide by the sample size to
    # get the cumulative probabilities between 0 and 1
    cumprob = np.cumsum(counts).astype(np.double) / sample.size

    return quantiles, cumprob

#geoFileTRMM = OMAGeoFile(r"F:\Dropbox\ClimateData\AmazonBasin\MonthlyPrec\TRMM_V7_1998_2018_SA05.nc")

#yearFrom = geoFileTRMM.year_begin
#yearTo = geoFileTRMM.year_end
#data = geoFileTRMM.GetAllGridcellsYearSpan("prec", yearFrom, yearTo)
#dataMeanSpatialTRMM = np.nanmean(data.flatten(), axis=0)
#qeTR, peTR = ecdf(dataMeanSpatialTRMM)

#PRECrootPAth = r"F:\Dropbox\ClimateData\AmazonBasin\MonthlyPrec"

setup = Setup2016()



files = setup.files


mean_scens = []

for file in files:
    path = setup.scPDSIrootPAth + "\\" + file[2]



    data = pd.read_csv(path,
                           sep=',',
                           header=0).values[:, :]

    data[data < -9000] = np.nan

    nYears = int(data.shape[1] / 12)

    anomalyData = np.zeros((1946, nYears))


    #dataMeanSpatial = np.nanmean(data, axis=0)
    #if  (file[0]== "ER5")|(file[0] == "ERI"):
     #   dataMeanSpatial*= 2.9
    mean_scens.append((ecdf(data.flatten()), file[0]))





fig = plt.figure(figsize=(9,7))



# a normal distribution with a mean of 0 and standard deviation of 1
n2 = stats.norm(loc=0, scale=1)
# compute the ECDF of the samples

ax = fig.add_subplot(1, 1, 1)

outputCDF = []
i = 0
for vals,  name in mean_scens:
    ax.plot(vals[0], vals[1],  lw=1, label=name)

    x = []
    x.append("CDF")
    x.extend(vals[1].tolist())
    outputCDF.append(x)
    list = []
    list.append((name))
    list.extend(vals[0].tolist())
    outputCDF.append(list)


    i +=1


ax.set_ylabel('Empirical CDF')
ax.set_xlabel('SPEI [-]')
ax.set_xlim((-6, 6))
ax.legend(fancybox=True, loc='lower right')




plt.savefig("Empirical_CDF_SPEI.png", dpi = 300)


import csv

with open("outputCDF_SPEI.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(outputCDF)


u = 3