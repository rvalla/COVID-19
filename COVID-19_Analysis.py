from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator
import numpy as nu
import pandas as pd

#Selecting data: "Confirmed", "Deaths" or "Recovered"
dataSelection = ["confirmed_global", "deaths_global"]
fileNamePrefix = "time_series_covid19_"
fileExtension = ".csv"
fileNames = []
fileCompletePaths = []
for i in range(len(dataSelection)):
	fileNames.append(fileNamePrefix + dataSelection[i] + fileExtension)
	fileCompletePaths.append("COVID-19/csse_covid_19_data/csse_covid_19_time_series/" + fileNames[i])

#Selecting plot scale: "linear" or "log"
plotScale = "linear"

#Selecting regions to study
#Note that the first one will be used as reference to decide periods of time to plot
regions = ["Italy", "Spain", "Germany"]
regionsIndexes = [[],[]]
groupbyCountry = False
#You can choose 'Country/Region' or 'Province/State'. Select regions correctly though...
#If you choose 'Province/State' then 'groupbyCountry' must be False
regionReference = "Country/Region"

#Selecting data to display
startDate = "1/22/20" #Starting point for plotbyDate. Default: 1/22/20
caseCount = 1 #Starting point for plotbyOutbreak (number of confirmed cases)
outbreakDayCount = 0 #Number of days after caseCount condition is fulfiled
dataType = 0 #0 = Confirmed, 1 = Deaths, 2 = Recovered

#Loading data...
databases = []
for i in range(len(fileCompletePaths)):
	databases.append(pd.read_csv(fileCompletePaths[i]))
	databases[i] = databases[i].T

#Function to look for selected regions in Data Frame
def getRegionsIndexes(regions):
	indexes = [[] for c in range (len(dataSelection))]
	for d in range(len(dataSelection)):
		for i in range(len(regions)):
			for e in range(databases[d].shape[1]):
				if databases[d].loc[regionReference, e] == regions[i]:
					indexes[d].append(e)
					break
	return indexes

regionsIndexes = getRegionsIndexes(regions)

#Grouping data by country if needed (sum added at the end of the Data Frame)
if groupbyCountry == True:
	for d in range(len(dataSelection)):
		for r in range(len(regions)):
			ls = []
			for i in range(databases[d].shape[1]):
				if databases[d].loc[regionReference, i] == regions[r]:
					ls.append(i)
			databases[d][databases[d].shape[1]] = databases[d][:][ls].sum(axis=1)
			print(databases[d].shape[1])
			regionsIndexes[d][r] = databases[d].shape[1] - 1

#Function to plot cases for regions by date. Use 0, 1 or 2 to select Confirmed, Deaths or Recovered
def plotbyDate(datalocation, datatype):
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(datalocation[datatype])):
		databases[datatype][startDate:][datalocation[datatype][i]].plot(kind='line', label=regions[i], linewidth=2.5)
	plt.title("COVID-19: " + dataSelection[datatype] + " cases since " + startDate)
	plt.legend()
	plt.grid(which='both', axis='both')
	plt.yscale(plotScale)
	plt.ylabel("Number of cases")
	plt.xlabel("Time in days")
	plt.tight_layout()
	plt.show()

#Function to look for first case in each region
def regionsStartPoints(regions):
	startPoints = [[] for c in range(len(dataSelection))]
	for d in range(len(dataSelection)):
		for i in range(len(regions)):
			for e in range(databases[d].shape[0]-4):
				if databases[d].iloc[4 + e, regionsIndexes[d][i]] >= caseCount:
					startPoints[d].append(e + 4)
					print(e + 4)
					break
	return startPoints

#Function to plot cases for regions since first case
def plotbyOutbreak(datalocation, datatype):
	startPoints = regionsStartPoints(regions)
	period = databases[datatype].shape[0] - startPoints[datatype][0] - outbreakDayCount
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(datalocation[datatype])):
		startPoint = startPoints[datatype][i] + outbreakDayCount
		datalist = databases[datatype][startPoint:startPoint + period][regionsIndexes[datatype][i]].values.tolist()
		plt.plot(datalist, label=regions[i], linewidth=2.5)

	plt.title("COVID-19: " + dataSelection[datatype] + " cases since number " + str(caseCount))
	plt.legend()	
	plt.grid()
	plt.ylabel("Number of cases")
	plt.xlabel("Time in days")
	plt.yscale(plotScale)
	plt.tight_layout()
	plt.show()

def getDeathRates(datalocation):
	deathRates = [[] for c in range(len(regions))]
	for r in range(len(regions)):
		confirmed = databases[0][startDate:][datalocation[0][r]].values.tolist()
		deaths = databases[1][startDate:][datalocation[1][r]].values.tolist()
		for d in range(len(confirmed)):
			if confirmed[d] > 0:
				deathRates[r].append(deaths[d]/confirmed[d])
			else:
				deathRates[r].append(0)
	return deathRates
	
def plotDeathRate(datalocation):
	deathRates = getDeathRates(regionsIndexes)
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(regions)):
		plt.plot(deathRates[i], label=regions[i], linewidth=2.5)
	plt.title("COVID-19: Death rate evolution since " + startDate)
	plt.legend()
	plt.grid(which='both', axis='both')
	plt.yscale(plotScale)
	plt.ylabel("Death ratio")
	plt.xlabel("Time in days")
	plt.tight_layout()
	plt.show()

	
plotbyDate(regionsIndexes, dataType)
plotbyOutbreak(regionsIndexes, dataType)
plotDeathRate(regionsIndexes)