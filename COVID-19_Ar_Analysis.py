from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator
import numpy as nu
import pandas as pd

print("####################################################")
print("       Visualization of COVID-19 Outbreak")
print("----------------------------------------------------")
print("https://github.com/rvalla/COVID-19")
print("Data loaded from official national reports")
print("https://argentina.gob.ar/coronavirus/informe-diario")
print("----------------------------------------------------")
print()
print("Ploting data of ", end=" ")

#Selecting data: "Confirmed", "Deaths" or "Recovered"
dataSelection = ["CONFIRMADOS", "ACTIVOS", "MUERTOS", "RECUPERADOS", "TESTEADOS", "DESCARTADOS"]
dataTitles = ["Confirmed", "Active", "Deaths", "Recovered", "Tested", "Dropped"]

fileName = "Argentina.csv"
fileCompletePath = "Argentina_Data/" + fileName
colorlist = ["orange", "tab:blue", "tab:red", "tab:green"]

#Loading data...
databases = []
dataframe = pd.read_csv(fileCompletePath)

for i in range(len(dataSelection)):
	databases.append(dataframe[dataframe['TYPE'] == dataSelection[i]])
	del	databases[i]["TYPE"]
	databases[i] = databases[i].T
	databases[i].columns = range(databases[i].shape[1])

del dataframe

#Selecting plot scale: "linear" or "log"
plotScale = "linear"
dayTags = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
startDateDay = 1

#Selecting regions to study
#Note that the first one will be used as reference to decide periods of time to plot
regions = ["CABA", "BUENOS AIRES", "CHACO"]
#regions = ["CHACO", "SANTA FE", "RIO NEGRO", "CORDOBA"]
#regions = ["NEUQUEN", "MENDOZA", "LA RIOJA", "ENTRE RIOS", "SANTA FE", "SAN JUAN", "CHUBUT"]
regionsIndexes = [[],[]]
regionReference = "PROVINCIA"
quarantineStart = "2020-03-03"
quarantineIndex = databases[0].index.get_loc(quarantineStart)

#Deciding what to plot...
byDate = True #Decide if you want to plot data by date for selected regions.
byOutbreak = True #Decide if you want to plot data by notified cases for selected regions.
newCases = False #Decide if you want to plot new daily cases for selected regions
newCasesTrend = True #Decide if you want to plot new daily cases trend (3 day average) for selected regions
deathRate = True #Decide if you want to plot death rate evolution for selected regions
duplicationTimes = True #Decide if you want to plot cases duplication times for selected regions
weeklyAnalysis = False #Decide if you want to plot new daily cases by day of the week for selected regions
plotAllCountry = True #Decide if you want a final plot with summary for cases in Argentina.
duplicationTimesAC = True #Decide if you want to plot Duplication Times in the country.
weeklyAnalysisAC = False #Decide if you want to plot week day data of notified cases in Argentina.

#Selecting data to display
startDate = "2020-03-03" #Starting point for plotbyDate. Default: 03/03
startDateIndex = databases[0].index.get_loc(startDate) #Saving the startDate index for annotations
caseCount = 200 #Starting point for plotbyOutbreak (number of confirmed cases)
outbreakDayCount = 0 #Number of days after caseCount condition is fulfiled
dataType = 0 #0 = Confirmed, 1 = Active, 2 = Deaths, 3 = Recovered
dataGuide = 0 #Data type to calculate startpoints (confirmed, active, deaths, recovered)

#Printing selected regions on console
print(regions, end="\r")

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

#Method to draw a mark in social isolation start date
def markQuarantine(tag, yshift, ytshift, font, x, y, w, hw, hl):
	if startDateIndex < quarantineIndex:
		plt.annotate(tag, fontsize=font, xy=(x, y + yshift),  xycoords='data',
    		xytext=(x, y + ytshift), textcoords='data',
			arrowprops=dict(facecolor='orangered', edgecolor="none", width=w, headwidth=hw, headlength=hl),
        	horizontalalignment='center', verticalalignment='top')

#Function to plot cases for regions by date. Use 0, 1 or 2 to select Confirmed, Deaths or Recovered
def plotbyDate(datalocation, datatype):
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	yquarantine = []
	x = quarantineIndex - startDateIndex
	for i in range(len(datalocation[datatype])):
		databases[datatype][startDate:][datalocation[datatype][i]].plot(kind='line', label=regions[i], linewidth=2.5)
		yquarantine.append(databases[datatype].iloc[x, datalocation[datatype][i]])
		if i == len(datalocation[datatype]) - 1:
			y = max(yquarantine)
			s = plt.ylim()
			markQuarantine("Social\nisolation", s[1]/25, s[1]/5, 8, x, y, 5, 9, 7)
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
		deaths = databases[2][startDate:][datalocation[1][r]].values.tolist()
		for d in range(len(confirmed)):
			if confirmed[d] > 0:
				deathRates[r].append(deaths[d]/confirmed[d])
			else:
				deathRates[r].append(0)
	return deathRates

