from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import matplotlib.ticker as tk
import matplotlib.dates as mdates
import numpy as nu
import pandas as pd

print("###############################################")
print("      Visualization of COVID-19 Outbreak")
print("-----------------------------------------------")
print("https://github.com/rvalla/COVID-19")
print("Data loaded from official national datasets")
print("https://datos.gob.ar/dataset?q=covid")
print("-----------------------------------------------")
print()

#Selecting data: "Confirmed", "Deaths" or "Recovered"
#regions = ["CABA", "Buenos Aires", "Santa Fe", "Córdoba", "Río Negro", "Chubut"]
regions = ["CABA", "Buenos Aires"]

fileName = "Covid19Determinaciones.csv"
fileCompletePath = "Argentina_Data/datos.gob.ar/" + fileName
chartPath = "Argentina_Data/actual_charts/"
colorlist = ["orange", "tab:blue", "tab:red", "tab:green"]

dataStartDate = "2020-02-11"
dataEndDate = "2020-06-05"
wantedStartDate = "2020-03-17"
wantedEndDate = "2020-06-01"
dataPeriod = pd.date_range(dataStartDate, dataEndDate)
plotScale = "linear"

#Deciding language for titles and tags...
lg = 0 # 0 for english, 1 for spanish

#Deciding what to plot...
plotByRegions = True
plotCumulative = True
plotInfectedRatio = True
plotCumulativeRatio = True
plotPositives = True
plotCumulativePositives = True

#Loading data by province...
databases = []
cumulative_databases = []
dataframe = pd.read_csv(fileCompletePath)
del dataframe["codigo_indec_provincia"]
del dataframe["codigo_indec_departamento"]
del dataframe["localidad"]
del dataframe["codigo_indec_localidad"]
del dataframe["origen_de_financiamiento"]
del dataframe["tipo"]
del dataframe["ultima_actualizacion"]

print("Loading dataset...", end= "\r")

for r in range(len(regions)):
	databases.append(dataframe[dataframe["provincia"] == regions[r]])
	databases[r].reset_index(drop=True, inplace=True)
del dataframe

for r in range(len(regions)):
	row = 0
	rowcount = databases[r].shape[0]
	province = databases[r]["provincia"][row]
	print("Processing data for " + province + "...      ", end= "\r")
	while row < rowcount:
		date = databases[r]["fecha"][row]
		newrow = databases[r].shape[0]
		databases[r].loc[newrow,:] = databases[r].loc[databases[r]["fecha"] == date].sum(axis=0)
		databases[r].loc[newrow,"fecha"] = date
		databases[r].loc[newrow,"provincia"] = province
		databases[r].loc[newrow,"departamento"] = province
		while date == databases[r]["fecha"][row]:
			row += 1
	databases[r] = databases[r][databases[r]["departamento"] == province]
	databases[r].set_index("fecha", inplace=True)
	del databases[r]["provincia"]
	del databases[r]["departamento"]
	databases[r].index = pd.DatetimeIndex(databases[r].index)
	databases[r] = databases[r].reindex(dataPeriod, fill_value=0)
	databases[r].index = pd.DatetimeIndex(databases[r].index)
	cumulative_databases.append(databases[r].cumsum())
	databases[r].loc[:,"ratio"] = databases[r][:]["positivos"].div(databases[r][:]["total"])
	databases[r]["ratio"].fillna(0, inplace=True)
	cumulative_databases[r].index = pd.DatetimeIndex(cumulative_databases[r].index)
	cumulative_databases[r].loc[:,"ratio"] = cumulative_databases[r][:]["positivos"].div(cumulative_databases[r][:]["total"])
	cumulative_databases[r]["ratio"].fillna(0, inplace=True)

print("The data is ready!                             ", end= "\n")

