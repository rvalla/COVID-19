from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator
import numpy as nu
import pandas as pd

print("###########################################")
print("    Visualization of COVID-19 Outbreak")
print("-------------------------------------------")
print("https://github.com/rvalla/COVID-19")
print("Data from John Hopkins University:")
print("https://github.com/CSSEGISandData/COVID-19")
print("------------------------------------------")
print()
print("Ploting data of ", end=" ")

#Selecting data: "Confirmed", "Deaths" or "Recovered"
dataSelection = ["confirmed_global", "deaths_global", "recovered_global"]
dataTitles = ["Confirmed", "Deaths", "Recovered"]
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
regions = ["Argentina", "Chile", "Uruguay", "Colombia", "Ecuador"]
regionsIndexes = [[],[]]
groupbyCountry = True
#You can choose 'Country/Region' or 'Province/State'. Select regions correctly though...
#If you choose 'Province/State' then 'groupbyCountry' must be False
regionReference = "Country/Region"

#Selecting data to display
startDate = "3/1/20" #Starting point for plotbyDate. Default: 1/22/20
caseCount = 200 #Starting point for plotbyOutbreak (number of confirmed cases)
outbreakDayCount = 0 #Number of days after caseCount condition is fulfiled
dataType = 0 #0 = Confirmed, 1 = Deaths, 2 = Recovered
dataGuide = 0 #Data type to calculate startpoints (confirmed, deaths, recovered)

#Printing selected regions to console
print(regions, end="\r")

#Loading data...
databases = []

for i in range(len(fileCompletePaths)):
	databases.append(pd.read_csv(fileCompletePaths[i]))
	if regionReference == "Country/Region":
		del	databases[i]["Province/State"]
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
			regionsIndexes[d][r] = databases[d].shape[1] - 1

#Function to plot cases for regions by date. Use 0, 1 or 2 to select Confirmed, Deaths or Recovered
def plotbyDate(datalocation, datatype):
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(datalocation[datatype])):
		databases[datatype][startDate:][datalocation[datatype][i]].plot(kind='line', label=regions[i], linewidth=2.5)
	plt.title("COVID-19: " + dataTitles[datatype] + " cases since " + startDate)
	plt.legend(loc=0, prop={'size': 8})
	plt.grid(which='both', axis='both')
	plt.yscale(plotScale)
	plt.ylabel("Number of cases")
	plt.xlabel("Time in days")
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
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
					break
	return startPoints

#Function to plot cases for regions since first case
def plotbyOutbreak(datalocation, datatype, dataguide):
	startPoints = regionsStartPoints(regions)
	period = databases[datatype].shape[0] - startPoints[dataguide][0] - outbreakDayCount
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(datalocation[datatype])):
		startPoint = startPoints[dataguide][i] + outbreakDayCount
		datalist = databases[datatype][startPoint:startPoint + period][regionsIndexes[datatype][i]].values.tolist()
		plt.plot(datalist, label=regions[i], linewidth=2.5)

	plt.title("COVID-19: " + dataTitles[datatype] + " cases since number " + str(caseCount) + " " + dataTitles[dataguide])
	plt.legend(loc=0, prop={'size': 8})	
	plt.grid()
	plt.ylabel("Number of cases")
	plt.xlabel("Time in days")
	plt.yscale(plotScale)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
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
	plt.legend(loc=0, prop={'size': 8})
	plt.grid(which='both', axis='both')
	plt.yscale(plotScale)
	plt.ylabel("Death ratio")
	plt.xlabel("Time in days")
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.tight_layout()
	plt.show()

def getNewCases(datalist):
	ls = []
	ls.append(datalist[0])
	for e in range(len(datalist) - 1):
		ls.append(datalist[e+1] - datalist[e])
	return ls

def getNewCasesAv(datalist):
	ls = []
	ls.append((datalist[0] + datalist[1])/2)
	for e in range(len(datalist) - 2):
		ls.append((datalist[e+2] + datalist[e+1] + datalist[e])/3)
	index = len(datalist)
	ls.append((datalist[index-1]+datalist[index-2])/2)
	return ls

