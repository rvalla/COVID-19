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
dayTags = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
startDateDay = 2

#Selecting regions to study
#Note that the first one will be used as reference to decide periods of time to plot
regions = ["Germany", "Italy", "Spain", "United Kingdom", "Switzerland"]
#regions = ["Sweden", "Norway", "Finland", "Denmark"]
#regions = ["Argentina", "Chile", "Uruguay", "Colombia", "Paraguay"]
regionsIndexes = [[],[]]
groupbyCountry = True
#You can choose 'Country/Region' or 'Province/State'. Select regions correctly though...
#If you choose 'Province/State' then 'groupbyCountry' must be False
regionReference = "Country/Region"

#Selecting data to display
startDate = "2/20/20" #Starting point for plotbyDate. Default: 1/22/20
caseCount = 200 #Starting point for plotbyOutbreak (number of confirmed cases)
outbreakDayCount = 0 #Number of days after caseCount condition is fulfiled
dataType = 1 #0 = Confirmed, 1 = Deaths, 2 = Recovered
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

startDateIndex = databases[0].index.get_loc(startDate)

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

def getStartDateDay():
	global startDateDay
	day = (startDateIndex + 1)%7
	startDateDay = day

getStartDateDay()
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
	period = databases[dataguide].shape[0] - startPoints[dataguide][0] - outbreakDayCount
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
	for e in range(len(datalist) - 1):
		ls.append(datalist[e+1] - datalist[e])
	return ls

def getNewCasesAv(datalist):
	ls = []
	for e in range(len(datalist) - 2):
		ls.append((datalist[e+2] + datalist[e+1] + datalist[e])/3)
	index = len(datalist)
	ls.append((datalist[index-1]+datalist[index-2])/2)
	return ls

def plotNewCases(datalocation, datatype, dataguide):
	startPoints = regionsStartPoints(regions)
	period = databases[dataguide].shape[0] - startPoints[dataguide][0] - outbreakDayCount
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(datalocation[datatype])):
		startPoint = startPoints[dataguide][i] + outbreakDayCount
		if startPoint > 0:
			startPoint -= 1
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
	period = databases[dataguide].shape[0] - startPoints[dataguide][0] - outbreakDayCount
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(datalocation[datatype])):
		startPoint = startPoints[dataguide][i] + outbreakDayCount
		if startPoint > 0:
			startPoint -= 1
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
	for e in range(len(newcases)-1):
		if newcases[e+1] > 0:
			duplicationtimes.append(datalist[e]/newcases[e+1])
		else:
			duplicationtimes.append(None)
	return duplicationtimes

def plotDuplicationTimes(datalocation, datatype, dataguide):
	startPoints = regionsStartPoints(regions)
	period = databases[dataguide].shape[0] - startPoints[dataguide][0] - outbreakDayCount
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

def getWeeklyCases(regionindex, datatype):
	casesHistory = databases[datatype][startDate:][regionindex].values.tolist()
	newCasesHistory = getNewCases(casesHistory)
	weekCount = int(len(newCasesHistory)/7)
	weeklyCases = [[] for d in range(weekCount)]
	for w in range(weekCount):
		for d in range(7):
			weeklyCases[w].append(newCasesHistory[w*7 + d])
	averages = []
	for d in range(7):
		aux = 0
		for w in range(weekCount):
			aux += weeklyCases[w][d]
		averages.append(aux/weekCount)
	weeklyCases.append(averages)
	
	return weeklyCases

def getWeeklyCasesR(regionindex, datatype):
	casesHistory = databases[datatype][startDate:][regionindex].values.tolist()
	newCasesHistory = getNewCases(casesHistory)
	weekCount = int(len(newCasesHistory)/7)
	weeklyCases = [[] for d in range(weekCount)]
	for w in range(weekCount):
		weeklyMaximun = max(newCasesHistory[w*7:w*7+7])
		for d in range(7):
			weeklyCases[w].append(newCasesHistory[w*7 + d]/weeklyMaximun)
	averages = []
	for d in range(7):
		aux = 0
		for w in range(weekCount):
			aux += weeklyCases[w][d]
		averages.append(aux/weekCount)
	weeklyCases.append(averages)
	
	return weeklyCases

def getDaysTags(dayTags, offset):
	daylist = []
	for d in range(len(dayTags)):
		daylist.append(dayTags[(d + startDateDay + offset)%7])
	return daylist

def plotWeeklyCases(regionindex, datatype, region):
	figure = plt.figure(num=None, figsize=(5, 4), dpi=150, facecolor='w', edgecolor='k')
	figure.suptitle(region + ": Weeks analysis (" + dataTitles[datatype] + " since " + startDate + ")", fontsize=12)
	weeklyCases = getWeeklyCases(regionindex, datatype)
	plt.subplot2grid((2, 1), (0, 0))
	for w in range(len(weeklyCases) - 1):
		plt.plot(weeklyCases[w], linewidth=2.0, color="tab:blue", alpha=0.5)
	plt.plot(weeklyCases[len(weeklyCases)-1], linewidth=2.5, color="orange", alpha=1.0)
	plt.plot([0, 6], [weeklyCases[len(weeklyCases)-1][0], weeklyCases[len(weeklyCases)-1][6]], linewidth=1.0,
						linestyle="--", color="tab:red", alpha=1.0)
	plt.title("New cases by day of the week (absolute)", fontsize=10)
	plt.grid()
	plt.ylabel("New daily cases", fontsize=6)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, round(ylimits[1]/5,0)))
	plt.xticks(nu.arange(0, 7, step = 1), getDaysTags(dayTags, 0), fontsize = 6, rotation = 30)
	plt.xticks(fontsize=5)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	weeklyCases = getWeeklyCasesR(regionindex, datatype)
	plt.subplot2grid((2, 1), (1, 0))
	for w in range(len(weeklyCases) - 1):
		plt.plot(weeklyCases[w], linewidth=2.0, color="tab:blue", alpha=0.5)
	plt.plot(weeklyCases[len(weeklyCases)-1], linewidth=2.5, color="orange", alpha=1.0)
	plt.plot([0, 6], [weeklyCases[len(weeklyCases)-1][0], weeklyCases[len(weeklyCases)-1][6]], linewidth=1.0,
						linestyle="--", color="tab:red", alpha=1.0)
	plt.title("New cases by day of the week (relative)", fontsize=10)
	plt.grid()
	plt.ylabel("Variation relative\nto week maximun", fontsize=6)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, round(ylimits[1]/5,1)))
	plt.xticks(nu.arange(0, 7, step = 1), getDaysTags(dayTags, 0), fontsize = 6, rotation = 30)
	plt.xticks(fontsize=5)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.tight_layout(rect=[0, 0.03, 1, 0.95])
	plt.show()

def plotWeeklyAnalysis(datalocation, datatype):
	for d in range(len(datalocation[datatype])):
		plotWeeklyCases(datalocation[datatype][d], datatype, regions[d])
	
plotbyDate(regionsIndexes, dataType)
plotbyOutbreak(regionsIndexes, dataType, dataGuide)
#plotNewCases(regionsIndexes, dataType, dataGuide)
plotNewCases3Av(regionsIndexes, dataType, dataGuide)
plotDeathRate(regionsIndexes)
plotDuplicationTimes(regionsIndexes,dataType, dataGuide)
#plotWeeklyAnalysis(regionsIndexes, dataType)

print("That's all. If you want more plots, edit the code and run again.                         ", end="\n")