def getCountryDeathRate():
	deathRates = []
	confirmed = databases[0][startDate:][databases[0].shape[1]-1].values.tolist()
	deaths = databases[2][startDate:][databases[2].shape[1]-1].values.tolist()
	for d in range(len(confirmed)):
		if confirmed[d] > 0:
			deathRates.append(deaths[d]/confirmed[d])
		else:
			deathRates.append(0)
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
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 0.05))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
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
	plt.yscale(plotScale)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
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
	
def plotAllCountryData():
	figure = plt.figure(num=None, figsize=(7, 4.5), dpi=150, facecolor='w', edgecolor='k')
	figure.suptitle("Total cases in Argentina", fontsize=13)
	plt.subplot2grid((3, 2), (0, 0))
	x = quarantineIndex - startDateIndex
	yquarantine = []
	for d in range(len(databases)-3):
		total = databases[d][startDate:][databases[d].shape[1] - 1].plot(kind="line", linewidth=2.0, label=dataTitles[d], color=colorlist[d])
		yquarantine.append(databases[0].iloc[x, databases[0].shape[1] - 1])
		if d == len(databases)-4:
			y = max(yquarantine)
			s = plt.ylim()			
			markQuarantine("", s[1]/20, s[1]/4.5, 8, x, y, 3, 6, 5)
	total.legend(loc=0, prop={'size': 7})
	total.set_title("Total cases", fontsize=10)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 3000))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.subplot2grid((3, 2), (0, 1))
	yquarantine = []
	for d in range(len(databases)-3):
		auxlist = databases[d][startDate:][databases[d].shape[1] - 1].values.tolist()
		ls = getNewCasesAv(getNewCases(auxlist))
		plt.plot(ls, linewidth=2.0, label=dataTitles[d], color=colorlist[d])
		yquarantine.append(ls[x])
		if d == 0:
			y = max(yquarantine)
			s = plt.ylim()			
			markQuarantine("", s[1]/20, s[1]/4.5, 8, x, y, 3, 6, 5)
	plt.legend(loc=0, prop={'size': 7})
	plt.title("New cases trend (3 days average)", fontsize=10)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 150))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.subplot2grid((3, 2), (1, 0))
	deaths = databases[2][startDate:][databases[2].shape[1] - 1].plot(kind="line", linewidth=2.0, label=dataTitles[2], color=colorlist[2])
	deaths.set_title("Deaths", fontsize=10)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 150))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.subplot2grid((3, 2), (1, 1))
	deathrate = getCountryDeathRate()
	plt.plot(deathrate, linewidth=2.0, label="Death rate", color=colorlist[2])
	plt.title("Death rate evolution", fontsize=10)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 0.05))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.subplot2grid((3, 2), (2, 0))
	tests = databases[4][startDate:][databases[4].shape[1] - 1].plot(kind="line", linewidth=2.0, label=dataTitles[4], color=colorlist[0])
	tests = databases[5][startDate:][databases[5].shape[1] - 1].plot(kind="line", linewidth=2.0, label=dataTitles[5], color=colorlist[3])
	plt.title("Testing & dropped cases evolution", fontsize=10)
	plt.legend(loc=0, prop={'size': 7})
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 30000))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.subplot2grid((3, 2), (2, 1))
	datalist = databases[0][startDate:][databases[0].shape[1] - 1].values.tolist()
	duplicationtimes = getDuplicationTimes(datalist, "average")
	plt.bar(range(len(duplicationtimes)), duplicationtimes)
	plt.title("Duplication speed trend (3 days av.)", fontsize=10)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 15))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.tight_layout(rect=[0, 0.03, 1, 0.95])
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

def getDuplicationTimesBar(datalist, type):
	newcases = getNewCases(datalist)
	duplicationtimes = []
	if type == "average":
		newcases = getNewCasesAv(newcases)
	for e in range(len(newcases)-1):
		if newcases[e+1] > 0:
			duplicationtimes.append(datalist[e]/newcases[e+1])
		else:
			duplicationtimes.append(0)
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
	plt.legend(loc=0, prop={'size': 6})	
	plt.ylabel("Days needed\nfor cases to double", fontsize=8)
	plt.xlabel("Days", fontsize=8)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.subplot2grid((2, 1), (1, 0))
	for i in range(len(datalocation[datatype])):
		startPoint = startPoints[dataguide][i] + outbreakDayCount
		datalist = databases[datatype][startPoint:startPoint + period][regionsIndexes[datatype][i]].values.tolist()
		duplicationtimes = getDuplicationTimes(datalist, "average")
		plt.plot(duplicationtimes, label=regions[i], linewidth=2.0)
	plt.title("Duplication speed trend in days for " + dataTitles[datatype] + " cases since number " + str(caseCount) + " " + dataTitles[dataguide], fontsize=11)
	plt.legend(loc=0, prop={'size': 6})	
	plt.ylabel("Days needed\nfor cases to double", fontsize=8)
	plt.xlabel("Values for 3 days average", fontsize=8)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.tight_layout(rect=[0, 0.03, 1, 1])
	plt.show()
	
