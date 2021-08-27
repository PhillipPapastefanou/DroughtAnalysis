
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


raisg_mask = r"F:\Dropbox\ClimateData\AmazonBasin\AB-SHAPE\amazon_shape.shp"
mask = ShapelyFeature(Reader(raisg_mask).geometries(),
                                 ccrs.PlateCarree())

#years =[2005, 2010]
PrecSD = [-2.85, -1.9, -0.95 -0.45, 0.45, +0.95, 1.9, 2.85]
PrecSD = [-2.5, -2, -0.5]
cmapPrec = mpl.colors.ListedColormap([
                                      (205/255, 149/255, 12/255),
                                      (255/255, 185/255, 15/255)
                                      ])


uColor = ((165 / 255, 42 / 255, 42 / 255))
oColor = 'white'
cmapPrec.set_under(uColor)
cmapPrec.set_over(oColor)
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

rowNames= ['a', 'b', 'c', 'd', 'e', 'f']

years = [2005, 2010, 2016]

imgs = []

for j in range(0, len(scenNames)):

    fileSCPDSI = os.path.join(setup.scPDSIrootPAth, setup.files[j][2])
    fileMCWD = os.path.join(setup.MCWDrootPAth, setup.files[j][1])
    filePREC = os.path.join(setup.PRECrootPAth, setup.files[j][3])

    scPDSIfile = scPDSI(fileSCPDSI)
    absSCPSIData = scPDSIfile.ParseRelativeDeviation(2000, 2016)

    fileMcwd2 = MCWDFile(fileMCWD)
    absMcwdData = fileMcwd2.ParseRelativeDeviation(2001, 2016)

    precFile = PrecAnomaly(filePREC)
    absPrecData = precFile.ParseRelativeDeviation(2001, 2016)





    #for i in range(0, 3):
    #    imgPREC = precData.CreateImage(precData.DataSlices[i])
    #    imgs.append(imgPREC)

    for i in [2016]:
        imgPREC = precFile.CreateImage(absPrecData[i - 2001])
        #imgs.append(imgPREC)

    for i in [2016]:
        imgMCWD = fileMcwd2.CreateImage(absMcwdData[i - 2001])
        imgs.append(imgMCWD)

    for i in [2016]:
        imgscPDSI = scPDSIfile.CreateImage(absSCPSIData[i - 2000])
        #imgs.append(imgscPDSI)


    #for i in range(0, 3):
     #   imgscPDSI = scPDSIData.CreateImage(scPDSIData.DataSlices[i])
    #    imgs.append(imgscPDSI)
        #img = precData.CreateImage(precData.DataSlices[i])


fig = plt.figure(figsize=(13, 8))
index = 1
for i in range(0, len(scenNames)):
    img_extent = fileMcwd2.GeoFile.IMG_extent
    offset = [-3, 3, -3, 3]

    axGeo = fig.add_subplot(2, 3, index, projection=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True, number_format='g')
    lat_formatter = LatitudeFormatter()
    axGeo.xaxis.set_major_formatter(lon_formatter)
    axGeo.yaxis.set_major_formatter(lat_formatter)
    axGeo.add_feature(cfeature.BORDERS, edgecolor='tab:grey')
    axGeo.coastlines(resolution='110m', linewidth=1, color='tab:grey')
    # axGeo.set_title("Precipitation")
    axGeo.set_extent(list(np.array(img_extent) + np.array(offset)), crs=ccrs.PlateCarree())
    axGeo.add_feature(mask, edgecolor='black', linewidth=1.3, facecolor="None")
    axGeo.text(0.03, 0.93, rowNames[index - 1] + ")", horizontalalignment='left',
            verticalalignment='center',
            transform=axGeo.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    axGeo.text(0.97, 0.93, scenNames[index-1], horizontalalignment='right', verticalalignment='center',
            transform=axGeo.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))

    #if i < 3:
        #titleTxt = axGeo.set_title(years[i], size=16)
        #titleTxt.set_path_effects([PathEffects.withStroke(linewidth=1, foreground='black')])

    axGeo.set_xticks([-80, -70, -60, -50], crs=ccrs.PlateCarree())
    axGeo.set_yticks([-20, -15, -10, -5, 0, 5], crs=ccrs.PlateCarree())


    if index > 3:
        axGeo.set_xlabel(r'Longitude')

    if (index == 1 )| (index == 4):
        axGeo.set_ylabel(r'Latitude')

    cmap = cmapPrec
    norm = normPrec

    imsh = axGeo.imshow(imgs[i], transform=ccrs.PlateCarree(), extent=img_extent, cmap=cmap, norm=norm)
    index += 1


plt.subplots_adjust(bottom=0.25, wspace=0.4, hspace = 0.0)

 #cax = plt.axes([0.126, 0.20, 0.775, 0.02])
 #bar = plt.colorbar(imsh, cax=cax, orientation="horizontal")
#cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
    #                                norm=norm,
    #                                orientation='horizontal', boundaries= bounds, ticks = bounds, format='%1i')
patches = []
d = 0
     #patches.append(mpatches.Patch(label=  'x < -4', facecolor ='#fe0003' , edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '-4 < x < -3', facecolor = cmapPDSI.colors[0], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '-3 < x < -2', facecolor = cmapPDSI.colors[1], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '-2 < x < -1', facecolor = cmapPDSI.colors[2], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '-1 < x < 1', facecolor = cmapPDSI.colors[3], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '1 < x < 2', facecolor = cmapPDSI.colors[4], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '2 < x < 3', facecolor = cmapPDSI.colors[5], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '3 < x < 4', facecolor = cmapPDSI.colors[6], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '> 4', facecolor =  "#55017b", edgecolor='black'))

patches.append(mpatches.Patch(label='x < -2.5', facecolor= uColor, edgecolor='black'))
patches.append(mpatches.Patch(label='-2.5 < x < -2', facecolor=cmapPrec.colors[0], edgecolor='black'))
patches.append(mpatches.Patch(label='-2 < x < -0.5', facecolor=cmapPrec.colors[1], edgecolor='black'))
#patches.append(mpatches.Patch(label='-2 < x < -0.5', facecolor=cmapPrec.colors[2], edgecolor='black'))
patches.append(mpatches.Patch(label='-0.5 < x', facecolor=oColor, edgecolor='black'))

fig.tight_layout()
legend = fig.legend(handles=patches[0:5], loc='lower center', prop={"size": 16}, title="Relative MCWD anomaly ($r$MCWD)", frameon=False, ncol=5,
                    bbox_to_anchor=(0.5, -0.10))

legend.get_title().set_fontsize('16') #legend 'Title' fontsize

legend.get_frame().set_edgecolor('black')


legend = fig.legend(handles=[], loc='lower center', prop={"size": 16}, title="$\Longleftarrow$ Increasing drought stress $\Longleftarrow$", frameon=False, ncol=1,
                    bbox_to_anchor=(0.5, -0.15))
legend.get_title().set_fontsize('14') #legend 'Title' fontsize

    # plt.show()
    #print(baseFileNames[j])
plt.savefig("Figure1_relative_2016.jpg", dpi=600, bbox_inches='tight',
                    pad_inches=0)


