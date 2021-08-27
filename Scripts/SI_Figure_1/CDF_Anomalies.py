
from A02_MCWD_Dataset_Analysis.Pylibs.MCWD_Analysis21 import MCWDFile
from A02_MCWD_Dataset_Analysis.Pylibs.PrecAnomalyDry21 import PrecAnomaly
from A02_MCWD_Dataset_Analysis.Pylibs.scPDSI2021 import scPDSI
from A02_MCWD_Dataset_Analysis.Setup2016 import Setup2016

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
#import matplotlib.pylab as plt
import os

import matplotlib as mpl
import matplotlib.patheffects as PathEffects

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import matplotlib.patches as mpatches
from scipy import stats

def ecdf(sample):

    # convert sample to a numpy array, if it isn't already
    sample = np.atleast_1d(sample)

    # find the unique values and their corresponding counts
    quantiles, counts = np.unique(sample, return_counts=True)

    # take the cumulative sum of the counts and divide by the sample size to
    # get the cumulative probabilities between 0 and 1
    cumprob = np.cumsum(counts).astype(np.double) / sample.size

    return quantiles, cumprob


raisg_mask = r"F:\Dropbox\ClimateData\AmazonBasin\AB-SHAPE\amazon_shape.shp"
mask = ShapelyFeature(Reader(raisg_mask).geometries(),
                                 ccrs.PlateCarree())

#years =[2005, 2010]
PrecSD = [-3, -2, -1 -0.5, 0.5, 1, 2, 3]
cmapPrec = mpl.colors.ListedColormap(['red',
                                      'orange',
                                      'white',
                                      'green',
                                      'tab:blue',
                                        'blue'])


cmapPrec.set_over('blue')
cmapPrec.set_under('red')
normPrec = mpl.colors.BoundaryNorm(PrecSD, cmapPrec.N)



setup = Setup2016()

#files = []
#baseFilnames = []

#for r, d, f in os.walk(r"F:\Dropbox\UNI\TuM\PyTest\MCWDPaper\2005-2010-2016"):
#    for file in f:
#        if '.txt' in file:
#            files.append(os.path.join(r, file))
#            baseFilnames.append(file.replace(".txt", ""))


scenNames = setup.GetNames()

rowNames= ['a', 'b', 'c']

years = np.arange(2001, 2016)
mean_scens_prec =  []
mean_scens_mcwd =  []
mean_scens_scpdsi =  []


for j in range(0, len(scenNames)):

    fileSCPDSI = os.path.join(setup.scPDSIrootPAth, setup.files[j][2])
    fileMCWD = os.path.join(setup.MCWDrootPAth, setup.files[j][1])
    filePREC = os.path.join(setup.PRECrootPAth, setup.files[j][3])

    scPDSIfile = scPDSI(fileSCPDSI)
    absSCPSIData = scPDSIfile.ParseAbsoluteDeviation(2000, 2016)

    fileMcwd2 = MCWDFile(fileMCWD)
    absMcwdData = fileMcwd2.ParseAbsoluteDeviation(2001, 2016)

    precFile = PrecAnomaly(filePREC)
    absPrecData = precFile.ParseAbsoluteDeviation(2001, 2016)

    #if  (file[0]== "ER5")|(file[0] == "ERI"):
     #   dataMeanSpatial*= 2.9
    mean_scens_prec.append((ecdf(absPrecData.flatten()),  setup.files[j][0]))
    mean_scens_mcwd.append((ecdf(absMcwdData.flatten()),  setup.files[j][0]))
    mean_scens_scpdsi.append((ecdf(absSCPSIData.flatten()),  setup.files[j][0]))

fig = plt.figure(figsize=(9, 7))

# a normal distribution with a mean of 0 and standard deviation of 1
n2 = stats.norm(loc=0, scale=1)
# compute the ECDF of the samples
ax = fig.add_subplot(3, 1, 1)
for vals, name in mean_scens_prec:
    ax.plot(vals[0], vals[1], lw=1, label=name, color = "tab:red")
    xlim_min = np.quantile(vals[0], q= 0.001)
    xlim_max = np.quantile(vals[0], q= 0.999)
    ax.set_xlim((xlim_min,-xlim_min))

ax = fig.add_subplot(3, 1, 2)
for vals, name in mean_scens_mcwd:
    ax.plot(vals[0], vals[1], lw=1, label=name, color = "tab:blue")
    xlim_min = np.nanquantile(vals[0], q= 0.001)
    xlim_max = np.nanquantile(vals[0], q= 0.999)
    ax.set_xlim((xlim_min,-xlim_min))

ax = fig.add_subplot(3, 1, 3)
for vals, name in mean_scens_scpdsi:
    ax.plot(vals[0], vals[1], lw=1, label=name, color = "tab:green")
    xlim_min = np.nanquantile(vals[0], q= 0.001)
    xlim_max = np.nanquantile(vals[0], q= 0.999)
    ax.set_xlim((xlim_min,-xlim_min))

ax.set_ylabel('Quantile')
ax.set_xlabel('Monthly prec [mm/month]')
#ax.legend(fancybox=True, loc='right')

plt.savefig("Empirical_CDF_Rainfall_abs.png", dpi=300)






    #for i in range(0, 3):
     #   imgscPDSI = scPDSIData.CreateImage(scPDSIData.DataSlices[i])
    #    imgs.append(imgscPDSI)
        #img = precData.CreateImage(precData.DataSlices[i])





