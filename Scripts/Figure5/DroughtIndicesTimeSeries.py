
from A02_MCWD_Dataset_Analysis.Setup2016 import Setup2016
from A02_MCWD_Dataset_Analysis.Pylibs.MCWD_Analysis21 import MCWDFile
from A02_MCWD_Dataset_Analysis.Pylibs.PrecAnomalyDry21 import PrecAnomaly
from A02_MCWD_Dataset_Analysis.Pylibs.scPDSI2021 import scPDSI

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
#import matplotlib.pylab as plt



colors = [
    '#2e8b57',
    '#ff0000',
    '#ffd700',
    '#c71585',
    '#00ff00',
    '#0000ff',
    '#1e90ff',
    ]


#files = [
#["CHR", "CHRIPS_AB_Monthly_05_mcwd.nc", "CHRIPS_AB_monthly_05-scPDSI-2016.txt", "CHRIPS_AB_monthly_05.nc"],
#["CRU", "CRU_NCEP_V8_AB_Yearly_05_MCWD.nc", "CRU_NCEP_V8_AB_Monthly_05-scPDSI-2016.txt", "CRU_NCEP_V8_AB_Monthly_05.nc"]]

CWDFiles = []
scPDSIFiles = []
precFiels = []

qs = [0.5]

import string
lowerletters = string.ascii_lowercase[0:26]

setup = Setup2016()

for file in setup.cwd_files:
    CWDFiles.append(MCWDFile(setup.CWDrootPAth + "\\" + file[1]))
for file in setup.files:
    scPDSIFiles.append(scPDSI(setup.scPDSIrootPAth + "\\" + file[2]))
    precFiels.append(PrecAnomaly(setup.PRECrootPAth + "\\" + file[3]))




qs = [0.25]
q = 0.10
cwdDataRaw = np.zeros((len(precFiels), len(qs), 4, 12))
i = 0
for CWDFile in CWDFiles:
    data = CWDFile.ParseRelativeMonthly(2001, 2016)

    data = np.nanquantile(data, q = q, axis = 0)
    cwdDataRaw[i, 0, 0,:] = data[(2005-2001)*12:(2005-2001)*12+12]
    cwdDataRaw[i, 0, 1,:] = data[(2010-2001)*12:(2010-2001)*12+12]
    cwdDataRaw[i, 0, 2,:] = data[(2015-2001)*12:(2015-2001)*12+12]
    cwdDataRaw[i, 0, 3,:] = data[(2016-2001)*12:(2016-2001)*12+12]
    i+=1

i = 0

scpdsiDataRaw = np.zeros((len(precFiels), len(qs), 4, 12))
for scPDSIFileMonthly in scPDSIFiles:
    data = scPDSIFileMonthly.ParseRelativeMonthly(2000, 2016)
    data = np.nanquantile(data, q = q, axis = 0)
    scpdsiDataRaw[i, 0, 0,:] = data[(2005-2000)*12:(2005-2000)*12+12]
    scpdsiDataRaw[i, 0, 1,:] = data[(2010-2000)*12:(2010-2000)*12+12]
    scpdsiDataRaw[i, 0, 2,:] = data[(2015-2000)*12:(2015-2000)*12+12]
    scpdsiDataRaw[i, 0, 3,:] = data[(2016-2000)*12:(2016-2000)*12+12]
    i+=1

precDataRaw = np.zeros((len(precFiels), len(qs), 4, 12))
i = 0
for precfile in precFiels:
    data = precfile.ParseRelativeMonthly(2001, 2016)
    data = np.nanquantile(data, q = q, axis = 0)
    precDataRaw[i, 0, 0,:] = data[(2005-2001)*12:(2005-2001)*12+12]
    precDataRaw[i, 0, 1,:] = data[(2010-2001)*12:(2010-2001)*12+12]
    precDataRaw[i, 0, 2,:] = data[(2015-2001)*12:(2015-2001)*12+12]
    precDataRaw[i, 0, 3,:] = data[(2016-2001)*12:(2016-2001)*12+12]
    i+=1


ylim = (-3,0.5)

mLabs = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]

lwd = 1.0

fig= plt.figure(figsize=(12,8))
gs = fig.add_gridspec(ncols=3, nrows=3, width_ratios = [1,1,2])

ax1= fig.add_subplot(gs[0, 0])
for i in range(0, len(qs)):
    ax1.plot(range(0,12), np.zeros((12)), c = 'tab:gray', linestyle = 'dashed')
    ax1.set_ylim(ylim)
    for d in range(0, len(precFiels)):
        ax1.plot(range(0, 12), precDataRaw[d, i, 0], c = colors[d], linewidth=lwd)
    #ax1.plot(range(0,12), precDataRawMean[i, 0], c = 'black', linestyle = 'dashed')
