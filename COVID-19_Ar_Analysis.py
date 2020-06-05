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
#regions = ["CABA", "BUENOS AIRES", "CHACO", "SANTA FE", "CORDOBA"]
regions = ["CABA", "BUENOS AIRES", "CHACO"]
#regions = ["NEUQUEN", "MENDOZA", "LA RIOJA", "ENTRE RIOS", "SANTA FE", "SAN JUAN", "CHUBUT"]

#Selecting data to display
startDate = "2020-03-03" #Starting point for plotbyDate. Default: 03/03
caseCount = 200 #Starting point for plotbyOutbreak (number of confirmed cases)
dataGuide = 0 #Data type to calculate startpoints (0 for confirmed, 2 for deaths)

#Deciding what to plot...
confirmedByDate = True #Decide if you want to plot confirmed data by date for selected regions.
deathsByDate = True #Decide if you want to plot deaths data by date for selected regions.
confirmedByOutbreak = True #Decide if you want to plot confirmed cases since dataGuide.
deathsByOutbreak = True #Decide if you want to plot deaths since dataGuide.
newConfirmedCases = False #Decide if you want to plot new daily confirmed cases for selected regions
newConfirmedCasesTrend = True #Decide if you want to plot new daily cases trend (3 day average)
newConfirmedCasesTrend5 = False #Decide if you want to plot new daily cases trend (5 day average)
newDeaths = False #Decide if you want to plot new daily deaths for selected regions
newDeathsTrend = True #Decide if you want to plot new daily deaths trend (3 day average)
newDeathsTrend5 = False #Decide if you want to plot new daily deaths trend (5 day average)
deathRate = True #Decide if you want to plot death rate evolution for selected regions
confirmedDuplication = False #Decide if you want to plot linear confirmed cases duplication times
confirmedDuplicationTrend = True #Decide if you want to plot linear confirmed cases duplication times trend
deathsDuplication = False #Decide if you want to plot linear deaths duplication times
deathsDuplicationTrend = True #Decide if you want to plot linear deaths duplication times trend
weeklyAnalysis = False #Decide if you want to plot new daily cases by day of the week for selected regions
weeklyAnalysisType = "relative" # You can plot "absolute" values, "relative" to week maximum or "both"
plotAllCountry = True #Decide if you want a final plot with summary for cases in Argentina.
duplicationTimesAC = False #Decide if you want to plot Duplication Times in the country.
weeklyAnalysisAC = True #Decide if you want to plot week day data of notified cases in Argentina.

#Deciding between linear or logarithmic scales...
plotScale = "linear"

#Deciding language for titles and tags...
lg = 0 # 0 for english, 1 for spanish

#Variables to store filenames and other strings...
fileNamePrefix = "Argentina_COVID19_"
fileNames = ["00_Confirmed.csv", "01_Active.csv", "02_Deaths.csv", "03_Recovered.csv", "04_Tested.csv",
				"05_Dropped.csv", "06_Deathrate.csv", "07_NewConfirmed.csv", "08_NewConfirmed3dAv.csv",
				"09_ActiveVariation.csv", "10_ActiveVariation3dAv.csv", "11_NewDeaths.csv", "12_NewDeaths3dAv.csv",
				"13_NewRecovered.csv", "14_NewRecovered3dAv.csv", "15_NewTested.csv", "16_NewTested3dAv.csv",
				"17_PositiveTestsRatio.csv", "18_PositiveTestsRatio3dAv.csv", "19_CumulativePositiveTestsRatio.csv",
				"20_DuplicationTimes.csv", "21_DuplicationTimes3dAv.csv", "22_DeathDuplicationTimes.csv",
				"23_DeathDuplicationTimes3dAv.csv", "24_NewDropped.csv", "25_NewDropped3dAv.csv",
				"26_NewConfirmed5dAv.csv", "27_ActiveVariation5dAv.csv", "28_Newdeaths5dAv.csv", "29_NewRecovered5dAv.csv",
				"30_NewTested5dAv.csv", "31_NewDropped5dAv.csv"]				
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
				"Daily dropped cases trend", "Casos descartados diariamente (3 días)", "New confirmed cases trend (5 days)",
				"Casos diarios (5 días)", "Active cases variation trend (5 days)", "Evolución de casos activos (5 días)",
				"New deaths trend (5 days)", "Fallecimientos diarios (5 días)", "New recovered trend (5 days)",
				"Altas diarias (5 días)", "Daily tests trend (5 days)", "Tests diarios (5 días)",
				"Daily dropped cases trend (5 days)", "Casos descartados diariamente (5 días)"]
