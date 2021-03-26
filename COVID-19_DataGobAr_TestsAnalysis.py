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

regions = ["CABA", "Buenos Aires", "Córdoba", "Santa Fe"]

fileName = "Covid19Determinaciones.csv"
fileCompletePath = "Argentina_Data/datos.gob.ar/" + fileName
chartPath = "Argentina_Data/actual_charts/testing/"
colorlist = ["orange", "tab:blue", "tab:red", "tab:green"]

dataStartDate = "2020-02-11"
dataEndDate = "2021-03-25"
wantedStartDate = "2020-09-01"
wantedEndDate = "2021-03-15"
dataPeriod = pd.date_range(dataStartDate, dataEndDate)
plotScale = "linear"

#Deciding language for titles and tags...
lg = 0 # 0 for english, 1 for spanish
ticksSizes = [1500, 250000, 0.1, 100000]

#Deciding if you want to save and show charts...
saveChart = True
showChart = False

#Deciding what to plot...
plotByRegions = True
plotCumulative = True
plotInfectedRatio = True
plotCumulativeRatio = True
plotPositives = True
plotCumulativePositives = True
plotTestAndRatio = True

#Loading data by province...
databases = []
cumulative_databases = []
dataframe = pd.read_csv(fileCompletePath)
del dataframe["codigo_indec_provincia"]
del dataframe["codigo_indec_departamento"]
del dataframe["localidad"]
del dataframe["codigo_indec_localidad"]
del dataframe["origen_financiamiento"]
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
	databases[r].loc[:,"ratio"] = databases[r][:]["positivos"].div(databases[r][:]["total"])
	databases[r]["ratio"].fillna(0, inplace=True)
	for d in range(databases[r].shape[0] - 6):
			d0 = databases[r].loc[databases[r].index[d], "total"]
			d1 = databases[r].loc[databases[r].index[d+1], "total"]
			d2 = databases[r].loc[databases[r].index[d+2], "total"]
			d3 = databases[r].loc[databases[r].index[d+3], "total"]
			d4 = databases[r].loc[databases[r].index[d+4], "total"]
			d5 = databases[r].loc[databases[r].index[d+5], "total"]
			d6 = databases[r].loc[databases[r].index[d+6], "total"]
			databases[r].loc[databases[r].index[d+3], "total7d"] = (d0 + d1+ d2 + d3 + d4 + d5 + d6) / 7
			d0 = databases[r].loc[databases[r].index[d], "positivos"]
			d1 = databases[r].loc[databases[r].index[d+1], "positivos"]
			d2 = databases[r].loc[databases[r].index[d+2], "positivos"]
			d3 = databases[r].loc[databases[r].index[d+3], "positivos"]
			d4 = databases[r].loc[databases[r].index[d+4], "positivos"]
			d5 = databases[r].loc[databases[r].index[d+5], "positivos"]
			d6 = databases[r].loc[databases[r].index[d+6], "positivos"]
			databases[r].loc[databases[r].index[d+3], "positivos7d"] = (d0 + d1+ d2 + d3 + d4 + d5 + d6) / 7
	databases[r].loc[:,"ratio7d"] = databases[r][:]["positivos7d"].div(databases[r][:]["total7d"])
	cumulative_databases.append(databases[r].cumsum())
	cumulative_databases[r].index = pd.DatetimeIndex(cumulative_databases[r].index)
	cumulative_databases[r].loc[:,"ratio"] = cumulative_databases[r][:]["positivos"].div(cumulative_databases[r][:]["total"])
	cumulative_databases[r]["ratio"].fillna(0, inplace=True)

print("The data is ready!                             ", end= "\n")

#Some styling...
defaultFont = "Oswald" #Change this if you don't like it or is not available in your system
legendFont = "Myriad Pro" #Change this to edit legends' font
backgroundPlot = "silver" #Default background color for charts
backgroundFigure = "white" #Default background color for figures
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
ptitles = ["Daily tests by region (7 days)", "Testeos diarios por provincia (7 días)", "Cumulative tests by region",
			"Testeos acumulados por provincia", "Daily positive tests ratio (7 days)", "Tasa de positividad diaria (7 días)",
			"Cumulative positive tests ratio", "Tasa de positividad acumulada", "Daily positive tests (7 days)",
			"Testeos positivos diarios (7 días)", "Cumulative positive tests", "Testeos positivos acumulados"]
filenames = ["T_00_dailytests", "T_01_cumulativetests", "T_02_dailypositiveratio", "T_03_positiveratio",
			"T_04_dailypositives", "T_05_cumulativepositives", "T_06_dailytestAndratio"]
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

def savePlot(csvname, figure):
	plt.savefig(chartPath + str(lg) + "_" + csvname + ".png", facecolor=figure.get_facecolor())

def gridAndTicks(yMax, ticksinterval):
	plt.grid(which='both', axis='both')
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.grid(True, "major", "x", ls="-", lw=0.8, c=majorGridColor, alpha=alphaMGC)
	plt.grid(True, "minor", "x", ls="--", lw=0.3, c=minorGridColor, alpha=alphamGC)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.yticks(nu.arange(0, yMax, ticksinterval))
	plt.gca().set_facecolor(backgroundPlot)

