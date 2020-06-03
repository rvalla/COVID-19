from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, FixedLocator
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
print("Ploting data of ", end=" ")

#Selecting data: "Confirmed", "Deaths" or "Recovered"
regions = ["CABA", "Buenos Aires", "Santa Fe", "Córdoba", "Río Negro", "Chubut"]
dataTitles = ["CABA", "Buenos Aires", "Santa Fe", "Córdoba", "Río Negro", "Chubut"]

fileName = "Covid19Determinaciones.csv"
fileCompletePath = "Argentina_Data/datos.gob.ar/" + fileName
colorlist = ["orange", "tab:blue", "tab:red", "tab:green"]

dataStartDate = "2020-02-11"
dataEndDate = "2020-05-14"
wantedStartDate = "2020-04-14"
wantedEndDate = "2020-05-14"
dataPeriod = pd.date_range(dataStartDate, dataEndDate)
plotScale = "linear"

#Loading data by province...
databases = []
cumulative_databases = []
dataframe = pd.read_csv(fileCompletePath)
del dataframe["codigo indec provincia"]
del dataframe["codigo Indec departamento"]
del dataframe["localidad"]
del dataframe["codigo indec localidad"]
del dataframe["origen de financiamiento"]
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
	cumulative_databases.append(databases[r].cumsum())
	databases[r].loc[:,"ratio"] = databases[r][:]["positivos"].div(databases[r][:]["total"])
	databases[r]["ratio"].fillna(0, inplace=True)
	cumulative_databases[r].loc[:,"ratio"] = cumulative_databases[r][:]["positivos"].div(cumulative_databases[r][:]["total"])
	cumulative_databases[r]["ratio"].fillna(0, inplace=True)

print("The data is ready!              ", end= "\n")

def plotTestsbyRegions():
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(databases)):
		databases[i][wantedStartDate:wantedEndDate]["total"].plot(kind='line', label=regions[i], linewidth=2.0)
	plt.title("COVID-19: Daily tests by regions")
	plt.legend(loc=0, prop={'size': 8})	
	plt.grid()
	plt.ylabel("Number of tests")
	plt.xlabel("Time in days")
	plt.yscale(plotScale)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.tight_layout()
	plt.show()

def plotCumulativeTestsbyRegions():
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(databases)):
		cumulative_databases[i][wantedStartDate:wantedEndDate]["total"].plot(kind='line', label=regions[i], linewidth=2.0)
	plt.title("COVID-19: Cumulative tests by regions")
	plt.legend(loc=0, prop={'size': 8})	
	plt.grid()
	plt.ylabel("Number of tests")
	plt.xlabel("Time in days")
	plt.yscale(plotScale)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.tight_layout()
	plt.show()

def plotDailyInfectedRatio():
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(databases)):
		databases[i][wantedStartDate:wantedEndDate]["ratio"].plot(kind='line', label=regions[i], linewidth=2.0)
	plt.title("COVID-19: Positive tests ratio")
	plt.legend(loc=0, prop={'size': 8})	
	plt.grid()
	plt.ylabel("Positive tests ratio")
	plt.xlabel("Time in days")
	plt.yscale(plotScale)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.tight_layout()
	plt.show()

def plotCumulativeInfectedRatio():
	figure(num=None, figsize=(8, 4), dpi=150, facecolor='w', edgecolor='k')
	for i in range(len(databases)):
		cumulative_databases[i][wantedStartDate:wantedEndDate]["ratio"].plot(kind='line', label=regions[i], linewidth=2.0)
	plt.title("COVID-19: Positive tests ratio (cumulative)")
	plt.legend(loc=0, prop={'size': 8})	
	plt.grid()
	plt.ylabel("Positive tests ratio")
	plt.xlabel("Time in days")
	plt.yscale(plotScale)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.tight_layout()
	plt.show()

#plotTestsbyRegions()
plotCumulativeTestsbyRegions()
plotDailyInfectedRatio()
plotCumulativeInfectedRatio()

print("That's all. If you want more plots, edit the code and run again.                          ", end="\n")