plotTitles = ["COVID-19 outbreak in Argentina", "COVID-19: el brote en Argentina", "Total cases", "Totales",
				"New cases trend (3 days average)", "Tendencia diaria (promedio 3 días)", "Deaths", "Fallecimientos",
				"Daily deaths (3 days average)", "Fallecimientos diarios (promedio 3 días)", "Deaths & positive tests ratios",
				"Tasas de mortalidad y tests positivos", "Testing & dropped cases", "Confirmados vs. descartados",
				"Linear duplication times", "Tiempos de duplicación"]
shortLabels = ["Confirmed", "Confirmados", "Active", "Activos", "Deaths", "Fallecimientos", "Death rate",
				"Tasa de mortalidad", "Positive trend", "Positividad (3 días)", "Positive ratio", "Positividad acumulada",
				"Laboratory tests", "Pruebas de diagnóstico", "Dropped cases", "Casos descartados"]
xTitles = ["Time in days", "Tiempo en días"]
yTitles = ["Number of cases", "Número de casos", "Deaths", "Fallecimientos", "Death rate", "Tasa de mortalidad",
			"Laboratory tests", "Pruebas de laboratorio", "Positive tests ratio", "Tasa de positividad",
			"Days needed for\nconfirmed cases to double", "Días necesarios para\nque los casos se dupliquen",
			"Days needed\nfor deaths to double", "Días necesarios para que\nlos fallecimientos se dupliquen"]
tConector = [" since ", " desde ", " after ", " después de ", " (absolute)", " (valores absolutos)",
				" (relative)", " (valores relativos)"]

filePath = "Argentina_Data/processed_data/"
chartPath = "Argentina_Data/actual_charts/"

#Some styling...
defaultFont = "Oswald" #Change this if you don't like it or is not available in your system
legendFont = "Myriad Pro" #Change this to edit legends' font 
colorlist = ["chocolate", "tab:blue", "firebrick", "tab:green", "rebeccapurple", "tab:pink", "olivedrab",
				"crimson", "darkcyan", "aqua", "dodgerblue", "palegreen", "seagreen", "limegreen", "indianred",
				"slategrey", "royalblue", "navy", "slateblue", "goldenrod", "greenyellow", "darkturquoise",
				"coral"] #Default colors for data
backgroundPlot = "silver" #Default background color for charts
backgroundFigure = "lightgrey" #Default background color for figures
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
	if startDate < quarantineStart:
		plt.annotate(tag, fontsize=font, xy=(x, y + yshift),  xycoords='data',
    		xytext=(x, y + ytshift), textcoords='data',
			arrowprops=dict(facecolor='orangered', edgecolor="none", width=w, headwidth=hw, headlength=hl),
        	horizontalalignment='center', verticalalignment='top')

def savePlot(csvName, figure):
	chartName = csvName.split(".")
	plt.savefig(chartPath + chartName[0] + ".png", facecolor=figure.get_facecolor())

