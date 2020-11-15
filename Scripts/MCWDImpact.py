from Source.MCWDevaluation import MCWDFile
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


raisg_mask = r"../Data/AB-SHAPE/amazon_shape.shp"
mask = ShapelyFeature(Reader(raisg_mask).geometries(),
                                 ccrs.PlateCarree())


years =[2005, 2010, 2016]

MCWD = [ -200, -150, -100,-50,  -25, 0]
cmapMCWD = mpl.colors.ListedColormap([(165 / 255, 42 / 255, 42 / 255),
                                      (205/255, 149/255, 12/255),
                                      (255/255, 185/255, 15/255),
                                      (238/255, 232/255, 205/255),
                                  'white'])
cmapMCWD.set_over('white')
cmapMCWD.set_under((165 / 255, 42 / 255, 42 / 255))
normMCWD = mpl.colors.BoundaryNorm(MCWD, cmapMCWD.N)


MCWDrootPAth = r"../Data/MCWD/"
MCWDFiles = ["GPCC_AB_Yearly_05_MCWD.nc", "CHRIPS_AB_Monthly_05_mcwd.nc", "CRU_NCEP_V8_AB_Yearly_05_MCWD.nc",
               "ERAIN_AB_Monthly_05_mcwd.nc", "ERA5_AB_Yearly_05_MCWD.nc", "GLDAS_AB_Yearly_05_MCWD.nc", "TRMM_MCWD_1999_2018_SA05.nc" ]

baseFileNames = ["GPCC", "CHRIPS", "CRU_NCEP_V8", "ERAIN", "ERA5", "GLDAS", "TRMM"]


rowNames= ['a', 'b', 'c']


for j in range(0, len(baseFileNames)):

    fileMCWD = os.path.join(MCWDrootPAth, MCWDFiles[j])

    mcwdData = MCWDFile(fileMCWD)
    mcwdData.Parse(2001, 2016, years)


    fig = plt.figure(figsize=(14, 5))

    imgs = []

    for i in range(0, 3):
        imgMCWD = mcwdData.CreateImage(mcwdData.DataSlices[i])
        imgs.append(imgMCWD)

    index = 1
    for i in range(0, 3):

        img_extent = mcwdData.GeoFile.IMG_extent
        offset = [-3, 3, -3, 3]

        axGeo = fig.add_subplot(1, 3, index, projection=ccrs.PlateCarree())
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

        cmap = cmapMCWD
        norm = normMCWD

        imsh = axGeo.imshow(imgs[i], transform=ccrs.PlateCarree(), extent=img_extent, cmap=cmap, norm=norm)
        index += 1

    plt.subplots_adjust(bottom=0.25, wspace=0.3, right= 0.9)

    cax = plt.axes([0.91, 0.3,  0.02, 0.53])

    bar = plt.colorbar(imsh, cax=cax, orientation="vertical")
    bar.set_label('$\Delta$MCWD [mm]', fontsize=12)
    plt.savefig(r"../Output/"+ baseFileNames[j]+ ".jpg", dpi=600)