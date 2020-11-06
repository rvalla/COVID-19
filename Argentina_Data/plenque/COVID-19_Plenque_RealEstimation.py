from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import matplotlib.ticker as tk
import numpy as nu
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime as dt

print("################################################")
print("      Estimations of COVID-19 Outbreak")
print("------------------------------------------------")
print("https://github.com/rvalla/COVID-19")
print("Data loaded from Mauro Infantino site")
print("https://covidstats.com.ar")
print("------------------------------------------------")
print()
print("Loading data...", end="\n")

#Selecting regions to study in detail...
#Note that the first one will be used as reference to decide periods of time in some charts...
#regions = ["CABA", "BUENOS AIRES", "CHACO", "CORDOBA", "RIO NEGRO", "MENDOZA", "NEUQUEN", "ARGENTINA", "SANTA FE", "TIERRA DEL FUEGO", "ENTRE RIOS"]
regionslabels = ["CABA", "PBA", "COR", "SF", "Argentina"]
regionstoplot = [0, 1, 4]

#Selecting data to display
startDate = "2020-03-01" #Starting point for plotbyDate. Default: 03/03
endDate = "2020-09-15"
caseCount = 200 #Starting point for plotbyOutbreak (number of confirmed cases)
dataGuide = 0 #Data type to calculate startpoints (0 for confirmed, 2 for deaths)

realMortality = 0.01 #Real mortality to estimate infected count from deaths
deathOffset = 10 #Number of days needed to reach a death since symptoms onset on average

#Deciding language for titles and tags...
lg = 1 # 0 for english, 1 for spanish
ratioticks = 0.1
estimationticks = 500000
newratioticks = 0.2
newestimationticks = 10000

#Deciding if you want to save and show charts...
saveChart = True
showChart = False

#Deciding what to plot...
realCasesEstimation = False
testedRatio = False
ratioAndEstimation = True
ratioAndEstimation7dAv = True

#Deciding between linear or logarithmic scales...
plotScale = "linear"

#Variables to store filenames and other strings...
fileNameSuffix = ".csv"
fileNamePrefix = "Argentina_COVID19_Plenque_"
fileNames = ["CABA", "PBA", "COR", "SF", "Argentina"]
dataTitles = ["Estimation based on deaths", "Estimación a partir de fallecimientos", "Known cases ratio",
				"Tasa de detección", "Estimation based on deaths (7d)", "Estimación a partir de fallecimientos (7d)",
				"Known cases ratio (7d)", "Tasa de detección (7d)"]
plotTitles = ["Real cases estimation", "Estimación de casos"]
shortLabels = ["Estimated cases", "Casos estimados", "Confirmed", "Confirmados", "Deaths", "Fallecimientos",
				"Known ratio", "Tasa de detección"]
xTitles = ["Time in days", "Tiempo en días"]
yTitles = ["Estimated cases", "Casos estimados", "Confirmed", "Confirmados", "Deaths", "Fallecimientos",
				"Known ratio", "Tasa de detección"]
tConector = [" since ", " desde ", " after ", " después de ", " and ", " y ", "IFR = ", "IFR = ",
			"deaths offset = ", "corrimiento fallecimientos = "]

filePath = "plenque_data/"
chartPath = "plenque_estimations/"

#Some styling...
defaultFont = "Oswald" #Change this if you don't like it or is not available in your system
legendFont = "Myriad Pro" #Change this to edit legends' font
colorlist = ["chocolate", "tab:blue", "firebrick", "tab:green", "rebeccapurple", "olivedrab",
				"crimson", "darkcyan", "aqua", "dodgerblue", "palegreen", "seagreen", "limegreen", "indianred",
				"slategrey", "royalblue", "navy", "slateblue", "goldenrod", "greenyellow", "darkturquoise",
				"coral", "tab:pink"] #Default colors for data
backgroundPlot = "silver" #Default background color for charts
backgroundFigure = "white" #Default background color for figures
majorGridColor = "dimgrey" #Default colors for grids...
minorGridColor = "dimgray"
alphaMGC = 0.7
alphamGC = 0.9
imageResolution = 150

#Loading data...
databases = []
for d in range(len(fileNames)):
	databases.append(pd.read_csv(filePath + fileNamePrefix + fileNames[d] + fileNameSuffix))
	databases[d].set_index("FECHA", inplace = True)
	databases[d].index = pd.DatetimeIndex(databases[d].index)
	databases[d].index.name = "FECHA"

#Constant configurations...
startDateTime = dt.strptime(startDate, "%Y-%m-%d")
regionsIndexes = [[],[]]
quarantineStart = "2020-03-21"
startDateIndex = databases[0].index.get_loc(startDate) #Saving the startDate index for annotations
quarantineIndex = databases[0].index.get_loc(quarantineStart)
dateFormat = mdates.DateFormatter('%b %d')
dateFormatString = "%B %d"
if lg ==1:
	dateFormat = mdates.DateFormatter('%d/%m')
	dateFormatString = "%d/%m"