def plotbyDate(regions, datatype, xtitle, ytitle, markQ, ticksInterval):
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
		markQuarantine("Social\nisolation", s[1]/25, s[1]/5, 8, quarantineStart, y, 5, 9, 7)
	#Setting up titles	
	plt.title("COVID-19: " + dataTitles[2*(datatype)+lg] + tConector[lg] + startDateTime.strftime(dateFormatString), fontname=defaultFont)
	plt.yscale(plotScale)
	plt.ylabel(ytitle, fontname=legendFont)
	plt.xlabel(xtitle, fontname=legendFont)
	#Setting up grid...
	plt.grid(which='both', axis='both')
	plt.yticks(nu.arange(0, s[1]*1.2, ticksInterval))
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.grid(True, "major", "x", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "x", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	#Setting date format...
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = 1))
	plt.gca().xaxis.set_major_formatter(dateFormat)
	plt.gca().set_facecolor(backgroundPlot)
	#Setting axis labels font and legend
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	if len(regions) > 1:
		plt.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	plt.tight_layout()
	savePlot(fileNames[datatype], figure)
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
def plotbyOutbreak(regions, datatype, dataguide, startpoints, xtitle, ytitle, ticksInterval):
	figure = plt.figure(num=None, figsize=(8, 4), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	period = 0
	#Plotting selected data...
	for i in range(len(regions)):
		datalist = databases[datatype][startPoints[i]:][regions[i]].values.tolist()
		if i == 0:
			period = len(datalist)
		plt.plot(datalist[0:period-1], label=regions[i], linewidth=2.5, color=colorlist[i])
	#Setting up titles
	plt.title("COVID-19: " + dataTitles[2*datatype+lg] + tConector[2 + lg] + str(caseCount) + " " + dataTitles[2*dataguide+lg], fontname=defaultFont)
	plt.yscale(plotScale)
	plt.ylabel(ytitle, fontname=legendFont)
	plt.xlabel(xtitle, fontname=legendFont)
	#Setting up grid...
	plt.grid(which='both', axis='both')
	s = plt.ylim()
	d = plt.xlim()
	plt.yticks(nu.arange(0, s[1]*1.2, ticksInterval))
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.grid(True, "major", "x", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "x", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	#Setting axis labels font and legend
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.gca().set_facecolor(backgroundPlot)
	if len(regions) > 1:
		plt.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	plt.tight_layout()
	savePlot(fileNames[datatype], figure)
	plt.show()

def plotAllCountryData():
	figure = plt.figure(num=None, figsize=(7, 4.5), dpi=imageResolution, facecolor=backgroundFigure, edgecolor='k')
	figure.suptitle(plotTitles[0+lg], fontsize=12, fontname=defaultFont)
	#Setting up totals chart...
	plt.subplot2grid((3, 2), (0, 0))
	x = quarantineStart
	yquarantine = []
	total = databases[0][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*0+lg], color=colorlist[0])
	yquarantine.append(databases[0].loc[x, "ARGENTINA"])
	total = databases[1][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*1+lg], color=colorlist[1])
	yquarantine.append(databases[1].loc[x, "ARGENTINA"])
	total = databases[2][startDate:]["ARGENTINA"].plot(kind="line", linewidth=1.7, label=shortLabels[2*2+lg], color=colorlist[2])
	yquarantine.append(databases[2].loc[x, "ARGENTINA"])
	y = max(yquarantine)
	s = plt.ylim()
	a = plt.xlim()
	markQuarantine("", s[1]/20, s[1]/4.5, 8, x, y, 3, 6, 5)
	total.legend(loc=0, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	total.set_title(plotTitles[2*1+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	ylabels = nu.arange(0, ylimits[1]/1000*1.1, 3).tolist()
	for l in range(len(ylabels)):
		ylabels[l] = "{:.0f}".format(ylabels[l])
		ylabels[l] += "K"
	plt.yticks(nu.arange(0, ylimits[1] * 1.1, 3000), ylabels)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.xlabel("")
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))
	plt.gca().xaxis.set_major_formatter(dateFormat)
	total.set_facecolor(backgroundPlot)
	plt.gca().xaxis.set_ticklabels([])
	#Setting up new daily chart...
	plt.subplot2grid((3, 2), (0, 1))
	yquarantine = []
	newtrend = databases[8][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*0+lg], color=colorlist[0])
	yquarantine.append(databases[8].loc[x, "ARGENTINA"])
	newtrend = databases[10][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*1+lg], color=colorlist[1])
	yquarantine.append(databases[10].loc[x, "ARGENTINA"])
	newtrend = databases[12][startDate:]["ARGENTINA"].plot(kind="line", linewidth=1.7, label=shortLabels[2*2+lg], color=colorlist[2])
	yquarantine.append(databases[12].loc[x, "ARGENTINA"])
	y = max(yquarantine)
	s = plt.ylim()			
	markQuarantine("", s[1]/20, s[1]/4.5, 8, x, y, 3, 6, 5)
	newtrend.legend(loc=0, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	newtrend.set_title(plotTitles[2*2+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.1, 150))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.xlabel("")
	plt.xlim(a[0], a[1])
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))
	plt.gca().xaxis.set_major_formatter(dateFormat)
	newtrend.set_facecolor(backgroundPlot)
	plt.gca().xaxis.set_ticklabels([])
	#Setting up new deaths chart...
	plt.subplot2grid((3, 2), (1, 0))
	newdeaths = databases[12][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*2+lg], color=colorlist[2])
	newdeaths.set_title(plotTitles[2*4+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.1, 5))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.xlabel("")
	plt.xlim(a[0], a[1])
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))
	plt.gca().xaxis.set_major_formatter(dateFormat)
	newdeaths.set_facecolor(backgroundPlot)
	plt.gca().xaxis.set_ticklabels([])
	#Setting up ratios chart...
	plt.subplot2grid((3, 2), (1, 1))
	ratios = databases[19][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*5+lg], color=colorlist[1])
	ratios = databases[18][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*4+lg], color=colorlist[0])
	ratios = databases[6][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*3+lg], color=colorlist[2])
	ratios.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	ratios.set_title(plotTitles[2*5+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.1, 0.1))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.xlabel("")
	plt.xlim(a[0], a[1])
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))
	plt.gca().xaxis.set_major_formatter(dateFormat)
	ratios.set_facecolor(backgroundPlot)
	plt.gca().xaxis.set_ticklabels([])
	#Setting up Tested vs Dropped...
	plt.subplot2grid((3, 2), (2, 0))
	tests = databases[4][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*6+lg], color=colorlist[0])
	tests = databases[5][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*7+lg], color=colorlist[1])
	tests.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	tests.set_title(plotTitles[2*6+lg], fontsize=10, fontname=defaultFont)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	ylabels = nu.arange(0, ylimits[1]/1000*1.1, 30).tolist()
	for l in range(len(ylabels)):
		ylabels[l] = "{:.0f}".format(ylabels[l])
		ylabels[l] += "K"
	plt.yticks(nu.arange(0, ylimits[1] * 1.1, 30000), ylabels)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.xlabel("")
	plt.xlim(a[0], a[1])
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))
	plt.gca().xaxis.set_major_formatter(dateFormat)
	tests.set_facecolor(backgroundPlot)
	#Plotting duplication times...
	plt.subplot2grid((3, 2), (2, 1))
	duplication = databases[23][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*2+lg], color=colorlist[2], zorder=2)
	duplication = databases[21][startDate:]["ARGENTINA"].plot(kind="line", linewidth=2.0, label=shortLabels[2*0+lg], color=colorlist[1], zorder=3)
	duplication.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	plt.fill_between(databases[23][startDate:].index.values, databases[23][startDate:]["ARGENTINA"], 0, facecolor=colorlist[2],
					alpha=0.5, zorder=2)
	plt.fill_between(databases[21][startDate:].index.values, databases[21][startDate:]["ARGENTINA"], 0, facecolor=colorlist[1],
					alpha=0.5, zorder=3)
	duplication.set_title(plotTitles[2*7+lg], fontsize=10, fontname=defaultFont)
	plt.ylabel("")
	plt.xlabel("")
	plt.xlim(a[0], a[1])
	plt.grid(which='both', axis='both')
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.1, 15))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = 2))
	plt.gca().xaxis.set_major_formatter(dateFormat)
	duplication.set_facecolor(backgroundPlot)
	plt.tight_layout(rect=[0, 0.03, 1, 0.95])
	savePlot("Argentina.csv", figure)
	plt.show()
	
