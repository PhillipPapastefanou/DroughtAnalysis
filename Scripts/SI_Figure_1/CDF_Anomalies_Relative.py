
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
PrecSD = [-2.85, -1.9, -0.95 -0.45, 0.45, +0.95, 1.9, 2.85]
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
mean_scens_mcwd_abs =  []
mean_scens_scpdsi =  []

import string
lowerletters = string.ascii_lowercase[:26]


for j in range(0, len(scenNames)):

    fileSCPDSI = os.path.join(setup.scPDSIrootPAth, setup.files[j][2])
    fileMCWD = os.path.join(setup.MCWDrootPAth, setup.files[j][1])
    fileMCWDabbs = os.path.join(setup.MCWDrootPAth, setup.files[j][1])
    filePREC = os.path.join(setup.PRECrootPAth, setup.files[j][3])

    scPDSIfile = scPDSI(fileSCPDSI)
    absSCPSIData = scPDSIfile.ParseRelativeDeviation(2000, 2016)

    fileMcwd2 = MCWDFile(fileMCWD)
    absMcwdData = fileMcwd2.ParseRelativeDeviation(2001, 2016)

    fileMcwd3 = MCWDFile(fileMCWD)
    absMcwdDataABS = fileMcwd2.ParseAbsoluteDeviation(2001, 2016)

    precFile = PrecAnomaly(filePREC)
    absPrecData = precFile.ParseRelativeDeviation(2001, 2016)

    #if  (file[0]== "ER5")|(file[0] == "ERI"):
     #   dataMeanSpatial*= 2.9

    mean_scens_prec.append((ecdf(absPrecData.flatten()),  setup.files[j][0]))
    mean_scens_mcwd.append((ecdf(absMcwdData.flatten()),  setup.files[j][0]))
    mean_scens_scpdsi.append((ecdf(absSCPSIData.flatten()),  setup.files[j][0]))
    mean_scens_mcwd_abs.append((ecdf(absMcwdDataABS.flatten()),  setup.files[j][0]))

fig = plt.figure(figsize=(9, 8))

# a normal distribution with a mean of 0 and standard deviation of 1
n2 = stats.norm(loc=0, scale=1)

xlimrel = ((-3.5, 2))
xlimabs = ((-185, 79))
xticks_rel  = [- 2.5, -2.0,-1.5, -1.0,  -0.5, 0, 0.5, 1.0]
ytext = "Empirical CDF"

ax = fig.add_subplot(2, 2, 1)

ax.vlines(-132, 0, 0.35, color='black',linestyle='--', lw = 0.75)
ax.vlines(-106, 0, 0.35, color='black' ,linestyle='--', lw = 0.75)
ax.vlines(-26, 0, 0.35,color='black', linestyle='--',  lw = 0.75)

rect1 = matplotlib.patches.Rectangle((-106,-0), -26+106, 0.35, color='#FFB90F', alpha = 0.5)
rect2 = matplotlib.patches.Rectangle((-132,-0), -106+132, 0.35, color='#CD950C', alpha = 0.5)
rect3 = matplotlib.patches.Rectangle((-185,-0), -132+185, 0.35, color='#A52A2A', alpha = 0.5)

ax.text(0.36, 0.32, "moderate", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)

ax.text(0.19, 0.39, "severe", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)

ax.text(0.02, 0.32, "extreme", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)

ax.add_patch(rect1)
ax.add_patch(rect2)
ax.add_patch(rect3)
for vals, name in mean_scens_mcwd_abs:
    ax.plot(vals[0], vals[1], lw=1, label=name, c = 'tab:gray')
ax.set_xlim(xlimabs)
ax.set_ylabel(ytext)
ax.text(0.04, 0.90, lowerletters[0] + ")  $a$MCWD", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))

ax.set_xticks([ -159, -132, -106, -79, -53, -26, 0,26 ,53])
ax.set_xticklabels(ax.get_xticks(), rotation = 45)
ax.set_xlabel('Absolute Anomaly [mm]')
# compute the ECDF of the samples
ax = fig.add_subplot(2, 2, 2)



ax.vlines(-2.5, 0, 0.35, color='black',linestyle='--', lw = 0.75)
ax.vlines(-2, 0, 0.35, color='black' ,linestyle='--', lw = 0.75)
ax.vlines(-0.5, 0, 0.35,color='black', linestyle='--',  lw = 0.75)

rect1 = matplotlib.patches.Rectangle((-2,-0), 1.5, 0.35, color='#FFB90F', alpha = 0.5)
rect2 = matplotlib.patches.Rectangle((-2.5,-0), 0.5, 0.35, color='#CD950C', alpha = 0.5)
rect3 = matplotlib.patches.Rectangle((-3.5, -0),1.0, 0.35, color='#A52A2A', alpha = 0.5)
ax.add_patch(rect1)
ax.add_patch(rect2)
ax.add_patch(rect3)

