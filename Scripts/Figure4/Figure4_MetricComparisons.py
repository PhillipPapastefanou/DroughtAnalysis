
from A02_MCWD_Dataset_Analysis.Setup2016 import Setup2016
from A02_MCWD_Dataset_Analysis.Pylibs.MCWD_Analysis21 import MCWDFile
from A02_MCWD_Dataset_Analysis.Pylibs.PrecAnomalyDry21 import PrecAnomaly
from A02_MCWD_Dataset_Analysis.Pylibs.scPDSI2021 import scPDSI
import pandas

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

rawData = pandas.read_csv(r"F:\Dropbox\ClimateData\Coords\SA_Amazon_basin\Amazon_basin_05_area.txt",
                     sep = ',',
                     header=0).values
areasRelative = rawData[:,4]
areasAbs = rawData[:,3]


raisg_mask = r"F:\Dropbox\ClimateData\AmazonBasin\AB-SHAPE\amazon_shape.shp"
mask = ShapelyFeature(Reader(raisg_mask).geometries(),
                                 ccrs.PlateCarree())


bounds = np.arange(1,9)
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
                                                            ], 8)


cmap = matplotlib.colors.LinearSegmentedColormap.from_list("",

                                                        ['#B0B8B4FF',
                                                         '#FC766AFF',
                                                         '#184A45FF'
                                                            ], 7)


cmap = matplotlib.colors.LinearSegmentedColormap.from_list("",

                                                        ['#F2A104',
                                                         '#00743F',
                                                         '#72A2C0',
'#1D65A6',
'#192E5B'
                                                            ], 7)


#cmap.set_over('white')
cmap.set_under('white')
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


setup = Setup2016()

files = setup.files



#files = [
#["CHR", "CHRIPS_AB_Monthly_05_mcwd.nc", "CHRIPS_AB_monthly_05-scPDSI-2016.txt", "CHRIPS_AB_monthly_05.nc"],
#["CRU", "CRU_NCEP_V8_AB_Yearly_05_MCWD.nc", "CRU_NCEP_V8_AB_Monthly_05-scPDSI-2016.txt", "CRU_NCEP_V8_AB_Monthly_05.nc"]]

MCWDFiles = []
scPDSIFiles = []
precFiels = []

data2005 = np.zeros((len(files), 3, 1946))
data2010 = np.zeros((len(files), 3, 1946))
data2016 = np.zeros((len(files), 3 , 1946))


for file in files:
    MCWDFiles.append(MCWDFile(setup.MCWDrootPAth + "\\" + file[1]))
    scPDSIFiles.append(scPDSI(setup.scPDSIrootPAth + "\\" + file[2]))
    precFiels.append(PrecAnomaly(setup.PRECrootPAth + "\\" + file[3]))

i = 0
for MCWDFile in MCWDFiles:
    data = MCWDFile.ParseRelativeDeviation(2001, 2016)
    data2005[i, 0] = data[2005 - 2001]
    data2010[i, 0] = data[2010 - 2001]
    data2016[i, 0] = data[2016 - 2001]
    i+=1

i = 0
for scPDSIFile in scPDSIFiles:
    data = scPDSIFile.ParseRelativeDeviation(2000, 2016)
    data2005[i, 1] = data[2005 - 2000]
    data2010[i, 1] = data[2010 - 2000]
    data2016[i, 1] = data[2016 - 2000]
    i+=1

i = 0
for precFile in precFiels:
    data = precFile.ParseRelativeDeviation(2001, 2016)
    data2005[i, 2] = data[2005 - 2001]
    data2010[i, 2] = data[2010 - 2001]
    data2016[i, 2] = data[2016 - 2001]
    i+=1


dataCount = np.zeros((9, 1946))
#dataCount[0] = ((-100 < dataSlice) & (dataSlice < -25)).sum(axis = 0)
#dataCount[1]  = ((-150 < dataSlice) & (dataSlice  < -100)).sum(axis = 0)
#dataCount[2]  = (dataSlice < -150).sum(axis = 0)

l = -0.5

dataCount[0]  = (data2005[:,2,:] < l).sum(axis = 0)
dataCount[1]  = (data2010[:,2,:] < l).sum(axis = 0)
dataCount[2]  = (data2016[:,2,:] < l).sum(axis = 0)

dataCount[3]  = (data2005[:,0,:] < l).sum(axis = 0)
dataCount[4]  = (data2010[:,0,:] < l).sum(axis = 0)
dataCount[5]  = (data2016[:,0,:] < l).sum(axis = 0)

dataCount[6]  = (data2005[:,1,:] < l).sum(axis = 0)
dataCount[7]  = (data2010[:,1,:] < l).sum(axis = 0)
dataCount[8]  = (data2016[:,1,:] < l).sum(axis = 0)


fig = plt.figure(figsize=(9,7))

index = 1
import string
lowerletters = string.ascii_lowercase[0:26]

df  = pandas.DataFrame()
acc = np.zeros((len(files), 6))


