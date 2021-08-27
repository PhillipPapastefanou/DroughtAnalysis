from A02_MCWD_Dataset_Analysis.Pylibs.MCWD_Analysis21 import MCWDFile
from A02_MCWD_Dataset_Analysis.Setup2010 import Setup2010
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
#import matplotlib.pylab as plt

import matplotlib as mpl

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

raisg_mask = r"F:\Dropbox\ClimateData\AmazonBasin\AB-SHAPE\amazon_shape.shp"
mask = ShapelyFeature(Reader(raisg_mask).geometries(),
                                 ccrs.PlateCarree())



bounds = np.arange(1,10)
#cmap = plt.get_cmap('coolwarm', 7)
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("",

                                                        ['#ffffd9' ,
                                                            '#edf8b1',
'#c7e9b4',
'#7fcdbb',
'#41b6c4',
'#1d91c0',
'#225ea8',
'#0c2c84'
                                                            ], 7)


cmap = matplotlib.colors.LinearSegmentedColormap.from_list("",

                                                        ['#B0B8B4FF',
                                                         '#FC766AFF',
                                                         '#184A45FF'
                                                            ], 8)


cmap = matplotlib.colors.LinearSegmentedColormap.from_list("",

                                                        ['#F2A104',
                                                         '#00743F',
                                                         '#72A2C0',
'#1D65A6',
'#192E5B'
                                                            ], 8)


#cmap.set_over('white')
cmap.set_under('white')
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

setup = Setup2010()


MCWDFiles = []
data2005 = np.zeros((len(setup.files), 1946))
data2010 = np.zeros((len(setup.files), 1946))


for file in setup.files:
    MCWDFiles.append(MCWDFile(setup.MCWDrootPAth + "\\" + file[1]))

i = 0
for MCWDFile in MCWDFiles:
    data = MCWDFile.ParseRelativeDeviation(2000, 2010)
    data2005[i] = data[2005-2000]
    data2010[i] = data[2010-2000]
    i += 1




dataCount = np.zeros((6, 1946))
#dataCount[0] = ((-100 < dataSlice) & (dataSlice < -25)).sum(axis = 0)
#dataCount[1]  = ((-150 < dataSlice) & (dataSlice  < -100)).sum(axis = 0)
#dataCount[2]  = (dataSlice < -150).sum(axis = 0)

dataSlice = data2005
dataCount[0] = (dataSlice < -0.5).sum(axis = 0)
dataCount[1]  = (dataSlice < -2.0).sum(axis = 0)
dataCount[2]  = (dataSlice < -2.5).sum(axis = 0)

dataSlice = data2010
dataCount[3] = (dataSlice < -0.5).sum(axis = 0)
dataCount[4]  = (dataSlice < -2.0).sum(axis = 0)
dataCount[5]  = (dataSlice < -2.5).sum(axis = 0)

fig = plt.figure(figsize=(11.5,7))

import string
lowerletters = string.ascii_lowercase[:26]

index = 1


for countFile in range(0, dataCount.shape[0]):

    img = MCWDFiles[0].CreateImage(dataCount[index - 1])

    img_extent = MCWDFiles[0].GeoFile.IMG_extent
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
    axGeo.text(-81, 5, r'$'+ lowerletters[index - 1] +'$)',
               fontsize=16, horizontalalignment='left', verticalalignment='center',
               bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    # titleTxt = axGeo.set_title(vulnerabilites[i], size=16)
    # titleTxt.set_path_effects([PathEffects.withStroke(linewidth=1, foreground='black')])
    # axGeo.text(0.02, 0.93, textborder[i - 1], horizontalalignment='left', verticalalignment='center',
    #           transform=axGeo.transAxes, size=14)

    axGeo.set_xticks([-80, -70, -60, -50], crs=ccrs.PlateCarree())
    axGeo.set_yticks([-20, -15, -10, -5, 0, 5], crs=ccrs.PlateCarree())



    axGeo.set_xlabel(r'Longitude')
    if (index == 1)|(index == 4):
        axGeo.set_ylabel(r'Latitude')


    imsh = axGeo.imshow(img, transform=ccrs.PlateCarree(), extent=img_extent, cmap=cmap, norm=norm)
    index+=1



fig.text(0.08, 0.75, '2005', ha='center', va='center', rotation='vertical', fontsize=16, fontweight='bold')
fig.text(0.08, 0.4, '2010', ha='center', va='center', rotation='vertical', fontsize=16, fontweight='bold')
fig.text(0.27, 0.93, 'Moderate\n $r\mathrm{MCWD} < -0.5$', ha='center', va='center', fontsize=12, fontweight='bold')
fig.text(0.52, 0.93, 'Severe\n $r\mathrm{MCWD} < -2.0$', ha='center', va='center', fontsize=12, fontweight='bold')
fig.text(0.8, 0.93, 'Extreme\n $r\mathrm{MCWD}< -2.5$', ha='center', va='center', fontsize=12, fontweight='bold')

#fig.tight_layout(pad = 3)
#cax = plt.axes([0.157, 0.9, 0.735, 0.035])
cax = plt.axes([0.157, 0.1, 0.735, 0.035])
#bar = plt.colorbar(imsh, cax=cax, orientation="horizontal")
#cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
#                                norm=norm,
#                                orientation='horizontal', boundaries= bounds, ticks = bounds, format='%1i')
cb2 = mpl.colorbar.ColorbarBase(cax,
                                cmap=cmap,
                                norm=norm,
                                boundaries=np.arange(0,9) + 0.5,
                                ticks=np.arange(1,9),
                                orientation='horizontal')
cb2.set_label('Datasets in agreement', fontsize=16)
#cb2.ax.xaxis.set_ticks_position('top')
cb2.ax.xaxis.set_label_position('top')
cb2.ax.set_xticklabels(['1 (None)', '2', '3', '4', '5', '6', '7', '8 (All)'])

plt.subplots_adjust(top = 0.9, bottom = 0.25, wspace=0.15, left = 0.15)

#bar = plt.colorbar.ColorbarBase(cax = cax, cmap=cmap, norm=norm, spacing='proportional', format='%1i')
plt.savefig("Drought-MCWD-Agreement-05-10-lessDatasets.png",  dpi=600, bbox_inches = 'tight',
    pad_inches = 0.0)
#plt.show()