#Some styling...
defaultFont = "Oswald" #Change this if you don't like it or is not available in your system
legendFont = "Myriad Pro" #Change this to edit legends' font 
backgroundPlot = "silver" #Default background color for charts
backgroundFigure = "lightgrey" #Default background color for figures
majorGridColor = "dimgrey" #Default colors for grids...
minorGridColor = "dimgray"
alphaMGC = 0.7
alphamGC = 0.9
imageResolution = 150

dateFormat = mdates.DateFormatter('%b %d')
dateFormatString = "%B %d"	
if lg ==1:
	dateFormat = mdates.DateFormatter('%d/%m')
	dateFormatString = "%d/%m"

titleprefix = "Argentina COVID-19: "
ptitles = ["Daily tests by region", "Testeos diarios por provincia", "Cumulative tests by region",
			"Testeos acumulados por provincia", "Daily positive tests ratio", "Tasa de positividad diaria",
			"Cumulative positive tests ratio", "Tasa de positividad acumulada", "Daily positive tests",
			"Testeos positivos diarios", "Cumulative positive tests", "Testeos positivos acumulados"]
xtitles = ["Time in days", "Tiempo en días"]
ytitles = ["Number of tests", "Cantidad de tests", "Positive tests ratio", "Tasa de positividad",
			"Positive tests", "Tests positivos"]

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

def gridAndTicks(yMax, ticksinterval):
	plt.grid(which='both', axis='both')
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.grid(True, "major", "x", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "x", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.xticks(fontsize=7)
	plt.yticks(fontsize=7)
	plt.yticks(nu.arange(0, yMax, ticksinterval))
	plt.gca().set_facecolor(backgroundPlot)

def ticksLocator(weekInterval):
	plt.gca().xaxis.set_minor_locator(tk.AutoMinorLocator(7))
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = weekInterval))
	plt.gca().xaxis.set_major_formatter(dateFormat)

def plotData(datatoplot, tag, ptitle, xtitle, ytitle, ticksinterval):
	figure(num=None, figsize=(8, 4), dpi=150, facecolor=backgroundFigure, edgecolor='k')
	for i in range(len(datatoplot)):
		datatoplot[i][wantedStartDate:wantedEndDate][tag].plot(kind='line', label=regions[i], linewidth=2.0)
	plt.title(ptitle, fontname=defaultFont)
	
	s = plt.ylim()
	plt.ylabel(ytitle, fontname=legendFont)
	plt.xlabel(xtitle, fontname=legendFont)
	gridAndTicks(s[1]*1.1, ticksinterval)
	ticksLocator(1)
	plt.yscale(plotScale)
	plt.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	plt.tight_layout()
	plt.show()

if plotByRegions == True:
	print("Plotting tests data by date...", end="\n")
	plotData(databases, "total", ptitles[0+lg], xtitles[0+lg], ytitles[0+lg], 500)
if plotCumulative == True:
	print("Plotting cummulative tests since date...", end="\n")
	plotData(cumulative_databases, "total", ptitles[2+lg], xtitles[0+lg], ytitles[0+lg], 3000)
if plotInfectedRatio == True:
	print("Plotting positive tests ratio since date...", end="\n")
	plotData(databases, "ratio", ptitles[4+lg], xtitles[0+lg], ytitles[2+lg], 0.25)
if plotCumulativeRatio == True:
	print("Plotting cumularive positive tests ratio since date...", end="\n")
	plotData(cumulative_databases, "ratio", ptitles[6+lg], xtitles[0+lg], ytitles[2+lg], 0.25)
if plotPositives == True:
	print("Plotting cumularive positive tests ratio since date...", end="\n")
	plotData(databases, "positivos", ptitles[8+lg], xtitles[0+lg], ytitles[4+lg], 100)
if plotCumulativePositives == True:
	print("Plotting cumularive positive tests ratio since date...", end="\n")
	plotData(cumulative_databases, "positivos", ptitles[8+lg], xtitles[0+lg], ytitles[4+lg], 500)

print("That's all. If you want more plots, edit the code and run again.                          ", end="\n")