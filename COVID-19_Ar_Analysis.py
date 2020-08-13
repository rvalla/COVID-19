from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import matplotlib.ticker as tk
import numpy as nu
import pandas as pd
import matplotlib.dates as mdates
from datetime import datetime as dt

print("####################################################")
print("       Visualization of COVID-19 Outbreak")
print("----------------------------------------------------")
print("https://github.com/rvalla/COVID-19")
print("Data loaded from official national reports")
print("https://argentina.gob.ar/coronavirus/informe-diario")
print("----------------------------------------------------")
print()
print("Loading data...", end="\n")

#Selecting regions to study in detail...
#Note that the first one will be used as reference to decide periods of time in some charts...
regions = ["CABA", "BUENOS AIRES", "CORDOBA", "CHACO", "JUJUY", "MENDOZA", "NEUQUEN", "RIO NEGRO", "SANTA FE"]
#regions = ["CORDOBA", "CHACO", "JUJUY", "LA RIOJA", "MENDOZA", "NEUQUEN", "RIO NEGRO", "SANTA FE"]

#Selecting data to display
startDate = "2020-05-01" #Starting point for plotbyDate. Default: 03/03
#startDate = "2020-04-15"
caseCount = 10 #Starting point for plotbyOutbreak (number of confirmed cases)
dataGuide = 2 #Data type to calculate startpoints (0 for confirmed, 2 for deaths)

#Deciding language for titles and tags...
lg = 0 # 0 for english, 1 for spanish

#Deciding if you want to save and show charts...
saveChart = True
showChart = False

#Deciding what to plot...
confirmedByDate = True #Decide if you want to plot confirmed data by date for selected regions.
deathsByDate = True #Decide if you want to plot deaths data by date for selected regions.
confirmedAndDeathsbyDate = True
confirmedByOutbreak = True #Decide if you want to plot confirmed cases since dataGuide.
deathsByOutbreak = True #Decide if you want to plot deaths since dataGuide.
confirmedAndDeathsbyOutbreak = True
newConfirmedCases = False #Decide if you want to plot new daily confirmed cases for selected regions
newConfirmedCasesTrend = False #Decide if you want to plot new daily cases trend (3 day average)
newConfirmedCasesTrend7 = True #Decide if you want to plot new daily cases trend (5 day average)
newDeaths = False #Decide if you want to plot new daily deaths for selected regions
newDeathsTrend = False #Decide if you want to plot new daily deaths trend (3 day average)
newDeathsTrend7 = True #Decide if you want to plot new daily deaths trend (5 day average)
newConfirmedAndDeathsTrend = True
deathRate = False #Decide if you want to plot death rate evolution for selected regions
deathsAndDeathRate = True
confirmedDuplication = False #Decide if you want to plot linear confirmed cases duplication times
confirmedDuplicationTrend = False #Decide if you want to plot linear confirmed cases duplication times trend
deathsDuplication = False #Decide if you want to plot linear deaths duplication times
deathsDuplicationTrend = False #Decide if you want to plot linear deaths duplication times trend
confirmedAndDeathsDuplicationTrend = False
weeklyAnalysis = False #Decide if you want to plot new daily cases by day of the week for selected regions
weeklyAnalysisType = "relative" # You can plot "absolute" values, "relative" to week maximum or "both"
plotAllCountry = True #Decide if you want a final plot with summary for cases in Argentina.
duplicationTimesAC = False #Decide if you want to plot Duplication Times in the country.
weeklyAnalysisAC = False #Decide if you want to plot week day data of notified cases in Argentina.

#Deciding between linear or logarithmic scales...
plotScale = "linear"
ticksSizes = [25000, 400, 1000, 20, 0.05]
#ticksSizes = [1000, 20, 50, 3, 0.05]

#Variables to store filenames and other strings...
fileNamePrefix = "Argentina_COVID19_"
fileNames = ["00_Confirmed.csv", "01_Active.csv", "02_Deaths.csv", "03_Recovered.csv", "04_Tested.csv",
				"05_Dropped.csv", "06_Deathrate.csv", "07_NewConfirmed.csv", "08_NewConfirmed3dAv.csv",
				"09_ActiveVariation.csv", "10_ActiveVariation3dAv.csv", "11_NewDeaths.csv", "12_NewDeaths3dAv.csv",
				"13_NewRecovered.csv", "14_NewRecovered3dAv.csv", "15_NewTested.csv", "16_NewTested3dAv.csv",
				"17_PositiveTestsRatio.csv", "18_PositiveTestsRatio3dAv.csv", "19_CumulativePositiveTestsRatio.csv",
				"20_DuplicationTimes.csv", "21_DuplicationTimes3dAv.csv", "22_DeathDuplicationTimes.csv",
				"23_DeathDuplicationTimes3dAv.csv", "24_NewDropped.csv", "25_NewDropped3dAv.csv",
				"26_NewConfirmed7dAv.csv", "27_ActiveVariation7dAv.csv", "28_Newdeaths7dAv.csv", "29_NewRecovered7dAv.csv",
				"30_NewTested7dAv.csv", "31_NewDropped7dAv.csv", "32_DuplicationTimes7dAv.csv", "33_DeathDuplicationTimes7dAv.csv",
				"34_PositiveTestsRatio7dAv.csv"]
