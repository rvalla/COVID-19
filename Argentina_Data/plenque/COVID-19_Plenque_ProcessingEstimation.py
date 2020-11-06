import numpy as np
import pandas as pd
from datetime import datetime as dt

print("################################################")
print("      Estimations of COVID-19 Outbreak")
print("------------------------------------------------")
print("https://github.com/rvalla/COVID-19")
print("Data loaded from Mauro Infantino site")
print("https://covidstats.com.ar")
print("------------------------------------------------")
print()
print("Loading data...", end="\n")

#Selecting regions to study in detail...
#Note that the first one will be used as reference to decide periods of time in some charts...
#regions = ["CABA", "BUENOS AIRES", "CHACO", "CORDOBA", "RIO NEGRO", "MENDOZA", "NEUQUEN", "ARGENTINA", "SANTA FE", "TIERRA DEL FUEGO", "ENTRE RIOS"]
regionslabels = ["CABA", "PBA", "COR", "SF", "Argentina"]

#Variables to store filenames and other strings...
fileNameSuffix = "_Plenque.csv"
fileNames = ["CABA", "PBA", "COR", "SF", "Argentina"]

filepath = "plenque_data/"
datapath = "plenque_data/"

#Defining the data period
dataStartDate = "2020-01-01"
dataEndDate = "2020-10-10"
dataPeriod = pd.date_range(dataStartDate, dataEndDate)

realMortality = 0.01 #Real mortality to estimate infected count from deaths
deathOffset = 10 #Number of days needed to reach a death since symptoms onset on average

#Loading data...
databases = []
for d in range(len(fileNames)):
	plenque_csv = pd.read_csv(filepath + fileNames[d] + fileNameSuffix, skiprows=[0,1,2])
	databases.append(plenque_csv)
	databases[d].set_index("fecha", inplace = True)
	databases[d].index.name = "FECHA"

#Printing selected regions on console
print("Processing data of " + str(regionslabels), end="\n")

estimationsAndData = []

def getNewCases7dAv(dataseries):
	print("Calculating new cases taking 7 day average...                   ", end="\r")
	newCases = pd.Series(index = dataPeriod, dtype = "float64")
	for d in range(dataseries.shape[0] - 6):
		d0 = dataseries.loc[dataseries.index[d]]
		d1 = dataseries.loc[dataseries.index[d+1]]
		d2 = dataseries.loc[dataseries.index[d+2]]
		d3 = dataseries.loc[dataseries.index[d+3]]
		d4 = dataseries.loc[dataseries.index[d+4]]
		d5 = dataseries.loc[dataseries.index[d+5]]
		d6 = dataseries.loc[dataseries.index[d+6]]
		newCases.loc[newCases.index[d+3]] = (d0 + d1+ d2 + d3 + d4 + d5 + d6) / 7
		newCases.index = pd.DatetimeIndex(dataseries.index)
	return newCases

def buildData():
	for r in range(len(regionslabels)):
		regiondata = pd.DataFrame(index=databases[0].index, columns=["confirmed",  "deaths", "estimation", "ratio",
					"new confirmed", "new deaths", "new estimated", "new ratio", "new confirmed (7d)", "new deaths (7d)",
					"new estimated (7d)", "new ratio (7d)"])
		for e in range(regiondata.shape[0]):
			regiondata.loc[regiondata.index[e], "new confirmed"] = databases[r].loc[databases[r].index[e], "casos_dx"]
			regiondata.loc[regiondata.index[e], "new deaths"] = databases[r].loc[databases[r].index[e], "fallecidos"]
		regiondata["confirmed"] = regiondata[:]["new confirmed"].cumsum()
		regiondata["deaths"] = regiondata[:]["new deaths"].cumsum()
		regiondata["new confirmed (7d)"] = getNewCases7dAv(regiondata["new confirmed"])
		regiondata["new deaths (7d)"] = getNewCases7dAv(regiondata["new deaths"])
		for e in range(regiondata.shape[0] - deathOffset):
			regiondata.loc[regiondata.index[e], "estimation"] = \
			regiondata.loc[regiondata.index[e + deathOffset], "deaths"] / realMortality
			regiondata.loc[regiondata.index[e], "new estimated"] = \
			regiondata.loc[regiondata.index[e + deathOffset], "new deaths"] / realMortality
			regiondata.loc[regiondata.index[e], "new estimated (7d)"] = \
			regiondata.loc[regiondata.index[e + deathOffset], "new deaths (7d)"] / realMortality
		regiondata["ratio"] = regiondata["confirmed"].div(regiondata["estimation"])
		regiondata["new ratio"] = regiondata["new confirmed"].div(regiondata["new estimated"])
		regiondata["new ratio (7d)"] = regiondata["new confirmed (7d)"].div(regiondata["new estimated (7d)"])
		regiondata.replace([np.inf, -np.inf], np.nan, inplace=True)
		global estimationsAndData
		estimationsAndData.append(regiondata)

buildData()

print("Saving data to csv files...", end="\r")
for d in range(len(estimationsAndData)):
	estimationsAndData[d].to_csv(datapath + "Argentina_COVID19_Plenque_" + regionslabels[d] + ".csv")
print("That's all. CSV files were saved.                          ", end="\n")