ax1.set_xticks(range(0,12))
ax1.set_xticklabels(mLabs)
ax1.text(0.04, 0.90, lowerletters[0] + ")", horizontalalignment='left',
           verticalalignment='center',
           transform=ax1.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))


ax2= fig.add_subplot(gs[0, 1])
for i in range(0, len(qs)):
    ax2.plot(range(0,12), np.zeros((12)), c = 'tab:gray', linestyle = 'dashed')
    ax2.set_ylim(ylim)
    for d in range(0, len(precFiels)):
        ax2.plot(range(0, 12), precDataRaw[d, i, 1], c = colors[d], linewidth=lwd)
    #ax2.plot(range(0,12), precDataRawMean[i, 1], c = 'black', linestyle = 'dashed')
ax2.set_xticks(range(0,12))
ax2.set_xticklabels(mLabs)
ax2.text(0.04, 0.90, lowerletters[1] + ")", horizontalalignment='left',
           verticalalignment='center',
           transform=ax2.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))


#v = np.concatenate(precFiels[0].DataSlices[:,2], precFiels[0].DataSlices[:,3])
ax3 = fig.add_subplot(gs[0, 2])
for i in range(0, len(qs)):
    ax3.plot(range(0,24), np.zeros((24)), c = 'tab:gray', linestyle = 'dashed')
    for d in range(0, len(precFiels)):
        ax3.plot(range(0, 24), np.concatenate((precDataRaw[d, i, 2], precDataRaw[d, i, 3])), c = colors[d], linewidth=lwd)
    #ax3.plot(range(0,24), np.concatenate((precDataRawMean[i, 2], precDataRawMean[i, 3])), c = 'black', linestyle = 'dashed')
    ax3.set_ylim(ylim)
ax3.plot([11,11], ylim, c = 'tab:gray')
ax3.set_xticks(range(0,24))
ax3.set_xticklabels(np.concatenate((mLabs, mLabs)))
ax3.text(0.04, 0.90, lowerletters[2] + ")", horizontalalignment='left',
           verticalalignment='center',
           transform=ax3.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))



ax1= fig.add_subplot(gs[1, 0])
for i in range(0, len(qs)):
    ax1.plot(range(0,12), np.zeros((12)), c = 'tab:gray', linestyle = 'dashed')
    ax1.set_ylim(ylim)
    for d in range(0, len(precFiels)):
        ax1.plot(range(0, 12), cwdDataRaw[d, i, 0], c = colors[d], linewidth=lwd)
    #ax1.plot(range(0,12), cwdDataRawMean[i, 0], c = 'black', linestyle = 'dashed')
ax1.set_xticks(range(0,12))
ax1.set_xticklabels(mLabs)
ax1.text(0.04, 0.90, lowerletters[3] + ")", horizontalalignment='left',
           verticalalignment='center',
           transform=ax1.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))


ax2= fig.add_subplot(gs[1, 1])
for i in range(0, len(qs)):
    ax2.plot(range(0,12), np.zeros((12)), c = 'tab:gray', linestyle = 'dashed')
    ax2.set_ylim(ylim)
    for d in range(0, len(precFiels)):
        ax2.plot(range(0, 12), cwdDataRaw[d, i, 1], c = colors[d], linewidth=lwd)
    #ax2.plot(range(0,12), cwdDataRawMean[i, 1], c = 'black', linestyle = 'dashed')
ax2.set_xticks(range(0,12))
ax2.set_xticklabels(mLabs)
ax2.text(0.04, 0.90, lowerletters[4] + ")", horizontalalignment='left',
           verticalalignment='center',
           transform=ax2.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))


#v = np.concatenate(precFiels[0].DataSlices[:,2], precFiels[0].DataSlices[:,3])
ax3 = fig.add_subplot(gs[1, 2])
for i in range(0, len(qs)):
    ax3.plot(range(0,24), np.zeros((24)), c = 'tab:gray', linestyle = 'dashed')
    for d in range(0, len(precFiels)):
        ax3.plot(range(0, 24), np.concatenate((cwdDataRaw[d, i, 2], cwdDataRaw[d, i, 3])), c = colors[d], linewidth=lwd)
    #ax3.plot(range(0,24), np.concatenate((cwdDataRawMean[i, 2], cwdDataRawMean[i, 3])), c = 'black', linestyle = 'dashed')
    ax3.set_ylim(ylim)