dataTitles = ["Confirmed cases", "Casos confirmados", "Active cases", "Casos activos", "Deaths", "Fallecimientos", 
				"Recovered patients", "Altas", "Laboratory Tests", "Tests", "Dropped cases", "Casos descartados",
				"Death rate", "Tasa de mortalidad", "Daily confirmed cases", "Casos diarios", "New confirmed cases trend",
				"Casos diarios (3 días)", "Active cases variation", "Evolución de casos activos",
				"Active cases variation trend", "Evolución de casos activos (3 días)", "New deahts",
				"Fallecimientos diarios", "New deaths trend", "Fallecimientos diarios (3 días)", "New recovered",
				"Altas diarias", "New recovered trend", "Altas diarias (3 días)", "Daily tests", "Tests diarios",
				"Daily tests trend", "Tests diarios (3 días)", "Positive tests ratio", "Porcentaje de tests positivos",
				"Positive tests ratio trend", "Porcentaje de tests positivos (3 días)", "Cumulative positive tests ratio",
				"Porcentaje acumulado de tests positivos", "Linear duplication times", "Tiempos de duplicación (lineal)",
				"Linear duplication times trend", "Tiempos de duplicación (3 días)", "Deaths duplication times",
				"Duplicación de fallecimientos (lineal)", "Deahts duplication times trend",
				"Duplicación de fallecimientos (3 días)", "Daily dropped cases", "Casos descartados diariamente",
				"Daily dropped cases trend", "Casos descartados diariamente (3 días)", "New confirmed cases trend (7 days)",
				"Casos diarios (7 días)", "Active cases variation trend (7 days)", "Evolución de casos activos (7 días)",
				"New deaths trend (7 days)", "Fallecimientos diarios (7 días)", "New recovered trend (7 days)",
				"Altas diarias (7 días)", "Daily tests trend (7 days)", "Tests diarios (7 días)",
				"Daily dropped cases trend (7 days)", "Casos descartados diariamente (7 días)"]
plotTitles = ["COVID-19 outbreak in Argentina", "COVID-19: el brote en Argentina", "Total cases", "Totales",
				"New cases trend (3 days average)", "Tendencia diaria (promedio 3 días)", "Deaths", "Fallecimientos",
				"Daily deaths (3 days average)", "Fallecimientos diarios (promedio 3 días)", "Deaths & positive tests ratios",
				"Tasas de mortalidad y tests positivos", "Testing & dropped cases", "Confirmados vs. descartados",
				"Linear duplication times (7 days)", "Tiempos de duplicación (7 días)", "New cases trend (7 days average)",
				"Tendencia diaria (promedio 7 días)", "Daily deaths (7 days average)", "Fallecimientos diarios (promedio 7 días)",
				"Positive tests ratios", "Tasa de positividad"]
shortLabels = ["Confirmed", "Confirmados", "Active", "Activos", "Deaths", "Fallecimientos", "Death rate",
				"Tasa de mortalidad", "Positive trend (7 days)", "Positividad (7 días)", "Positive ratio", "Positividad acumulada",
				"Laboratory tests", "Pruebas de diagnóstico", "Dropped cases", "Casos descartados"]
xTitles = ["Time in days", "Tiempo en días"]
yTitles = ["Number of cases", "Número de casos", "Deaths", "Fallecidos", "Death rate", "Tasa de mortalidad",
			"Laboratory tests", "Pruebas de laboratorio", "Positive tests ratio", "Tasa de positividad",
			"Days needed for\nconfirmed cases to double", "Días necesarios para\nque los casos se dupliquen",
			"Days needed\nfor deaths to double", "Días necesarios para que\nlos fallecimientos se dupliquen"]
tConector = [" since ", " desde ", " after ", " después de ", " (absolute)", " (valores absolutos)",
				" (relative)", " (valores relativos)", "\nand ", "\ny "]

filePath = "Argentina_Data/processed_data/"
chartPath = "Argentina_Data/actual_charts/"
#chartPath = "aux/"

#Some styling...
defaultFont = "Oswald" #Change this if you don't like it or is not available in your system
legendFont = "Myriad Pro" #Change this to edit legends' font 
colorlist = ["tab:orange", "tab:blue", "firebrick", "tab:green", "rebeccapurple", "brown",
				"crimson", "darkcyan", "steelblue", "indianred", "seagreen", "slateblue", "dodgerblue",
				"slategrey", "royalblue", "navy", "limegreen", "goldenrod", "greenyellow", "darkturquoise",
				"coral", "tab:pink", "white"] #Default colors for data
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
	databases.append(pd.read_csv(filePath + fileNamePrefix + fileNames[d]))
	databases[d].set_index("FECHA", inplace = True)
	databases[d].index = pd.DatetimeIndex(databases[d].index)
	databases[d].index.name = "FECHA"

#Constant configurations...
dayTags = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
startDateTime = dt.strptime(startDate, "%Y-%m-%d")
startDateDay = 1
regionsIndexes = [[],[]]
quarantineStart = "2020-03-21"
startDateIndex = databases[0].index.get_loc(startDate) #Saving the startDate index for annotations
quarantineIndex = databases[0].index.get_loc(quarantineStart)
dateFormat = mdates.DateFormatter('%b %d')
dateFormatString = "%B %d"	
if lg ==1:
	dateFormat = mdates.DateFormatter('%d/%m')
	dateFormatString = "%d/%m"
	dayTags = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
	
#Printing selected regions on console
print("Plotting data of " + str(regions), end="\n")

#Method to draw a mark in social isolation start date
def markQuarantine(tag, yshift, ytshift, font, x, y, w, hw, hl):
	if startDate < quarantineStart and plotScale == "linear":
		plt.annotate(tag, fontsize=font, xy=(x, y + yshift),  xycoords='data',
    		xytext=(x, y + ytshift), textcoords='data',
			arrowprops=dict(facecolor='orangered', edgecolor="none", width=w, headwidth=hw, headlength=hl),
        	horizontalalignment='center', verticalalignment='top')

def savePlot(csvName, figure, directory):
	chartName = csvName.split(".")
	plt.savefig(chartPath + directory + str(lg) + "_" + chartName[0] + ".png", facecolor=figure.get_facecolor())

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