def ticksLocator(weekInterval):
	plt.gca().xaxis.set_minor_locator(tk.AutoMinorLocator(7))
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = weekInterval))
	plt.gca().xaxis.set_major_formatter(dateFormat)
	plt.gca().xaxis.set_minor_formatter(tk.NullFormatter())

def plotData(datatoplot, tag, ptitle, xtitle, ytitle, ticksinterval, savechart, show, csvname):
	figure = plt.figure(num=None, figsize=(6, 4), dpi=150, facecolor=backgroundFigure, edgecolor='k')
	for i in range(len(datatoplot)):
		datatoplot[i][wantedStartDate:wantedEndDate][tag].plot(kind='line', label=regions[i], linewidth=2.0)
	plt.title(ptitle, fontname=defaultFont)
	s = plt.ylim()
	plt.yscale(plotScale)
	plt.ylabel(ytitle, fontname=legendFont)
	plt.xlabel(xtitle, fontname=legendFont)
	gridAndTicks(s[1]*1.1, ticksinterval)
	ticksLocator(2)
	plt.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	plt.tight_layout()
	if savechart == True:
		savePlot(csvname, figure)
	if show == True:
		plt.show()

def plotDoubleData(datatoplot, tagA, tagB, ptitle, xtitle, ytitle, ticksintervalA, ticksintervalB, savechart, show, csvname):
	figure = plt.figure(num=None, figsize=(5, 4.5), dpi=150, facecolor=backgroundFigure, edgecolor='k')
	dataA = plt.subplot2grid((2, 1), (0, 0))
	for i in range(len(datatoplot)):
		dataA = datatoplot[i][wantedStartDate:wantedEndDate][tagA].plot(kind='line', label=regions[i], linewidth=2.0)
	dataA.set_title(ptitle[0], fontname=defaultFont)
	s = plt.ylim()
	dataA.set_yscale(plotScale)
	dataA.set_ylabel(ytitle[0], fontname=legendFont)
	dataA.set_xlabel("")
	gridAndTicks(s[1]*1.1, ticksintervalA)
	ticksLocator(2)
	plt.legend(loc=2, shadow = True, facecolor = backgroundFigure, prop={'family' : legendFont, 'size' : 7})
	dataB = plt.subplot2grid((2, 1), (1, 0))
	for i in range(len(datatoplot)):
		dataB = datatoplot[i][wantedStartDate:wantedEndDate][tagB].plot(kind='line', label=regions[i], linewidth=2.0)
	dataB.set_title(ptitle[1], fontname=defaultFont)
	s = plt.ylim()
	dataB.set_yscale(plotScale)
	dataB.set_ylabel(ytitle[1], fontname=legendFont)
	dataB.set_xlabel(xtitle, fontname=legendFont)
	gridAndTicks(s[1]*1.1, ticksintervalB)
	ticksLocator(2)
	plt.tight_layout(rect=[0, 0, 1, 1])
	if savechart == True:
		savePlot(csvname, figure)
	if show == True:
		plt.show()

if plotByRegions == True:
	print("Plotting tests data by date...", end="\n")
	plotData(databases, "total7d", ptitles[0+lg], xtitles[0+lg], ytitles[0+lg], ticksSizes[0], saveChart, showChart, filenames[0])
if plotCumulative == True:
	print("Plotting cummulative tests since date...", end="\n")
	plotData(cumulative_databases, "total", ptitles[2+lg], xtitles[0+lg], ytitles[0+lg], ticksSizes[1], saveChart, showChart, filenames[1])
if plotInfectedRatio == True:
	print("Plotting positive tests ratio since date...", end="\n")
	plotData(databases, "ratio7d", ptitles[4+lg], xtitles[0+lg], ytitles[2+lg], ticksSizes[2], saveChart, showChart, filenames[2])
if plotCumulativeRatio == True:
	print("Plotting cummulative positive tests ratio since date...", end="\n")
	plotData(cumulative_databases, "ratio", ptitles[6+lg], xtitles[0+lg], ytitles[2+lg], ticksSizes[2], saveChart, showChart, filenames[3])
if plotPositives == True:
	print("Plotting cummulative positive tests ratio since date...", end="\n")
	plotData(databases, "positivos7d", ptitles[8+lg], xtitles[0+lg], ytitles[4+lg], ticksSizes[0], saveChart, showChart, filenames[4])
if plotCumulativePositives == True:
	print("Plotting cummulative positive tests ratio since date...", end="\n")
	plotData(cumulative_databases, "positivos", ptitles[10+lg], xtitles[0+lg], ytitles[4+lg], ticksSizes[3], saveChart, showChart, filenames[5])
if plotTestAndRatio == True:
	plotDoubleData(databases, "total7d", "ratio7d", [ptitles[0+lg],ptitles[4+lg]], xtitles[0+lg], ["",""], \
					2.5*ticksSizes[0], ticksSizes[2],  saveChart, showChart, filenames[6])

print("That's all. If you want more plots, edit the code and run again.                          ", end="\n")