def plotAllCountryDT():
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
	plt.grid(which='both', axis='both')
	plt.yticks(nu.arange(0, s[1] * 1.1, 10))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.grid(True, "major", "x", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "x", ls="--", lw=0.3, c="black", alpha=0.5)
	#Setting date format...
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = 1))
	plt.gca().xaxis.set_major_formatter(dateFormat)
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
	plt.grid(which='both', axis='both')
	plt.yticks(nu.arange(0, s[1] * 1.1, 10))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.grid(True, "major", "x", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "x", ls="--", lw=0.3, c="black", alpha=0.5)
	#Setting date format...
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = 1))
	plt.gca().xaxis.set_major_formatter(dateFormat)
	plt.tight_layout()
	savePlot("ArgentinaDT.csv", figure)
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

def plotWeeklyCases(weeklyConfirmed, weeklyDeaths, yTitleC, yTitleD, region, aType, saveChart):
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
	if saveChart == True:
		savePlot(region + "_WA.csv", figure)
	plt.show()

def plotWeeklyAnalysis(weeklyConfirmed, weeklyDeaths, yTitleC, yTitleD, aType, regions, saveChart):
	for d in range(len(regions)):
		plotWeeklyCases(weeklyConfirmed[d], weeklyDeaths[d], yTitleC, yTitleD, regions[d], aType, saveChart)