for countFile in range(0, dataCount.shape[0]):
    img = MCWDFiles[0].CreateImage(dataCount[index - 1])
    img_extent = MCWDFiles[0].GeoFile.IMG_extent
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
    axGeo.text(-80.8, 4.7, lowerletters[index-1] +')',
               fontsize=12, horizontalalignment='left', verticalalignment='center',
               bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    # titleTxt = axGeo.set_title(vulnerabilites[i], size=16)
    # titleTxt.set_path_effects([PathEffects.withStroke(linewidth=1, foreground='black')])
    # axGeo.text(0.02, 0.93, textborder[i - 1], horizontalalignment='left', verticalalignment='center',
    #           transform=axGeo.transAxes, size=14)

    axGeo.set_xticks([-80, -70, -60, -50], crs=ccrs.PlateCarree())
    axGeo.set_yticks([-20, -15, -10, -5, 0, 5], crs=ccrs.PlateCarree())



    axGeo.set_xlabel(r'Longitude')

    if index % 3 == 1:
        axGeo.set_ylabel(r'Latitude' )


    imsh = axGeo.imshow(img, transform=ccrs.PlateCarree(), extent=img_extent, cmap=cmap, norm=norm)
    index+=1

df  = pandas.DataFrame()
acc = np.zeros((len(files), 9))

metricPlain = ""



l = -2.5

dataCountIndv = np.zeros((9, 6))

dataCountIndv[0]  = (data2005[:,2,:] < l).sum(axis = 1)
dataCountIndv[1]  = (data2010[:,2,:] < l).sum(axis = 1)
dataCountIndv[2]  = (data2016[:,2,:] < l).sum(axis = 1)

dataCountIndv[3]  = (data2005[:,0,:] < l).sum(axis =1)
dataCountIndv[4]  = (data2010[:,0,:] < l).sum(axis = 1)
dataCountIndv[5]  = (data2016[:,0,:] < l).sum(axis = 1)

dataCountIndv[6]  = (data2005[:,1,:] < l).sum(axis = 1)
dataCountIndv[7]  = (data2010[:,1,:] < l).sum(axis = 1)
dataCountIndv[8]  = (data2016[:,1,:] < l).sum(axis = 1)



for d in range(0, 9):
    for j in range(0, len(files)):
        if d < 3:
            metric = "$r\mathrm{RAI}"
            metricPlain = "rRAI"
        elif d < 6:
            metric = "$r\mathrm{MCWD}"
            metricPlain = "rMCWD"
        else:
            metric = "$r\mathrm{scPDSI}"
            metricPlain = "rscPDSI"

        if d % 3 == 0:
            year = 2005
        elif d % 3 == 1:
            year = 2010
        else:
            year = 2016

        subdf = pandas.DataFrame({"metric": metricPlain,
                                  "Year": year,
                                  'Dataset': files[j][0],
                                  'Condition': d % 3,
                                  'TotalArea': dataCountIndv[d, j] / 1946.0 * 5.94*10**6 ,
                                  'RelativeArea': dataCountIndv[d, j] / 1946.0
                                  }, index=[0])
        df = df.append(subdf)


df.to_csv(r'AgreementMetricExtreme.tsv', sep= '\t', header = True)




plt.subplots_adjust(bottom=  0.15, top = 0.8, left = 0.18)
fig.text(0.16, 0.31, '$r\mathrm{scPDSI}$', ha='center', va='center', rotation='vertical', fontsize=12)
fig.text(0.16, 0.51, "$r\mathrm{MCWD}$", ha='center', va='center', rotation='vertical', fontsize=12)
fig.text(0.16, 0.71, "$r\mathrm{RAI}$", ha='center', va='center', rotation='vertical', fontsize=12)



fig.text(0.3, 0.82, '2005', ha='center', va='center', fontsize=12, fontweight='bold')
fig.text(0.54, 0.82, '2010', ha='center', va='center', fontsize=12, fontweight='bold')
fig.text(0.77, 0.82,  '2016', ha='center', va='center', fontsize=12, fontweight='bold')

#fig.tight_layout(pad = 3)
cax = plt.axes([0.225, 0.1, 0.63, 0.03])
#bar = plt.colorbar(imsh, cax=cax, orientation="horizontal")
#cb1 = mpl.colorbar.ColorbarBase(cax, cmap=cmap,
#                                norm=norm,
#                                orientation='horizontal', boundaries= bounds, ticks = bounds, format='%1i')
cb2 = mpl.colorbar.ColorbarBase(cax,
                                cmap=cmap,
                                norm=norm,
                                boundaries=np.arange(0,8) + 0.5,
                                ticks=np.arange(1,8),
                                orientation='horizontal')
cb2.set_label('Datasets in agreement', fontsize=16)
#cb2.ax.xaxis.set_ticks_position('top')
cb2.ax.xaxis.set_label_position('top')
cb2.ax.set_xticklabels(['1 (None)', '2', '3', '4', '5', '6', '7 (All)'])

plt.subplots_adjust(bottom = 0.23 , wspace= -0.2)

#bar = plt.colorbar.ColorbarBase(cax = cax, cmap=cmap, norm=norm, spacing='proportional', format='%1i')
plt.savefig("Drought metric comparison.png",  dpi=600, bbox_inches = 'tight',
    pad_inches = 0.3)
