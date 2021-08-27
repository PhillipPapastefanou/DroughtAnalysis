
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

years =[2005, 2010, 2016]
MCWD = [-200, -200, -150, -100, -25, -25]
cmapMCWD = mpl.colors.ListedColormap([(165 / 255, 42 / 255, 42 / 255),
                                      (205/255, 149/255, 12/255),
                                      (255/255, 185/255, 15/255),
                                      (238/255, 232/255, 205/255),
                                  'white'])
cmapMCWD.set_over('white')
cmapMCWD.set_under((165 / 255, 42 / 255, 42 / 255))
normMCWD = mpl.colors.BoundaryNorm(MCWD, cmapMCWD.N)




#years =[2005, 2010]
PrecSD = [-50, -50, -25, 0, 25, 50, 50]
cmapPrec = mpl.colors.ListedColormap(['red',
                                      'orange',
                                      'white',
                                      'green',
                                      'tab:blue',
                                  'blue'])
cmapPrec.set_over('blue')
cmapPrec.set_under('red')
normPrec = mpl.colors.BoundaryNorm(PrecSD, cmapPrec.N)

scPDSIBoundary = [-3, -2, -1 -0.5, 0.5, 1, 2, 3]
cmapPDSI = mpl.colors.ListedColormap([
                                    '#ff7401',
                                    '#ffb204',
                                      '#ffeb00',
                                      '#ffffff',
                                      '#01ffc3',
                                      '#01dafd',
                                      '#0c00fa',
                                      ])
cmapPDSI.set_over('#55017b')
cmapPDSI.set_under('#fe0003')
normPDSI = mpl.colors.BoundaryNorm(scPDSIBoundary, cmapPDSI.N)

# TAKE ONLY NEGATIVE VALUES
scPDSIBoundary = [-4, -3, -2]
cmapPDSI = mpl.colors.ListedColormap([
                                    '#ff7401',
                                      '#ffeb00'
                                      ])
cmapPDSI.set_over('white')
cmapPDSI.set_under('#fe0003')
normPDSI = mpl.colors.BoundaryNorm(scPDSIBoundary, cmapPDSI.N)




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


    fig = plt.figure(figsize=(10, 8))

    imgs = []
    #for i in range(0, 3):
    #    imgPREC = precData.CreateImage(precData.DataSlices[i])
    #    imgs.append(imgPREC)

    for i in [2005, 2010, 2016]:
        imgPREC = precFile.CreateImage(absPrecData[i - 2001])
        imgs.append(imgPREC)

    for i in [2005, 2010, 2016]:
        imgMCWD = fileMcwd2.CreateImage(absMcwdData[i - 2001])
        imgs.append(imgMCWD)

    for i in [2005, 2010, 2016]:
        imgscPDSI = scPDSIfile.CreateImage(absSCPSIData[i - 2000])
        imgs.append(imgscPDSI)


    #for i in range(0, 3):
     #   imgscPDSI = scPDSIData.CreateImage(scPDSIData.DataSlices[i])
    #    imgs.append(imgscPDSI)
        #img = precData.CreateImage(precData.DataSlices[i])



    index = 1
    for i in range(0, 9):
        #imgMCWD = mcwdData.CreateImage(mcwdData.DataSlices[i])
        #img = precData.CreateImage(precData.DataSlices[i])
        #imgscPDSI = scPDSIData.CreateImage(scPDSIData.DataSlices[i])

        img_extent = fileMcwd2.GeoFile.IMG_extent
        offset = [-3, 3, -3, 3]

        axGeo = fig.add_subplot(3, 3, index, projection=ccrs.PlateCarree())
        lon_formatter = LongitudeFormatter(zero_direction_label=True, number_format='g')
        lat_formatter = LatitudeFormatter()
        axGeo.xaxis.set_major_formatter(lon_formatter)
        axGeo.yaxis.set_major_formatter(lat_formatter)
        axGeo.add_feature(cfeature.BORDERS, edgecolor='tab:grey')
        axGeo.coastlines(resolution='110m', linewidth=1, color='tab:grey')
        # axGeo.set_title("Precipitation")
        axGeo.set_extent(list(np.array(img_extent) + np.array(offset)), crs=ccrs.PlateCarree())
        axGeo.add_feature(mask, edgecolor='black', linewidth=1.3, facecolor="None")
       # axGeo.text(-81, 5, str(rowNames[index - 1]) + ')',
       #            fontsize=16, fontweight='bold', horizontalalignment='left', verticalalignment='center',
       #            bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))

        if i < 3:
            titleTxt = axGeo.set_title(years[i], size=16)
            titleTxt.set_path_effects([PathEffects.withStroke(linewidth=1, foreground='black')])

        axGeo.set_xticks([-80, -70, -60, -50], crs=ccrs.PlateCarree())
        axGeo.set_yticks([-20, -15, -10, -5, 0, 5], crs=ccrs.PlateCarree())
        axGeo.set_xlabel(r'Longitude')
        axGeo.set_ylabel(r'Latitude')
        if(i  < 3):
            cmap = cmapPrec
            norm = normPrec
        elif(i  < 6):
            cmap = cmapMCWD
            norm = normMCWD
        elif ( i < 9):
            cmap = cmapPDSI
            norm = normPDSI

        imsh = axGeo.imshow(imgs[i], transform=ccrs.PlateCarree(), extent=img_extent, cmap=cmap, norm=norm)
        index += 1

    plt.subplots_adjust(bottom=0.25, wspace=0.1)

    # cax = plt.axes([0.126, 0.20, 0.775, 0.02])
    # bar = plt.colorbar(imsh, cax=cax, orientation="horizontal")
    # cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
    #                                norm=norm,
    #                                orientation='horizontal', boundaries= bounds, ticks = bounds, format='%1i')
    patches = []
    d = 0
    # patches.append(mpatches.Patch(label=  'x < -4', facecolor ='#fe0003' , edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '-4 < x < -3', facecolor = cmapPDSI.colors[0], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '-3 < x < -2', facecolor = cmapPDSI.colors[1], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '-2 < x < -1', facecolor = cmapPDSI.colors[2], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '-1 < x < 1', facecolor = cmapPDSI.colors[3], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '1 < x < 2', facecolor = cmapPDSI.colors[4], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '2 < x < 3', facecolor = cmapPDSI.colors[5], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '3 < x < 4', facecolor = cmapPDSI.colors[6], edgecolor='black'))
    # patches.append(mpatches.Patch(label=  '> 4', facecolor =  "#55017b", edgecolor='black'))

    patches.append(mpatches.Patch(label='x < -4', facecolor='#fe0003', edgecolor='black'))
    patches.append(mpatches.Patch(label='-4 < x < -3', facecolor=cmapPDSI.colors[0], edgecolor='black'))
    patches.append(mpatches.Patch(label='-3 < x < -2', facecolor=cmapPDSI.colors[1], edgecolor='black'))
    patches.append(mpatches.Patch(label='x > -2', facecolor='white', edgecolor='black'))

    # fig.tight_layout()
    legend = fig.legend(handles=patches, loc='lower center', prop={"size": 12}, title="scPDSI", frameon=True, ncol=4,
                        bbox_to_anchor=(0.5, 0.15))
    legend.get_frame().set_edgecolor('black')


    # cb2 = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
    #                                norm=norm,
    #                                boundaries=bounds,
    #                                extend='both',
    #                                ticks=bounds,
    #                                orientation='horizontal')
    # cb2.set_label('$\Delta$MCWD [mm/year]')
    # plt.show()
    #print(baseFileNames[j])
    plt.savefig(scenNames[j]+ ".jpg", dpi=600)