def plotNewCases(datalocation, datatype, dataguide):
	startPoints = regionsStartPoints(regions)
	period = databases[datatype].shape[0] - startPoints[datatype][0] - outbreakDayCount
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(datalocation[datatype])):
		startPoint = startPoints[dataguide][i] + outbreakDayCount
		datalist = databases[datatype][startPoint:startPoint + period][regionsIndexes[datatype][i]].values.tolist()
		datalistsub = getNewCases(datalist)
		plt.plot(datalistsub, label=regions[i], linewidth=2.5)
	plt.title("COVID-19: New " + dataTitles[datatype] + " cases since number " + str(caseCount) + " " + dataTitles[dataguide])
	plt.legend(loc=0, prop={'size': 8})	
	plt.grid()
	plt.ylabel("Number of new cases")
	plt.xlabel("Time in days")
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.yscale(plotScale)
	plt.tight_layout()
	plt.show()

def plotNewCases3Av(datalocation, datatype, dataguide):
	startPoints = regionsStartPoints(regions)
	period = databases[datatype].shape[0] - startPoints[datatype][0] - outbreakDayCount
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(datalocation[datatype])):
		startPoint = startPoints[dataguide][i] + outbreakDayCount
		datalist = databases[datatype][startPoint:startPoint + period][regionsIndexes[datatype][i]].values.tolist()
		datalistsub = getNewCasesAv(getNewCases(datalist))
		plt.plot(datalistsub, label=regions[i], linewidth=2.5)
	plt.title("COVID-19: New " + dataTitles[datatype] + " cases trend since number " + str(caseCount) + " " + dataTitles[dataguide])
	plt.legend(loc=0, prop={'size': 8})	
	plt.grid()
	plt.ylabel("Average of new cases (3 days)")
	plt.xlabel("Time in days")
	plt.yscale(plotScale)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.tight_layout()
	plt.show()

def getDuplicationTimes(datalist, type):
	newcases = getNewCases(datalist)
	duplicationtimes = []
	if type == "average":
		newcases = getNewCasesAv(newcases)
	for e in range(len(datalist)-1):
		if newcases[e+1] > 0:
			duplicationtimes.append(datalist[e]/newcases[e+1])
		else:
			duplicationtimes.append(0)
	return duplicationtimes

def plotDuplicationTimes(datalocation, datatype, dataguide):
	startPoints = regionsStartPoints(regions)
	period = databases[datatype].shape[0] - startPoints[datatype][0] - outbreakDayCount
	figure = plt.figure(num=None, figsize=(7, 4), dpi=150, facecolor='w', edgecolor='k')
	plt.subplot2grid((2, 1), (0, 0))
	for i in range(len(datalocation[datatype])):
		startPoint = startPoints[dataguide][i] + outbreakDayCount
		datalist = databases[datatype][startPoint:startPoint + period][regionsIndexes[datatype][i]].values.tolist()
		duplicationtimes = getDuplicationTimes(datalist, " ")
		plt.plot(duplicationtimes, label=regions[i], linewidth=2.0)
	plt.title("Duplication speed in days for " + dataTitles[datatype] + " cases since number " + str(caseCount) + " " + dataTitles[dataguide], fontsize=11)
	plt.legend(loc=2, prop={'size': 8})	
	plt.grid()
	plt.ylabel("Days needed\nfor cases to double", fontsize=8)
	plt.xlabel("Days", fontsize=8)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.subplot2grid((2, 1), (1, 0))
	for i in range(len(datalocation[datatype])):
		startPoint = startPoints[dataguide][i] + outbreakDayCount
		datalist = databases[datatype][startPoint:startPoint + period][regionsIndexes[datatype][i]].values.tolist()
		duplicationtimes = getDuplicationTimes(datalist, "average")
		plt.plot(duplicationtimes, label=regions[i], linewidth=2.0)
	plt.title("Duplication speed trend in days for " + dataTitles[datatype] + " cases since number " + str(caseCount) + " " + dataTitles[dataguide], fontsize=11)
	plt.legend(loc=2, prop={'size': 8})	
	plt.grid()
	plt.ylabel("Days needed\nfor cases to double", fontsize=8)
	plt.xlabel("Values for 3 days average", fontsize=8)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.tight_layout(rect=[0, 0.03, 1, 1])
	plt.show()
	
plotbyDate(regionsIndexes, dataType)
plotbyOutbreak(regionsIndexes, dataType, dataGuide)
plotNewCases(regionsIndexes, dataType, dataGuide)
plotNewCases3Av(regionsIndexes, dataType, dataGuide)
plotDeathRate(regionsIndexes)
plotDuplicationTimes(regionsIndexes,dataType, dataGuide)

print("That's all. If you want more plots, edit the code and run again.                         ", end="\n")