#Calling the functions to build selected charts...
if confirmedByDate == True:
	print("Plotting confirmed cases data by date...", end="\n")
	plotbyDate(regions, 0, xTitles[0+lg], yTitles[0+lg], True, 1000)
if deathsByDate == True:
	print("Plotting deaths cases data by date...", end="\n")
	plotbyDate(regions, 2, xTitles[0+lg], yTitles[2+lg], True, 50)
if confirmedByOutbreak == True:
	print("Plotting confirmed cases data by outbreak...", end="\n")
	plotbyOutbreak(regions, 0, dataGuide, startPoints, xTitles[0+lg], yTitles[0+lg], 1000)
if deathsByOutbreak == True:
	print("Plotting deaths data by outbreak...", end="\n")
	plotbyOutbreak(regions, 2, dataGuide, startPoints, xTitles[0+lg], yTitles[2+lg], 50)
if newConfirmedCases == True:
	print("Plotting daily confirmed cases data...", end="\n")
	plotbyDate(regions, 7, xTitles[0+lg], yTitles[0+lg], True, 100)
if newConfirmedCasesTrend == True:
	print("Plotting daily confirmed cases trend data...", end="\n")
	plotbyDate(regions, 8, xTitles[0+lg], yTitles[0+lg], True, 100)
if newConfirmedCasesTrend5 == True:
	print("Plotting daily confirmed cases trend data...", end="\n")
	plotbyDate(regions, 26, xTitles[0+lg], yTitles[0+lg], True, 100)
if newDeaths == True:
	print("Plotting daily deaths cases data...", end="\n")
	plotbyDate(regions, 11, xTitles[0+lg], yTitles[2+lg], True, 5)
if newDeathsTrend == True:
	print("Plotting daily deahts trend...", end="\n")
	plotbyDate(regions, 12, xTitles[0+lg], yTitles[2+lg], True, 5)
if newDeathsTrend5 == True:
	print("Plotting daily deahts trend...", end="\n")
	plotbyDate(regions, 28, xTitles[0+lg], yTitles[2+lg], True, 5)