#Printing selected regions on console
print("Plotting data of " + str(regionslabels), end="\n")

#Method to draw a mark in social isolation start date
def markQuarantine(tag, yshift, ytshift, font, x, y, w, hw, hl):
	if startDate < quarantineStart and plotScale == "linear":
		plt.annotate(tag, fontsize=font, xy=(x, y + yshift),  xycoords='data',
    		xytext=(x, y + ytshift), textcoords='data',
			arrowprops=dict(facecolor='orangered', edgecolor="none", width=w, headwidth=hw, headlength=hl),
        	horizontalalignment='center', verticalalignment='top')

def savePlot(csvName, figure):
	chartName = csvName.split(".")
	plt.savefig(chartPath + str(lg) + "_" + chartName[0] + ".png", facecolor=figure.get_facecolor())

def gridAndTicks(yMax, ticksInterval):
	plt.grid(which='both', axis='both')
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.grid(True, "major", "x", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "x", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	if plotScale == "linear":
		plt.yticks(nu.arange(0, yMax, ticksInterval))
	plt.gca().set_facecolor(backgroundPlot)

def ticksLocator(weekInterval):
	plt.gca().xaxis.set_minor_locator(tk.AutoMinorLocator(7))
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=weekInterval))
	plt.gca().xaxis.set_major_formatter(dateFormat)
	plt.gca().xaxis.set_minor_formatter(tk.NullFormatter())

def plotRatioAndEstimation(regions, xtitle, ytitleA, ytitleB, markQ, ticksIntervalA, ticksIntervalB, savechart, show):
	figure = plt.figure(num=None, figsize=(4, 4), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	#figure.suptitle("COVID-19: " + plotTitles[0+lg] + "\n (" + tConector[6+lg] + str(realMortality) + ")", fontname=defaultFont, fontsize=12)
	plt.subplot2grid((2, 1), (0, 0))
	#Saving y values for markQ...
	yquarantine = []
	x = quarantineIndex
	#Plotting selected data...
	for i in range(len(regions)):
		plotA = databases[regions[i]][startDate:endDate]["ratio"].plot(kind='line', label=regionslabels[regions[i]], \
				color=colorlist[i], alpha = 1.0, linewidth=2.0)
	s = plt.ylim()
	a = plt.xlim()
	#Setting up titles
	plotA.set_title(dataTitles[2+lg], fontname=defaultFont, fontsize=10)
	plt.yscale(plotScale)
#	plt.ylabel(ytitleA, fontname=legendFont, fontsize=8)
	plt.ylabel("")
	plt.xlabel("")
	plt.legend(loc=4, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 6})
	#Setting up grid...
	gridAndTicks(s[1]*1.1, ticksIntervalA)
	ticksLocator(3)
	plt.gca().xaxis.set_ticklabels([])
	#Setting axis labels font and legend
	plt.subplot2grid((2, 1), (1, 0))
	#Saving y values for markQ...
	yquarantine = []
	x = quarantineIndex
	#Plotting selected data...
	for i in range(len(regions)):
		plotB = databases[regions[i]][startDate:endDate]["estimation"].plot(kind='line', label=regionslabels[regions[i]], \
				color=colorlist[i], alpha = 1.0, linewidth=2.0, zorder=2)
		plotB = databases[regions[i]][startDate:endDate]["confirmed"].plot(kind='line', label=regionslabels[regions[i]], \
				color=colorlist[i], alpha = 0.5, linewidth=2.0, zorder=1)
		yquarantine.append(databases[regions[i]].loc[quarantineStart, "estimation"])
	s = plt.ylim()
	plt.xlim(a[0], a[1])
	if markQ == True:
		y = max(yquarantine) #Drawing a mark on quarantineStartDate
		markQuarantine("", s[1]/20, s[1]/5, 8, quarantineStart, y, 5, 9, 7)
	#Setting up titles
	plotB.set_title(dataTitles[0+lg] +"\n (" + tConector[8+lg] + str(deathOffset) + ", " +
			tConector[6+lg] + str(realMortality) + ")", fontname=defaultFont, fontsize=10)
	plt.yscale(plotScale)