ax.text(0.33, 0.32, "moderate", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)

ax.text(0.17, 0.39, "severe", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)

ax.text(0.02, 0.32, "extreme", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)

#ax.vlines(0, 0, 0.5 ,color='black', linestyle='-')
for vals, name in mean_scens_mcwd:
    ax.plot(vals[0], vals[1], lw=1, label=name, c = 'tab:gray')
ax.set_xlim(xlimrel)
ax.set_xticks(xticks_rel)
ax.set_xticklabels(ax.get_xticks(), rotation = 45)
ax.text(0.04, 0.90, lowerletters[1] + ")  $r$MCWD", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))

ax.set_xlabel('Standardized Anomaly')

ax = fig.add_subplot(2, 2, 3)

ax.vlines(-2.5, 0, 0.35, color='black',linestyle='--', lw = 0.75)
ax.vlines(-2, 0, 0.35, color='black' ,linestyle='--', lw = 0.75)
ax.vlines(-0.5, 0, 0.35,color='black', linestyle='--',  lw = 0.75)

rect1 = matplotlib.patches.Rectangle((-2,-0), 1.5, 0.35, color='#FFB90F', alpha = 0.5)
rect2 = matplotlib.patches.Rectangle((-2.5,-0), 0.5, 0.35, color='#CD950C', alpha = 0.5)
rect3 = matplotlib.patches.Rectangle((-3.5, -0),1.0, 0.35, color='#A52A2A', alpha = 0.5)
ax.add_patch(rect1)
ax.add_patch(rect2)
ax.add_patch(rect3)

ax.text(0.33, 0.32, "moderate", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)

ax.text(0.17, 0.39, "severe", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)

ax.text(0.02, 0.32, "extreme", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)
#ax.vlines(0, 0, 0.5 ,color='black', linestyle='-')
for vals, name in mean_scens_prec:
    ax.plot(vals[0], vals[1], lw=1, label=name, c = 'tab:gray')
ax.set_xlim(xlimrel)
ax.set_xticks(xticks_rel)
ax.set_xticklabels(ax.get_xticks(), rotation = 45)
ax.set_ylabel(ytext)
ax.text(0.04, 0.90, lowerletters[2] + ")  $r$RAI", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))

ax.set_xlabel('Standardized Anomaly')

ax = fig.add_subplot(2, 2, 4)
ax.vlines(-2.5, 0, 0.35, color='black',linestyle='--', lw = 0.75)
ax.vlines(-2, 0, 0.35, color='black' ,linestyle='--', lw = 0.75)
ax.vlines(-0.5, 0, 0.35,color='black', linestyle='--',  lw = 0.75)

rect1 = matplotlib.patches.Rectangle((-2,-0), 1.5, 0.35, color='#FFB90F', alpha = 0.5)
rect2 = matplotlib.patches.Rectangle((-2.5,-0), 0.5, 0.35, color='#CD950C', alpha = 0.5)
rect3 = matplotlib.patches.Rectangle((-3.5, -0),1.0, 0.35, color='#A52A2A', alpha = 0.5)
ax.add_patch(rect1)
ax.add_patch(rect2)
ax.add_patch(rect3)

ax.text(0.33, 0.32, "moderate", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)

ax.text(0.17, 0.39, "severe", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)

ax.text(0.02, 0.32, "extreme", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=8)

#ax.vlines(0, 0, 0.5 ,color='black', linestyle='-')
for vals, name in mean_scens_scpdsi:
    ax.plot(vals[0], vals[1], lw=1, label=name, c = 'tab:gray')
ax.set_xlim(xlimrel)
ax.set_xticks(xticks_rel)
ax.set_xticklabels(ax.get_xticks(), rotation = 45)
ax.text(0.04, 0.90, lowerletters[3] + ")  $r$scPDSI", horizontalalignment='left',
           verticalalignment='center',
           transform=ax.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))



ax.set_xlabel('Standardized Anomaly')

plt.subplots_adjust(hspace = 0.25)
#ax.legend(fancybox=True, loc='right')

plt.savefig("Empirical_CDF_Rainfalls_Rel.png", dpi=600, bbox_inches='tight',
                    pad_inches=0)






    #for i in range(0, 3):
     #   imgscPDSI = scPDSIData.CreateImage(scPDSIData.DataSlices[i])
    #    imgs.append(imgscPDSI)
        #img = precData.CreateImage(precData.DataSlices[i])