if deathRate == True:
	print("Plotting death rate evolution...", end="\n")
	plotbyDate(regions, 6, xTitles[0+lg], yTitles[4+lg], False, 0.02)
if confirmedDuplication == True:
	print("Plotting confirmed cases duplications times by date...", end="\n")
	plotbyDate(regions, 20, xTitles[0+lg], yTitles[10+lg], False, 15)
if confirmedDuplicationTrend == True:
	print("Plotting confirmed cases duplications times trend by date...", end="\n")
	plotbyDate(regions, 21, xTitles[0+lg], yTitles[10+lg], False, 15)
if deathsDuplication == True:
	print("Plotting confirmed cases duplications times by date...", end="\n")
	plotbyDate(regions, 22, xTitles[0+lg], yTitles[12+lg], False, 25)
if deathsDuplicationTrend == True:
	print("Plotting confirmed cases duplications times by date...", end="\n")
	plotbyDate(regions, 23, xTitles[0+lg], yTitles[12+lg], False, 25)
weeklyConfirmed = []
weeklyDeaths = []
weeklyConfirmedR = []
weeklyDeaths = []
if weeklyAnalysis == True or weeklyAnalysisAC == True:
	print("Ordening data by day of the week", end="\n")
	weeklyConfirmed = buildWeeklyData(regions, 7)
	weeklyDeaths = buildWeeklyData(regions, 11)
	weeklyConfirmedR = buildWeeklyDataR(weeklyConfirmed)
	weeklyDeathsR = buildWeeklyDataR(weeklyDeaths)
if weeklyAnalysis == True:
	if weeklyAnalysisType == "both":
		print("Plotting week analysis (absolute and relative)", end="\n")
		plotWeeklyAnalysis(weeklyConfirmed, weeklyDeaths, yTitles[0+lg], yTitles[2+lg], tConector[4+lg], regions, False)
		plotWeeklyAnalysis(weeklyConfirmedR, weeklyDeathsR, yTitles[0+lg], yTitles[2+lg], tConector[6+lg], regions, False)
	elif weeklyAnalysisType == "relative":
		print("Plotting week analysis (relative)", end="\n")
		plotWeeklyAnalysis(weeklyConfirmedR, weeklyDeathsR, yTitles[0+lg], yTitles[2+lg], tConector[6+lg], regions, False)		
	elif weeklyAnalysisType == "absolute":
		print("Plotting week analysis (absolute)", end="\n")
		plotWeeklyAnalysis(weeklyConfirmed, weeklyDeaths, yTitles[0+lg], yTitles[2+lg], tConector[4+lg], regions, False)
if plotAllCountry == True:
	plotAllCountryData()
	if duplicationTimesAC == True:
		plotAllCountryDT()
	if weeklyAnalysisAC == True:
		if weeklyAnalysisType == "both":
			print("Plotting week analysis for Argentina (absolute and relative)", end="\n")
			plotWeeklyAnalysis(weeklyConfirmed, weeklyDeaths, yTitles[0+lg], yTitles[2+lg], tConector[4+lg], ["ARGENTINA"], True)
			plotWeeklyAnalysis(weeklyConfirmedR, weeklyDeathsR, yTitles[0+lg], yTitles[2+lg], tConector[6+lg], ["ARGENTINA"], True)
		elif weeklyAnalysisType == "relative":
			print("Plotting week analysis for Argentina (relative)", end="\n")
			plotWeeklyAnalysis(weeklyConfirmedR, weeklyDeathsR, yTitles[0+lg], yTitles[2+lg], tConector[6+lg], ["ARGENTINA"], True)		
		elif weeklyAnalysisType == "absolute":
			print("Plotting week analysis for Argentina (absolute)", end="\n")
			plotWeeklyAnalysis(weeklyConfirmed, weeklyDeaths, yTitles[0+lg], yTitles[2+lg], tConector[4+lg], ["ARGENTINA"], True)

#Saying good bye...
print("That's all. If you want more plots, edit the code and run again.                          ", end="\n")