#	plt.ylabel(ytitleB, fontname=legendFont, fontsize=8)
	plt.ylabel("")
	plt.xlabel(xtitle, fontname=legendFont, fontsize=8)
	#Setting up grid...
	gridAndTicks(s[1]*1.1, ticksIntervalB)
	ticksLocator(3)
	ylabels = nu.arange(0, s[1]/1000000*1.1, ticksIntervalB/1000000).tolist()
	for l in range(len(ylabels)):
		ylabels[l] = "{:.1f}".format(ylabels[l])
		ylabels[l] += "M"
	plt.yticks(nu.arange(0, s[1] * 1.1, ticksIntervalB), ylabels)
	plt.tight_layout(rect=[0, 0, 1, 1])
	if savechart == True:
		auxName = fileNames[0].split(".")
		savePlot("E_00_Plenque_KnownRatioAndEstimation.csv", figure)
	if show == True:
		plt.show()

def plotRatioAndEstimation7dAv(regions, xtitle, ytitleA, ytitleB, markQ, ticksIntervalA, ticksIntervalB, savechart, show):
	figure = plt.figure(num=None, figsize=(4, 4), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	#figure.suptitle("COVID-19: " + plotTitles[0+lg] + "\n (" + tConector[6+lg] + str(realMortality) + ")", fontname=defaultFont, fontsize=12)
	plt.subplot2grid((2, 1), (0, 0))
	#Saving y values for markQ...
	yquarantine = []
	x = quarantineIndex
	#Plotting selected data...
	for i in range(len(regions)):
		plotA = databases[regions[i]][startDate:endDate]["new ratio (7d)"].plot(kind='line', label=regionslabels[regions[i]], \
				color=colorlist[i], alpha = 1.0, linewidth=2.0)
	s = plt.ylim()
	a = plt.xlim()
	#Setting up titles
	plotA.set_title(dataTitles[6+lg], fontname=defaultFont, fontsize=10)
	plt.yscale(plotScale)
#	plt.ylabel(ytitleA, fontname=legendFont, fontsize=8)
	plt.ylabel("")
	plt.xlabel("")
	plt.legend(loc=1, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 6})
	#Setting up grid...
	gridAndTicks(s[1]*1.1, ticksIntervalA)
	ticksLocator(3)
	plt.gca().xaxis.set_ticklabels([])
	#Setting axis labels font and legend
	plt.subplot2grid((2, 1), (1, 0))
	#Saving y values for markQ...
	yquarantine = []
	x = quarantineIndex
	#Plotting selected data...
	for i in range(len(regions)):
		plotB = databases[regions[i]][startDate:endDate]["new estimated (7d)"].plot(kind='line', label=regionslabels[regions[i]], \
				color=colorlist[i], alpha = 1.0, linewidth=2.0, zorder=2)
		plotB = databases[regions[i]][startDate:endDate]["new confirmed (7d)"].plot(kind='line', label=regionslabels[regions[i]], \
				color=colorlist[i], alpha = 0.5, linewidth=2.0, zorder=1)
		yquarantine.append(databases[i].loc[quarantineStart, "estimation"])
	s = plt.ylim()
	plt.xlim(a[0], a[1])
	if markQ == True:
		y = max(yquarantine) #Drawing a mark on quarantineStartDate
		markQuarantine("", s[1]/20, s[1]/5, 8, quarantineStart, y, 5, 9, 7)
	#Setting up titles
	plotB.set_title(dataTitles[4+lg] +"\n (" + tConector[8+lg] + str(deathOffset) + ", " +
			tConector[6+lg] + str(realMortality) + ")", fontname=defaultFont, fontsize=10)
	plt.yscale(plotScale)
#	plt.ylabel(ytitleB, fontname=legendFont, fontsize=8)
	plt.ylabel("")
	plt.xlabel(xtitle, fontname=legendFont, fontsize=8)
	#Setting up grid...
	gridAndTicks(s[1]*1.1, ticksIntervalB)
	ticksLocator(3)
	ylabels = nu.arange(0, s[1]/1000*1.1, ticksIntervalB/1000).tolist()
	for l in range(len(ylabels)):
		ylabels[l] = "{:.0f}".format(ylabels[l])
		ylabels[l] += "K"
	plt.yticks(nu.arange(0, s[1] * 1.1, ticksIntervalB), ylabels)
	plt.tight_layout(rect=[0, 0, 1, 1])
	if savechart == True:
		auxName = fileNames[0].split(".")
		savePlot("E_00_Plenque_KnownRatioAndEstimation7dAv.csv", figure)
	if show == True:
		plt.show()

if ratioAndEstimation == True:
	plotRatioAndEstimation(regionstoplot, xTitles[0+lg], yTitles[6+lg], yTitles[0+lg], True, ratioticks, estimationticks, saveChart, showChart)

if ratioAndEstimation7dAv == True:
	plotRatioAndEstimation7dAv(regionstoplot, xTitles[0+lg], yTitles[6+lg], yTitles[0+lg], True, newratioticks, newestimationticks, saveChart, showChart)

#Saying good bye...
print("That's all. If you want more plots, edit the code and run again.                          ", end="\n")