def plotAllCountryDT(datatype):
	figure = plt.figure(num=None, figsize=(7, 4), dpi=150, facecolor='w', edgecolor='k')
	plt.subplot2grid((2, 1), (0, 0))
	datalist = databases[datatype][startDate:][databases[datatype].shape[1] - 1].values.tolist()
	duplicationtimes = getDuplicationTimesBar(datalist, " ")
	plt.bar(range(len(duplicationtimes)), duplicationtimes)
	x = quarantineIndex - startDateIndex
	y = duplicationtimes[x]
	s = plt.ylim()
	markQuarantine("", s[1]/20, s[1]/5, 6, x, y, 3, 6, 5)
	plt.title("Argentina: Duplication speed in days for " + dataTitles[datatype] + " cases since " + str(startDate), fontsize=11)
	plt.grid()
	plt.ylabel("Days needed\nfor cases to double", fontsize=8)
	plt.xlabel("Days", fontsize=8)
	plt.yticks(nu.arange(0, s[1] * 1.2, 10))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.subplot2grid((2, 1), (1, 0))
	duplicationtimes = getDuplicationTimesBar(datalist, "average")
	plt.bar(range(len(duplicationtimes)), duplicationtimes)
	x = quarantineIndex - startDateIndex
	y = duplicationtimes[x]
	s = plt.ylim()
	markQuarantine("", s[1]/20, s[1]/5, 6, x, y, 3, 6, 5)
	plt.title("Argentina: Duplication speed trend in days for " + dataTitles[datatype] + " cases since " + str(startDate), fontsize=11)
	plt.grid()
	plt.ylabel("Days needed\nfor cases to double", fontsize=8)
	plt.xlabel("Values for 3 days average", fontsize=8)
	plt.yticks(nu.arange(0, s[1] * 1.2, 10))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
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
			if weeklyMaximun > 0:
				weeklyCases[w].append(newCasesHistory[w*7 + d]/weeklyMaximun)
			else:
				weeklyCases[w].append(None)
	averages = []
	for d in range(7):
		aux = 0
		realWeekCount = 0
		for w in range(weekCount):
			if weeklyCases[w][d] != None:
				aux += weeklyCases[w][d]
				realWeekCount += 1
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
		plt.plot(weeklyCases[w], linewidth=2.0, color=colorlist[1], alpha=0.5)
	plt.plot(weeklyCases[len(weeklyCases)-1], linewidth=2.5, color=colorlist[0], alpha=1.0)
	plt.plot([0, 6], [weeklyCases[len(weeklyCases)-1][0], weeklyCases[len(weeklyCases)-1][6]], linewidth=1.0,
						linestyle="--", color=colorlist[2], alpha=1.0)
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
		plt.plot(weeklyCases[w], linewidth=2.0, color=colorlist[1], alpha=0.5)
	plt.plot(weeklyCases[len(weeklyCases)-1], linewidth=2.5, color=colorlist[0], alpha=1.0)
	plt.plot([0, 6], [weeklyCases[len(weeklyCases)-1][0], weeklyCases[len(weeklyCases)-1][6]], linewidth=1.0,
						linestyle="--", color=colorlist[2], alpha=1.0)
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

if byDate == True:
	plotbyDate(regionsIndexes, dataType)
if byOutbreak == True:
	plotbyOutbreak(regionsIndexes, dataType, dataGuide)
if newCases == True:
	plotNewCases(regionsIndexes, dataType, dataGuide)
if newCasesTrend == True:
	plotNewCases3Av(regionsIndexes, dataType, dataGuide)
if deathRate == True:
	plotDeathRate(regionsIndexes)
if duplicationTimes == True:
	plotDuplicationTimes(regionsIndexes, dataType, dataGuide)
if weeklyAnalysis == True:
	plotWeeklyAnalysis(regionsIndexes, dataType)
if plotAllCountry == True:
	plotAllCountryData()
	if duplicationTimesAC == True:
		plotAllCountryDT(dataType)
	if weeklyAnalysisAC == True:
		plotWeeklyCases(databases[dataType].shape[1]-1, dataType, "Argentina")

print("That's all. If you want more plots, edit the code and run again.                          ", end="\n")