ax3.plot([11,11], ylim, c = 'tab:gray')
ax3.set_xticks(range(0,24))
ax3.set_xticklabels(np.concatenate((mLabs, mLabs)))
ax3.text(0.04, 0.90, lowerletters[5] + ")", horizontalalignment='left',
           verticalalignment='center',
           transform=ax3.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))


ax1= fig.add_subplot(gs[2, 0])
for i in range(0, len(qs)):
    ax1.plot(range(0,12), np.zeros((12)), c = 'tab:gray', linestyle = 'dashed')
    ax1.set_ylim(ylim)
    for d in range(0, len(precFiels)):
        ax1.plot(range(0, 12), scpdsiDataRaw[d, i, 0], c = colors[d], linewidth=lwd)
    #ax1.plot(range(0,12), scpdsiDataRawMean[i, 0], c = 'black', linestyle = 'dashed')
ax1.set_xticks(range(0,12))
ax1.set_xticklabels(mLabs)
ax1.text(0.04, 0.90, lowerletters[6] + ")", horizontalalignment='left',
           verticalalignment='center',
           transform=ax1.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))


ax2= fig.add_subplot(gs[2, 1])

for i in range(0, len(qs)):
    ax2.plot(range(0,12), np.zeros((12)), c = 'tab:gray', linestyle = 'dashed')
    ax2.set_ylim(ylim)
    for d in range(0, len(precFiels)):
        ax2.plot(range(0, 12), scpdsiDataRaw[d, i, 1], c = colors[d], linewidth=lwd)
    #ax2.plot(range(0,12), scpdsiDataRawMean[i, 1], c = 'black', linestyle = 'dashed')
ax2.set_xticks(range(0,12))
ax2.set_xticklabels(mLabs)
ax2.text(0.04, 0.90, lowerletters[7] + ")", horizontalalignment='left',
           verticalalignment='center',
           transform=ax2.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))

#v = np.concatenate(precFiels[0].DataSlices[:,2], precFiels[0].DataSlices[:,3])
ax3 = fig.add_subplot(gs[2, 2])
for i in range(0, len(qs)):
    ax3.plot(range(0,24), np.zeros((24)), c = 'tab:gray', linestyle = 'dashed')
    for d in range(0, len(precFiels)):
        ax3.plot(range(0, 24), np.concatenate((scpdsiDataRaw[d, i, 2], scpdsiDataRaw[d, i, 3])), c = colors[d], linewidth=lwd)
    #ax3.plot(range(0,24), np.concatenate((scpdsiDataRawMean[i, 2], scpdsiDataRawMean[i, 3])), c = 'black', linestyle = 'dashed')
    ax3.set_ylim(ylim)
ax3.plot([11,11], ylim, c = 'tab:gray')
ax3.set_xticks(range(0,24))
ax3.set_xticklabels(np.concatenate((mLabs, mLabs)))
ax3.text(0.04, 0.90, lowerletters[8] + ")", horizontalalignment='left',
           verticalalignment='center',
           transform=ax3.transAxes, size=14, bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))

plt.subplots_adjust(bottom=  0.15, top = 0.8, left = 0.15)
fig.text(0.1, 0.7, '$r\mathrm{RAI}$', ha='center', va='center', rotation='vertical', fontsize=12)
fig.text(0.1, 0.47, '$r\mathrm{CWD}$', ha='center', va='center', rotation='vertical', fontsize=12)
fig.text(0.1, 0.25, '$r\mathrm{scPDSI}$', ha='center', va='center', rotation='vertical', fontsize=12)

fig.text(0.23, 0.82, '2005', ha='center', va='center', fontsize=12, fontweight='bold')
fig.text(0.44, 0.82, '2010', ha='center', va='center', fontsize=12, fontweight='bold')
fig.text(0.64, 0.82,  '2015', ha='center', va='center', fontsize=12, fontweight='bold')
fig.text(0.81, 0.82,  '2016', ha='center', va='center', fontsize=12, fontweight='bold')

#fig.tight_layout(pad = 3)
from matplotlib.lines import Line2D
lines = [Line2D([0], [0], color=c, linewidth=3) for c in colors]

#lines.append(Line2D([0],[0], color = 'black')


#plt.subplots_adjust(bottom=  0.2)


fig.legend(handles = lines ,
           labels= [f[0] for f in setup.files],
           loc='lower center',
            markerscale=5,
            bbox_to_anchor=(0.5,0.03),
            fontsize=12,
           ncol=8,
           fancybox=False, shadow=False)

plt.savefig("Figure5.png", dpi = 600, bbox_inches = 'tight',
    pad_inches = 0.3)
