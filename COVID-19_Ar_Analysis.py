from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator
import numpy as nu
import pandas as pd

print("###########################################")
print("    Visualization of COVID-19 Outbreak")
print("-------------------------------------------")
print("https://github.com/rvalla/COVID-19")
print("Data from argcovidapi:")
print("https://github.com/mariano22/argcovidapi")
print("------------------------------------------")
print()
print("Ploting data of ", end=" ")

#Selecting data: "Confirmed", "Deaths" or "Recovered"
dataSelection = ["CONFIRMADOS", "ACTIVOS", "MUERTOS", "RECUPERADOS", "TESTEADOS"]
dataTitles = ["Confirmed", "Active", "Deaths", "Recovered", "Tested"]

fileName = "Argentina.csv"
fileCompletePath = "Argentina_Data/" + fileName

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

#Selecting regions to study
#Note that the first one will be used as reference to decide periods of time to plot
regions = ["CABA", "BUENOS AIRES", "CORDOBA", "CHACO", "SANTA FE", "RIO NEGRO"]
#regions = ["CABA", "BUENOS AIRES"]
#regions = ["NEUQUEN", "MENDOZA", "SALTA", "LA RIOJA", "ENTRE RIOS", "SAN JUAN"]
regionsIndexes = [[],[]]
regionReference = "PROVINCIA"
quarantineStart = "20/03"
quarantineIndex = databases[0].index.get_loc(quarantineStart)

plotAllCountry = True #Decide if you want a final plot of total cases in Argentina.

#Selecting data to display
startDate = "03/03" #Starting point for plotbyDate. Default: 03/03
startDateIndex = databases[0].index.get_loc(startDate) #Saving the startDate index for annotations
caseCount = 100 #Starting point for plotbyOutbreak (number of confirmed cases)
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
	for i in range(len(datalocation[datatype])):
		databases[datatype][startDate:][datalocation[datatype][i]].plot(kind='line', label=regions[i], linewidth=2.5)
		if i == 0:
			x = quarantineIndex - startDateIndex
			y = databases[datatype].iloc[x, datalocation[datatype][i]]
			s = plt.ylim()
			markQuarantine("Social\nisolation", s[1]/16, s[1]/4, 8, x, y, 5, 9, 7)
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
	for d in range(len(databases)-3):
		total = databases[d][startDate:][databases[d].shape[1] - 1].plot(kind="line", linewidth=2.0, label=dataTitles[d])
		if d == 0:
			x = quarantineIndex - startDateIndex
			y = databases[0].iloc[x, databases[0].shape[1] - 1]
			markQuarantine("", 180, 630, 8, x, y, 3, 6, 5)
	total.legend(loc=0, prop={'size': 7})
	total.set_title("Total cases", fontsize=10)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 1000))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.subplot2grid((3, 2), (0, 1))
	for d in range(len(databases)-3):
		auxlist = databases[d][startDate:][databases[d].shape[1] - 1].values.tolist()
		ls = getNewCasesAv(getNewCases(auxlist))
		plt.plot(ls, linewidth=2.5, label=dataTitles[d])
		if d == 0:
			x = quarantineIndex - startDateIndex
			y = ls[x]
			markQuarantine("", 10, 30, 8, x, y, 3, 6, 5)
	plt.legend(loc=0, prop={'size': 7})
	plt.title("New cases trend (3 days average)", fontsize=10)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 50))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.subplot2grid((3, 2), (1, 0))
	deaths = databases[2][startDate:][databases[2].shape[1] - 1].plot(kind="line", linewidth=2.0, label=dataTitles[2], color="orangered")
	deaths.set_title("Deaths", fontsize=10)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 50))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.subplot2grid((3, 2), (1, 1))
	deathrate = getCountryDeathRate()
	plt.plot(deathrate, linewidth=2.0, label="Death rate", color="orangered")
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
	tests = databases[4][startDate:][databases[4].shape[1] - 1].plot(kind="line", linewidth=2.0, label=dataTitles[2], color="orange")
	plt.title("Testing evolution", fontsize=10)
	plt.yscale(plotScale)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 10000))
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
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 10))
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
	duplicationtimes = getDuplicationTimes(datalist, " ")
	plt.bar(range(len(duplicationtimes)), duplicationtimes)
	plt.title("Argentina: Duplication speed in days for " + dataTitles[datatype] + " cases since " + str(startDate), fontsize=11)
	plt.grid()
	plt.ylabel("Days needed\nfor cases to double", fontsize=8)
	plt.xlabel("Days", fontsize=8)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 10))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.subplot2grid((2, 1), (1, 0))
	duplicationtimes = getDuplicationTimes(datalist, "average")
	plt.bar(range(len(duplicationtimes)), duplicationtimes)
	plt.title("Argentina: Duplication speed trend in days for " + dataTitles[datatype] + " cases since " + str(startDate), fontsize=11)
	plt.grid()
	plt.ylabel("Days needed\nfor cases to double", fontsize=8)
	plt.xlabel("Values for 3 days average", fontsize=8)
	ylimits = plt.ylim()
	plt.yticks(nu.arange(0, ylimits[1] * 1.2, 10))
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c="dimgray", alpha=0.5)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c="black", alpha=0.5)
	plt.tight_layout(rect=[0, 0.03, 1, 1])
	plt.show()
	
plotbyDate(regionsIndexes, dataType)
plotbyOutbreak(regionsIndexes, dataType, dataGuide)
plotNewCases(regionsIndexes, dataType, dataGuide)
plotNewCases3Av(regionsIndexes, dataType, dataGuide)
plotDeathRate(regionsIndexes)
plotDuplicationTimes(regionsIndexes, dataType, dataGuide)
if plotAllCountry == True:
	plotAllCountryData()
	plotAllCountryDT(dataType)

print("That's all. If you want more plots, edit the code and run again.                          ", end="\n")