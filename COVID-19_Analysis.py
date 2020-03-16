from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator
import numpy as nu
import pandas as pd

#Selecting data: "Confirmed", "Deaths" or "Recovered"
dataSelection = "Confirmed"
fileName = "time_series_19-covid-" + dataSelection + ".csv"
fileCompletePath = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/" + fileName

#Selecting plot scale: "linear" or "log"
plotScale = "linear"

#Selecting regions to study
#Note that the first one will be used as reference to decide periods of time to plot
regions = ["Argentina", "Germany", "France", "Italy", "Spain"]

#Selecting data to display
startDate = "1/22/20" #Starting point for plotbyDate. Default: 1/22/20
caseCount = 1 #Starting point for plotbyOutbreak (number of confirmed cases)
outbreakDayCount = 0 #Number of days after caseCount condition is fulfiled

#Loading data...
data = pd.read_csv(fileCompletePath)
data = data.T

#Function to look for selected regions in Data Frame
def regionsIndexes(regions):
	indexes = []
	for i in range(len(regions)):
		for e in range(data.shape[1]):
			if data.loc['Country/Region', e] == regions[i]:
				indexes.append(e)
				break
	return indexes

#Function to plot cases for regions by date
def plotbyDate(regions):
	indexes = regionsIndexes(regions)
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(indexes)):
		data[startDate:][indexes[i]].plot(kind='line', label=regions[i])
	plt.title("COVID-19: " + dataSelection + " cases since " + startDate)
	plt.legend()	
	plt.tight_layout()
	plt.grid()
	plt.yscale(plotScale)
	plt.show()

#Function to look for first case in each region
def regionsStartPoints(regions):
	indexes = regionsIndexes(regions)
	startPoints = []
	for i in range(len(regions)):
		for e in range(data.shape[0]-4):
			if data.iloc[4 + e, indexes[i]] >= caseCount:
				startPoints.append(e + 4)
				break
	return startPoints

#Function to plot cases for regions since first case
def plotbyOutbreak(regions):
	indexes = regionsIndexes(regions)
	startPoints = regionsStartPoints(regions)
	period = data.shape[0] - startPoints[0] - outbreakDayCount
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(indexes)):
		startPoint = startPoints[i] + outbreakDayCount
		data[startPoint:startPoint + period][indexes[i]].plot(kind='line', label=regions[i])
	plt.title("COVID-19: " + dataSelection + " cases since number " + str(caseCount))
	plt.legend()	
	plt.tight_layout()
	plt.grid()
	plt.xticks([])
	plt.xlabel("Time in days")
	plt.yscale(plotScale)
	plt.show()

#plotbyDate(regions)
plotbyOutbreak(regions)