def plotbyDate(regions, datatype, xtitle, ytitle, markQ, ticksInterval, savechart, show):
	figure = plt.figure(num=None, figsize=(8, 4), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	#Saving y values for markQ...
	yquarantine = []
	x = quarantineIndex
	#Plotting selected data...
	for i in range(len(regions)):
		databases[datatype][startDate:][regions[i]].plot(kind='line', label=regions[i], color=colorlist[i], linewidth=2.5)
		yquarantine.append(databases[datatype].loc[quarantineStart, regions[i]])
	s = plt.ylim()
	if markQ == True:
		y = max(yquarantine) #Drawing a mark on quarantineStartDate
		#y = 0
		markQuarantine("Social\nisolation", s[1]/25, s[1]/5, 8, quarantineStart, y, 5, 9, 7)
	#Setting up titles	
	plt.title("COVID-19: " + dataTitles[2*(datatype)+lg] + tConector[lg] + startDateTime.strftime(dateFormatString), fontname=defaultFont)
	plt.yscale(plotScale)
	plt.ylabel(ytitle, fontname=legendFont)
	plt.xlabel(xtitle, fontname=legendFont)
	#Setting up grid...
	gridAndTicks(s[1]*1.1, ticksInterval)
	ticksLocator(1)
	#Setting axis labels font and legend
	if len(regions) > 1:
		plt.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	plt.tight_layout()
	if savechart == True:
		savePlot("D_" + fileNames[datatype], figure, "byDate/")
	if show == True:
		plt.show()

#Function to look for certain case count in each region
def regionsStartPoints(regions, dataguide):
	startPoints = []
	for r in range(len(regions)):
		for e in databases[dataguide].index.to_list():
			if databases[dataguide].loc[e, regions[r]] >= caseCount:
				startPoints.append(e)
				break
	return startPoints

startPoints = regionsStartPoints(regions, dataGuide)

#Function to plot cases for regions since first case
def plotbyOutbreak(regions, datatype, dataguide, startpoints, xtitle, ytitle, ticksInterval, savechart, show):
	figure = plt.figure(num=None, figsize=(8, 4), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	period = 0
	#Plotting selected data...
	for i in range(len(regions)):
		datalist = databases[datatype][startPoints[i]:][regions[i]].values.tolist()
		if i == 0:
			period = len(datalist) - 1
		plt.plot(datalist[0:period], label=regions[i], linewidth=2.5, color=colorlist[i])
	#Setting up titles
	plt.title("COVID-19: " + dataTitles[2*datatype+lg] + tConector[2 + lg] + str(caseCount) + " " + dataTitles[2*dataguide+lg], fontname=defaultFont)
	plt.yscale(plotScale)
	plt.ylabel(ytitle, fontname=legendFont)
	plt.xlabel(xtitle, fontname=legendFont)
	#Setting up grid...
	s = plt.ylim()
#	d = plt.xlim()
	gridAndTicks(s[1]*1.1, ticksInterval)
	if len(regions) > 1:
		plt.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	plt.tight_layout()
	if savechart == True:
		savePlot("O_" + fileNames[datatype], figure, "byOutbreak/")
	if show == True:
		plt.show()
	
def plotDoublebyDate(regions, datatypeA, datatypeB, xtitle, ytitleA, ytitleB, markQ, ticksIntervalA, ticksIntervalB, savechart, show):
	figure = plt.figure(num=None, figsize=(5, 4.5), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	#if superiorTitles == True:
	#	figure.suptitle("COVID-19: " + dataTitles[2*(datatypeA)+lg] + tConector[8+lg] + dataTitles[2*(datatypeB)+lg] +
	#					 tConector[lg] + startDateTime.strftime(dateFormatString), fontsize=11, fontname=defaultFont)
	plt.subplot2grid((2, 1), (0, 0))
	#Saving y values for markQ...
	yquarantine = []
	x = quarantineIndex
	#Plotting selected data...
	for i in range(len(regions)):
		plotA = databases[datatypeA][startDate:][regions[i]].plot(kind='line', label=regions[i], color=colorlist[i], linewidth=2.5)
		yquarantine.append(databases[datatypeA].loc[quarantineStart, regions[i]])
	s = plt.ylim()
	a = plt.xlim()
	if markQ == True:
		y = max(yquarantine) #Drawing a mark on quarantineStartDate
		markQuarantine("", s[1]/20, s[1]/5, 8, quarantineStart, y, 5, 9, 7)
	#Setting up titles	
	plotA.set_title(dataTitles[2*(datatypeA)+lg], fontname=defaultFont, fontsize=10)
	plt.yscale(plotScale)
	#plt.ylabel(ytitleA, fontname=legendFont)
	plt.ylabel("")
	plt.xlabel("")
	plt.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	#Setting up grid...
	gridAndTicks(s[1]*1.1, ticksIntervalA)
	ticksLocator(2)
	plt.gca().xaxis.set_ticklabels([])
	#Setting axis labels font and legend
	plt.subplot2grid((2, 1), (1, 0))
	#Saving y values for markQ...
	yquarantine = []
	x = quarantineIndex
	#Plotting selected data...
	for i in range(len(regions)):
		plotB = databases[datatypeB][startDate:][regions[i]].plot(kind='line', label=regions[i], color=colorlist[i], linewidth=2.5)
		yquarantine.append(databases[datatypeB].loc[quarantineStart, regions[i]])
	s = plt.ylim()
	plt.xlim(a[0], a[1])
	if markQ == True:
		y = max(yquarantine) #Drawing a mark on quarantineStartDate
		markQuarantine("", s[1]/20, s[1]/5, 8, quarantineStart, y, 5, 9, 7)
	#Setting up titles	
	plotB.set_title(dataTitles[2*(datatypeB)+lg], fontname=defaultFont, fontsize=10)
	plt.yscale(plotScale)
	#plt.ylabel(ytitleB, fontname=legendFont)
	plt.ylabel("")
	plt.xlabel(xtitle, fontname=legendFont)
	#plt.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	#Setting up grid...
	gridAndTicks(s[1]*1.1, ticksIntervalB)
	ticksLocator(2)
	plt.tight_layout(rect=[0, 0, 1, 1])
	if savechart == True:
		auxName = fileNames[datatypeA].split(".")
		savePlot("D_" + auxName[0] + "_" + fileNames[datatypeB], figure, "byDate/")
	if show == True:
		plt.show()

def plotDoublebyOutbreak(regions, datatypeA, datatypeB, dataguide, xtitle, ytitleA, ytitleB, ticksIntervalA, ticksIntervalB, savechart, show):
	figure = plt.figure(num=None, figsize=(5, 4.5), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	#if superiorTitles == True:
	#	figure.suptitle("COVID-19: " + dataTitles[2*(datatypeA)+lg] + tConector[8+lg] + dataTitles[2*(datatypeB)+lg] +
	#					 tConector[2+lg] + str(caseCount)  + " " + dataTitles[2*dataguide+lg], fontsize=11, fontname=defaultFont)
	plt.subplot2grid((2, 1), (0, 0))
	period = 0
	#Plotting selected data...
	for i in range(len(regions)):
		datalist = databases[datatypeA][startPoints[i]:][regions[i]].values.tolist()
		if i == 0:
			period = len(datalist) - 1
		plt.plot(datalist[0:period], label=regions[i], linewidth=2.5, color=colorlist[i])
	s = plt.ylim()
	a = plt.xlim()
	#Setting up titles	
	plt.title(dataTitles[2*(datatypeA)+lg], fontname=defaultFont)
	plt.yscale(plotScale)
	#plt.ylabel(ytitleA, fontname=legendFont)
	plt.ylabel("")
	plt.xlabel("")
	#plt.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	#Setting up grid...
	gridAndTicks(s[1]*1.1, ticksIntervalA)
	plt.gca().xaxis.set_ticklabels([])
	#Setting axis labels font and legend
	plt.subplot2grid((2, 1), (1, 0))
	#Plotting selected data...
	for i in range(len(regions)):
		datalist = databases[datatypeB][startPoints[i]:][regions[i]].values.tolist()
		if i == 0:
			period = len(datalist) - 1
		plt.plot(datalist[0:period], label=regions[i], linewidth=2.5, color=colorlist[i])
	s = plt.ylim()
	plt.xlim(a[0], a[1])
	#Setting up titles	
	plt.title(dataTitles[2*(datatypeB)+lg], fontname=defaultFont)
	plt.yscale(plotScale)
	#plt.ylabel(ytitleB, fontname=legendFont)
	plt.ylabel("")
	plt.xlabel(xtitle, fontname=legendFont)
	plt.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	#Setting up grid...
	gridAndTicks(s[1]*1.1, ticksIntervalB)
	plt.tight_layout(rect=[0, 0, 1, 1])
	if savechart == True:
		auxName = fileNames[datatypeA].split(".")
		savePlot("O_" + auxName[0] + "_" + fileNames[datatypeB], figure, "byOutbreak/")
	if show == True:
		plt.show()

def plotArgentinaA(savechart, show):
	figure = plt.figure(num=None, figsize=(5, 4.5), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	#Setting up totals chart...
	plt.subplot2grid((2, 1), (0, 0))
	x = quarantineStart
	yquarantine = []
	total = databases[0][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*0+lg], color=colorlist[0])
	yquarantine.append(databases[0].loc[x, "ARGENTINA"])
	total = databases[2][startDate:]["ARGENTINA"].plot(kind="line", linewidth=1.7, label=shortLabels[2*2+lg], color=colorlist[2])
	yquarantine.append(databases[2].loc[x, "ARGENTINA"])
	y = max(yquarantine)
	s = plt.ylim()
	a = plt.xlim()
	markQuarantine("", s[1]/20, s[1]/4.5, 8, x, y, 3, 6, 5)
	total.legend(loc=0, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	total.set_title(plotTitles[2*1+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	plt.xlabel("")
	gridAndTicks(s[1]*1.1, 50000)
	ticksLocator(2)
	ylabels = nu.arange(0, s[1]/1000*1.1, 50).tolist()
	for l in range(len(ylabels)):
		ylabels[l] = "{:.0f}".format(ylabels[l])
		ylabels[l] += "K"
	plt.yticks(nu.arange(0, s[1] * 1.1, 50000), ylabels)
	plt.gca().xaxis.set_ticklabels([])
	#Setting up new daily chart...
	plt.subplot2grid((2, 1), (1, 0))
	yquarantine = []
	newtrend = databases[26][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*0+lg], color=colorlist[0])
	yquarantine.append(databases[26].loc[x, "ARGENTINA"])
	newtrend = databases[28][startDate:]["ARGENTINA"].plot(kind="line", linewidth=1.7, label=shortLabels[2*2+lg], color=colorlist[2])
	yquarantine.append(databases[28].loc[x, "ARGENTINA"])
	y = max(yquarantine)
	s = plt.ylim()			
	markQuarantine("", s[1]/20, s[1]/4.5, 8, x, y, 3, 6, 5)
	newtrend.legend(loc=0, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	newtrend.set_title(plotTitles[2*8+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	s = plt.ylim()
	plt.xlabel("")
	gridAndTicks(s[1]*1.1, 1500)
	ticksLocator(2)
	plt.xlim(a[0], a[1])
	plt.tight_layout(rect=[0, 0, 1, 1])
	if savechart == True:
		savePlot("ArgentinaA.csv", figure, "")
	if show == True:
		plt.show()
		
def plotArgentinaB(savechart, show):
	figure = plt.figure(num=None, figsize=(5, 4.5), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	#Setting up new deaths chart...
	plt.subplot2grid((2, 1), (0, 0))
	newdeaths = databases[28][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*2+lg], color=colorlist[2])
	newdeaths.set_title(plotTitles[2*9+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	s = plt.ylim()
	plt.xlabel("")
	gridAndTicks(s[1]*1.1, 30)
	ticksLocator(2)
	a = plt.xlim()
	plt.gca().xaxis.set_ticklabels([])
	#Setting up ratios chart...
	plt.subplot2grid((2, 1), (1, 0))
	ratios = databases[6][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*3+lg], color=colorlist[2])
	ratios.set_title(shortLabels[6+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	s = plt.ylim()
	plt.xlabel("")
	gridAndTicks(s[1]*1.1, 0.025)
	ticksLocator(2)
	plt.xlim(a[0], a[1])
	plt.tight_layout(rect=[0, 0, 1, 1])
	if savechart == True:
		savePlot("ArgentinaB.csv", figure, "")
	if show == True:
		plt.show()

def plotArgentinaC(savechart, show):
	figure = plt.figure(num=None, figsize=(5, 4.5), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	#Setting up Tested vs Dropped...
	plt.subplot2grid((2, 1), (0, 0))
	ratios = databases[19][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*5+lg], color=colorlist[1])
	ratios = databases[34][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*4+lg], color=colorlist[0])
	ratios.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	ratios.set_title(plotTitles[20+lg], fontsize=10, fontname=defaultFont)
	ratios.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	plt.yscale(plotScale)
	s = plt.ylim()
	gridAndTicks(s[1]*1.1, 0.1)
	ticksLocator(2)
	plt.xlabel("")
	a = plt.xlim()
	plt.gca().xaxis.set_ticklabels([])
	#Plotting duplication times...
	plt.subplot2grid((2, 1), (1, 0))
	duplication = databases[33][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*2+lg], color=colorlist[2], zorder=2)
	duplication = databases[32][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*0+lg], color=colorlist[1], zorder=3)
	duplication.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	plt.fill_between(databases[33][startDate:].index.values, databases[33][startDate:]["ARGENTINA"], 0, facecolor=colorlist[2],
					alpha=0.5, zorder=2)
	plt.fill_between(databases[32][startDate:].index.values, databases[32][startDate:]["ARGENTINA"], 0, facecolor=colorlist[1],
					alpha=0.5, zorder=3)
	duplication.set_title(plotTitles[2*7+lg], fontsize=10, fontname=defaultFont)
	plt.ylabel("")
	plt.xlabel("")
	plt.xlim(a[0], a[1])
	plt.grid(which='both', axis='both')
	plt.yscale(plotScale)
	s = plt.ylim()
	gridAndTicks(s[1]*1.1, 15)
	ticksLocator(2)
	plt.tight_layout(rect=[0, 0, 1, 1])
	if savechart == True:
		savePlot("ArgentinaC.csv", figure, "")
	if show == True:
		plt.show()
	
def plotAllCountryDataWide(savechart, show):
	figure = plt.figure(num=None, figsize=(7, 4.5), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	figure.suptitle(plotTitles[0+lg], fontsize=12, fontname=defaultFont)
	#Setting up totals chart...
	plt.subplot2grid((3, 2), (0, 0))
	x = quarantineStart
	yquarantine = []
	total = databases[0][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*0+lg], color=colorlist[0])
	yquarantine.append(databases[0].loc[x, "ARGENTINA"])
	total = databases[2][startDate:]["ARGENTINA"].plot(kind="line", linewidth=1.7, label=shortLabels[2*2+lg], color=colorlist[2])
	yquarantine.append(databases[2].loc[x, "ARGENTINA"])
	y = max(yquarantine)
	s = plt.ylim()
	a = plt.xlim()
	markQuarantine("", s[1]/20, s[1]/4.5, 8, x, y, 3, 6, 5)
	total.legend(loc=0, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	total.set_title(plotTitles[2*1+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	plt.xlabel("")
	gridAndTicks(s[1]*1.1, 100000)
	ticksLocator(2)
	ylabels = nu.arange(0, s[1]/1000*1.1, 100).tolist()
	for l in range(len(ylabels)):
		ylabels[l] = "{:.0f}".format(ylabels[l])
		ylabels[l] += "K"
	plt.yticks(nu.arange(0, s[1] * 1.1, 100000), ylabels)
	plt.gca().xaxis.set_ticklabels([])
	#Setting up new daily chart...
	plt.subplot2grid((3, 2), (0, 1))
	yquarantine = []
	newtrend = databases[26][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*0+lg], color=colorlist[0])
	yquarantine.append(databases[26].loc[x, "ARGENTINA"])
	newtrend = databases[28][startDate:]["ARGENTINA"].plot(kind="line", linewidth=1.7, label=shortLabels[2*2+lg], color=colorlist[2])
	yquarantine.append(databases[28].loc[x, "ARGENTINA"])
	y = max(yquarantine)
	s = plt.ylim()			
	markQuarantine("", s[1]/20, s[1]/4.5, 8, x, y, 3, 6, 5)
	newtrend.legend(loc=0, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	newtrend.set_title(plotTitles[2*8+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	s = plt.ylim()
	plt.xlabel("")
	gridAndTicks(s[1]*1.1, 2000)
	ticksLocator(2)
	plt.xlim(a[0], a[1])
	plt.gca().xaxis.set_ticklabels([])
	#Setting up new deaths chart...
	plt.subplot2grid((3, 2), (1, 0))
	newdeaths = databases[28][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*2+lg], color=colorlist[2])
	newdeaths.set_title(plotTitles[2*9+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	s = plt.ylim()
	plt.xlabel("")
	gridAndTicks(s[1]*1.1, 50)
	ticksLocator(2)
	plt.xlim(a[0], a[1])
	plt.gca().xaxis.set_ticklabels([])
	#Setting up ratios chart...
	plt.subplot2grid((3, 2), (1, 1))
	ratios = databases[19][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*5+lg], color=colorlist[1])
	ratios = databases[34][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*4+lg], color=colorlist[0])
	ratios = databases[6][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*3+lg], color=colorlist[2])
	ratios.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	ratios.set_title(plotTitles[2*5+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	s = plt.ylim()
	plt.xlabel("")
	gridAndTicks(s[1]*1.1, 0.1)
	ticksLocator(2)
	plt.xlim(a[0], a[1])
	plt.gca().xaxis.set_ticklabels([])
	#Setting up Tested vs Dropped...
	plt.subplot2grid((3, 2), (2, 0))
	tests = databases[4][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*6+lg], color=colorlist[0])
	tests = databases[5][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*7+lg], color=colorlist[1])
	tests.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	tests.set_title(plotTitles[2*6+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	s = plt.ylim()
	gridAndTicks(s[1]*1.1, 300000)
	ticksLocator(2)
	ylabels = nu.arange(0, s[1]/1000*1.1, 300).tolist()
	for l in range(len(ylabels)):
		ylabels[l] = "{:.0f}".format(ylabels[l])
		ylabels[l] += "K"
	plt.yticks(nu.arange(0, s[1] * 1.1, 300000), ylabels)
	plt.xlabel("")
	plt.xlim(a[0], a[1])
	#Plotting duplication times...
	plt.subplot2grid((3, 2), (2, 1))
	duplication = databases[33][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*2+lg], color=colorlist[2], zorder=2)
	duplication = databases[32][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*0+lg], color=colorlist[1], zorder=3)
	duplication.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	plt.fill_between(databases[33][startDate:].index.values, databases[33][startDate:]["ARGENTINA"], 0, facecolor=colorlist[2],
					alpha=0.5, zorder=2)
	plt.fill_between(databases[32][startDate:].index.values, databases[32][startDate:]["ARGENTINA"], 0, facecolor=colorlist[1],
					alpha=0.5, zorder=3)
	duplication.set_title(plotTitles[2*7+lg], fontsize=10, fontname=defaultFont)
	plt.ylabel("")
	plt.xlabel("")
	plt.xlim(a[0], a[1])
	plt.grid(which='both', axis='both')
	plt.yscale(plotScale)
	s = plt.ylim()
	gridAndTicks(s[1]*1.1, 15)
	ticksLocator(2)
	plt.tight_layout(rect=[0, 0.03, 1, 0.95])
	if savechart == True:
		savePlot("Argentina.csv", figure, "")
	if show == True:
		plt.show()	

def plotAllCountryDT(savechart, show):
	figure = plt.figure(num=None, figsize=(7, 4), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	#Setting up first subplot...
	plt.subplot2grid((2, 1), (0, 0))
	#Plotting the data...
	plt.bar(databases[21][startDate:].index, databases[21][startDate:]["ARGENTINA"])
	#Marking quarantine start...
	x = dt.strptime(quarantineStart, "%Y-%m-%d")
	y = databases[21].loc[quarantineStart, "ARGENTINA"]
	s = plt.ylim()
	q = plt.xlim()
	markQuarantine("", s[1]/20, s[1]/6, 6, x, y, 3, 6, 5)
	#Setting up titles	
	plt.title("Argentina: " + dataTitles[(2*21)+lg] + tConector[lg] + startDateTime.strftime(dateFormatString), fontsize=11, fontname=defaultFont)
	plt.ylabel(yTitles[10+lg], fontsize=9, fontname=legendFont)
	plt.xlabel("")
	#Setting up grid...
	gridAndTicks(s[1]*1.1, 10)
	ticksLocator(2)
	plt.gca().xaxis.set_ticklabels([])
	#Setting up second subplot...
	plt.subplot2grid((2, 1), (1, 0))
	plt.bar(databases[23][startDate:].index, databases[23][startDate:]["ARGENTINA"])
	plt.xlim(q[0], q[1])
	#Marking quarantine start...
	y = databases[23].loc[quarantineStart, "ARGENTINA"]
	s = plt.ylim()
	markQuarantine("", s[1]/20, s[1]/6, 6, x, y, 3, 6, 5)
	plt.ylabel(yTitles[12+lg], fontsize=9, fontname=legendFont)
	plt.xlabel(xTitles[0+lg], fontsize=9, fontname=legendFont)
	#Setting up grid...
	gridAndTicks(s[1]*1.1, 10)
	ticksLocator(2)
	plt.tight_layout()
	if savechart == True:
		savePlot("ArgentinaDT.csv", figure, "byDate/")
	if show == True:
		plt.show()
	
def getDaysTags(dayTags, offset):
	daylist = []
	for d in range(len(dayTags)):
		daylist.append(dayTags[(d + startDateDay + offset)%7])
	return daylist

weekCount = int(databases[0][startDate:].shape[0]/7)
days = getDaysTags(dayTags, 0)

def getWeeklyCases(region, datatype):
	weeklyCases = pd.DataFrame(index=nu.arange(0, weekCount + 3, 1), columns=days)
	for d in range(7):
		for w in range(weekCount):
			weeklyCases.loc[w,days[d]] = databases[datatype].loc[databases[datatype].index[w*7 + d], region]
		weeklyCases.loc[weekCount,days[d]] = weeklyCases[0:weekCount][days[d]].min()
		weeklyCases.loc[weekCount+1,days[d]] = weeklyCases[0:weekCount][days[d]].max()
		weeklyCases.loc[weekCount+2,days[d]] = weeklyCases[0:weekCount][days[d]].mean()
	return weeklyCases

def getWeeklyCasesR(weeklyCases):
	weeklyCasesR = pd.DataFrame(index=weeklyCases.index, columns=weeklyCases.columns)
	for w in range(weekCount):
		weekMax = weeklyCases.loc[weeklyCases.index[w],:].max()
		if weekMax > 0:
			for d in range(7):
				weeklyCasesR.loc[w,days[d]] = weeklyCases.loc[weeklyCases.index[w], days[d]]/weekMax
	for d in range(7):
		weeklyCasesR.loc[weekCount,days[d]] = weeklyCasesR[0:weekCount][days[d]].min()
		weeklyCasesR.loc[weekCount+1,days[d]] = weeklyCasesR[0:weekCount][days[d]].max()
		weeklyCasesR.loc[weekCount+2,days[d]] = weeklyCasesR[0:weekCount][days[d]].mean()
	return weeklyCasesR

def buildWeeklyData(regions, datatype):
	weeklyData = []
	for d in range(len(regions)):
		weeklyData.append(getWeeklyCases(regions[d], datatype))
	return weeklyData

def buildWeeklyDataR(weeklyCases):
	weeklyDataR = []
	for d in range(len(weeklyCases)):
		weeklyDataR.append(getWeeklyCasesR(weeklyCases[d]))
	return weeklyDataR

def plotWeeklyCases(weeklyConfirmed, weeklyDeaths, yTitleC, yTitleD, region, aType, savechart, show):
	figure = plt.figure(num=None, figsize=(5, 4), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	figure.suptitle(region + ": Weeks analysis" + tConector[lg] + startDateTime.strftime(dateFormatString) + 
					aType, fontsize=12, fontname=defaultFont)
	weekCount = weeklyConfirmed.shape[0]-3
	#Plotting analysis for confirmed cases...
	plt.subplot2grid((2, 1), (0, 0))
	for w in range(weekCount):
		weeklyConfirmed.loc[weeklyConfirmed.index[w],:].plot(linewidth=2.0, color=colorlist[3], alpha=0.3)
	weeklyConfirmed.loc[weeklyConfirmed.index[weekCount],:].plot(linewidth=2.0, color=colorlist[1], alpha=0.6)
	weeklyConfirmed.loc[weeklyConfirmed.index[weekCount + 1],:].plot(linewidth=2.0, color=colorlist[1], alpha=0.6)
	weeklyConfirmed.loc[weeklyConfirmed.index[weekCount + 2],:].plot(linewidth=2.0, color=colorlist[2], alpha=1.0)
	plt.title(dataTitles[0+lg] , fontsize=10, fontname=defaultFont)
	plt.grid()
	plt.ylabel(yTitleC, fontsize=6)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.1, ylimits[1]/5))
	plt.xticks(nu.arange(0, 7, 1))
	plt.gca().xaxis.set_ticklabels([])
	plt.xticks(fontsize=5)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.gca().set_facecolor(backgroundPlot)
	#Plotting analysis for deahts...
	plt.subplot2grid((2, 1), (1, 0))
	for w in range(weekCount):
		weeklyDeaths.loc[weeklyDeaths.index[w],:].plot(linewidth=2.0, color=colorlist[3], alpha=0.3)
	weeklyDeaths.loc[weeklyDeaths.index[weekCount],:].plot(linewidth=2.0, color=colorlist[1], alpha=1.0)
	weeklyDeaths.loc[weeklyDeaths.index[weekCount + 1],:].plot(linewidth=2.0, color=colorlist[1], alpha=1.0)
	weeklyDeaths.loc[weeklyDeaths.index[weekCount + 2],:].plot(linewidth=2.0, color=colorlist[2], alpha=1.0)
	plt.title(dataTitles[4+lg] , fontsize=10, fontname=defaultFont)
	plt.grid()
	plt.ylabel(yTitleD, fontsize=6)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.1, ylimits[1]/5))
	plt.xticks(nu.arange(0, 7, step = 1), days, fontsize = 6, rotation = 30, fontname=legendFont)
	plt.xticks(fontsize=5)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.gca().set_facecolor(backgroundPlot)
	plt.tight_layout(rect=[0, 0.03, 1, 0.95])
	if savechart == True:
		savePlot(region + "_WA.csv", figure, "weekAnalysis/")
	if show == True:
		plt.show()

def plotWeeklyAnalysis(weeklyConfirmed, weeklyDeaths, yTitleC, yTitleD, aType, regions, savechart, showchart):
	for d in range(len(regions)):
		plotWeeklyCases(weeklyConfirmed[d], weeklyDeaths[d], yTitleC, yTitleD, regions[d], aType, savechart, showchart)

#Calling the functions to build selected charts...
if confirmedByDate == True:
	print("Plotting confirmed cases data by date...", end="\n")
	plotbyDate(regions, 0, xTitles[0+lg], yTitles[0+lg], True, ticksSizes[0], saveChart, showChart)
if deathsByDate == True:
	print("Plotting deaths cases data by date...", end="\n")
	plotbyDate(regions, 2, xTitles[0+lg], yTitles[2+lg], True, ticksSizes[1], saveChart, showChart)
if confirmedAndDeathsbyDate == True:
	plotDoublebyDate(regions, 0, 2, xTitles[0+lg], yTitles[0+lg], yTitles[2+lg], True, ticksSizes[0], 2*ticksSizes[1], saveChart, showChart)
if confirmedByOutbreak == True:
	print("Plotting confirmed cases data by outbreak...", end="\n")
	plotbyOutbreak(regions, 0, dataGuide, startPoints, xTitles[0+lg], yTitles[0+lg], ticksSizes[0], saveChart, showChart)
if deathsByOutbreak == True:
	print("Plotting deaths data by outbreak...", end="\n")
	plotbyOutbreak(regions, 2, dataGuide, startPoints, xTitles[0+lg], yTitles[2+lg], ticksSizes[1], saveChart, showChart)
if confirmedAndDeathsbyOutbreak == True:
	plotDoublebyOutbreak(regions, 0, 2, dataGuide, xTitles[0+lg], yTitles[0+lg], yTitles[2+lg], ticksSizes[0], 2*ticksSizes[1], saveChart, showChart)
if newConfirmedCases == True:
	print("Plotting daily confirmed cases data...", end="\n")
	plotbyDate(regions, 7, xTitles[0+lg], yTitles[0+lg], True, ticksSizes[2], saveChart, showChart)
if newConfirmedCasesTrend == True:
	print("Plotting daily confirmed cases trend data...", end="\n")
	plotbyDate(regions, 8, xTitles[0+lg], yTitles[0+lg], True, ticksSizes[2], saveChart, showChart)
if newConfirmedCasesTrend7 == True:
	print("Plotting daily confirmed cases trend data...", end="\n")
	plotbyDate(regions, 26, xTitles[0+lg], yTitles[0+lg], True, ticksSizes[2], saveChart, showChart)
if newDeaths == True:
	print("Plotting daily deaths cases data...", end="\n")
	plotbyDate(regions, 11, xTitles[0+lg], yTitles[2+lg], True, ticksSizes[3], saveChart, showChart)
if newDeathsTrend == True:
	print("Plotting daily deahts trend...", end="\n")
	plotbyDate(regions, 12, xTitles[0+lg], yTitles[2+lg], True, ticksSizes[3], saveChart, showChart)
if newDeathsTrend7 == True:
	print("Plotting daily deahts trend...", end="\n")
	plotbyDate(regions, 28, xTitles[0+lg], yTitles[2+lg], True, ticksSizes[3], saveChart, showChart)
if newConfirmedAndDeathsTrend == True:
	plotDoublebyDate(regions, 26, 28, xTitles[0+lg], yTitles[0+lg], yTitles[2+lg], True, ticksSizes[2], ticksSizes[3], saveChart, showChart)
	plotDoublebyOutbreak(regions, 26, 28, dataGuide, xTitles[0+lg], yTitles[0+lg], yTitles[2+lg], ticksSizes[2], ticksSizes[3], saveChart, showChart)
if deathRate == True:
	print("Plotting death rate evolution...", end="\n")
	plotbyDate(regions, 6, xTitles[0+lg], yTitles[4+lg], False, ticksSizes[4]/2, saveChart, showChart)
if deathsAndDeathRate == True:
	plotDoublebyDate(regions, 2, 6, xTitles[0+lg], yTitles[2+lg], yTitles[4+lg], True, 2*ticksSizes[1], ticksSizes[4], saveChart, showChart)
if confirmedDuplication == True:
	print("Plotting confirmed cases duplications times by date...", end="\n")
	plotbyDate(regions, 20, xTitles[0+lg], yTitles[10+lg], False, ticksSizes[3], saveChart, showChart)
if confirmedDuplicationTrend == True:
	print("Plotting confirmed cases duplications times trend by date...", end="\n")
	plotbyDate(regions, 21, xTitles[0+lg], yTitles[10+lg], False, ticksSizes[3], saveChart, showChart)
if deathsDuplication == True:
	print("Plotting confirmed cases duplications times by date...", end="\n")
	plotbyDate(regions, 22, xTitles[0+lg], yTitles[12+lg], False, 2*ticksSizes[3], saveChart, showChart)
if deathsDuplicationTrend == True:
	print("Plotting confirmed cases duplications times by date...", end="\n")
	plotbyDate(regions, 23, xTitles[0+lg], yTitles[12+lg], False, 2*ticksSizes[3], saveChart, showChart)
if confirmedAndDeathsDuplicationTrend == True:
	plotDoublebyDate(regions, 21, 23, xTitles[0+lg], yTitles[10+lg], yTitles[12+lg], False, 3*ticksSizes[3], ticksSizes[3], saveChart, showChart)
weeklyConfirmed = []
weeklyDeaths = []
weeklyConfirmedR = []
weeklyDeaths = []
if weeklyAnalysis == True or weeklyAnalysisAC == True:
	print("Ordening data by day of the week...", end="\n")
	weeklyConfirmed = buildWeeklyData(regions, 7)
	weeklyDeaths = buildWeeklyData(regions, 11)
	weeklyConfirmedR = buildWeeklyDataR(weeklyConfirmed)
	weeklyDeathsR = buildWeeklyDataR(weeklyDeaths)
if weeklyAnalysis == True:
	if weeklyAnalysisType == "both":
		print("Plotting week analysis (absolute and relative)...", end="\n")
		plotWeeklyAnalysis(weeklyConfirmed, weeklyDeaths, yTitles[0+lg], yTitles[2+lg], tConector[4+lg], regions, False, showChart)
		plotWeeklyAnalysis(weeklyConfirmedR, weeklyDeathsR, yTitles[0+lg], yTitles[2+lg], tConector[6+lg], regions, False, showChart)
	elif weeklyAnalysisType == "relative":
		print("Plotting week analysis (relative)...", end="\n")
		plotWeeklyAnalysis(weeklyConfirmedR, weeklyDeathsR, yTitles[0+lg], yTitles[2+lg], tConector[6+lg], regions, False, showChart)		
	elif weeklyAnalysisType == "absolute":
		print("Plotting week analysis (absolute)...", end="\n")
		plotWeeklyAnalysis(weeklyConfirmed, weeklyDeaths, yTitles[0+lg], yTitles[2+lg], tConector[4+lg], regions, False, showChart)
if plotAllCountry == True:
	print("Plotting Argentina summary...", end="\n")
	plotAllCountryDataWide(saveChart, showChart)
	plotArgentinaA(saveChart, showChart)
	plotArgentinaB(saveChart, showChart)
	plotArgentinaC(saveChart, showChart)
	if duplicationTimesAC == True:
		plotAllCountryDT(saveChart, showChart)
	if weeklyAnalysisAC == True:
		if weeklyAnalysisType == "both":
			print("Plotting week analysis for Argentina (absolute and relative)...", end="\n")
			plotWeeklyAnalysis(weeklyConfirmed, weeklyDeaths, yTitles[0+lg], yTitles[2+lg], tConector[4+lg], ["ARGENTINA"], saveChart, showChart)
			plotWeeklyAnalysis(weeklyConfirmedR, weeklyDeathsR, yTitles[0+lg], yTitles[2+lg], tConector[6+lg], ["ARGENTINA"], saveChart, showChart)
		elif weeklyAnalysisType == "relative":
			print("Plotting week analysis for Argentina (relative)...", end="\n")
			plotWeeklyAnalysis(weeklyConfirmedR, weeklyDeathsR, yTitles[0+lg], yTitles[2+lg], tConector[6+lg], ["ARGENTINA"], saveChart, showChart)		
		elif weeklyAnalysisType == "absolute":
			print("Plotting week analysis for Argentina (absolute)...", end="\n")
			plotWeeklyAnalysis(weeklyConfirmed, weeklyDeaths, yTitles[0+lg], yTitles[2+lg], tConector[4+lg], ["ARGENTINA"], saveChart, showChart)

#Saying good bye...
print("That's all. If you want more plots, edit the code and run again.                          ", end="\n")