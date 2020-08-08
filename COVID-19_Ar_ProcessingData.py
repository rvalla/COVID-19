from matplotlib.pyplot import figure
import pandas as pd

print("####################################################")
print("       Processing data of COVID-19 Outbreak")
print("----------------------------------------------------")
print("https://github.com/rvalla/COVID-19")
print("Data loaded from official national reports")
print("https://argentina.gob.ar/coronavirus/informe-diario")
print("----------------------------------------------------")
print()
print("Loading Argentina.csv...", end="\n")

#Selecting data: "Confirmed", "Deaths" or "Recovered"
dataSelection = ["CONFIRMADOS", "ACTIVOS", "MUERTOS", "RECUPERADOS", "TESTEADOS", "DESCARTADOS"]
dataTitles = ["Confirmed", "Active", "Deaths", "Recovered", "Tested", "Dropped",
				"Deathrate", "NewConfirmed", "NewConfirmed3dAv", "ActiveVariation", "ActiveVariation3dAv",
				"NewDeaths", "NewDeaths3dAv", "NewRecovered", "NewRecovered3dAv", "NewTested", "NewTested3dAv",
				"PositiveTestsRatio", "PositiveTestsRatio3dAv", "CumulativePositiveTestsRatio",
				"DuplicationTimes", "DuplicationTimes3dAv", "DeathDuplicationTimes", "DeathDuplicationTimes3dAv",
				"NewDropped", "NewDropped3dAv", "NewConfirmed7dAv", "ActiveVariation7dAv", "Newdeaths7dAv",
				"NewRecovered7dAv", "NewTested7dAv", "NewDropped7dAv", "DuplicationTimes7dAv", "DeathDuplicationTimes7dAv",
				"PositiveTestsRatio7dAv"]

fileName = "Argentina.csv"
fileCompletePath = "Argentina_Data/" + fileName

dataStartDate = "2020-03-03"
dataEndDate = "2020-08-07"
dataPeriod = pd.date_range(dataStartDate, dataEndDate)

datapath = "Argentina_Data/processed_data/"

#Loading data...
databases = []
dataframe = pd.read_csv(fileCompletePath)

for i in range(len(dataSelection)):
	print("Creating dataframe for " + dataSelection[i] + "          ", end="\r")
	databases.append(dataframe[dataframe['TYPE'] == dataSelection[i]])
	del	databases[i]["TYPE"]
	databases[i] = databases[i].T
	databases[i].columns = databases[i].loc["PROVINCIA"]
	databases[i] = databases[i].drop(databases[i].index[0], axis=0)
	databases[i].index = pd.DatetimeIndex(databases[i].index)
	databases[i].index.name = "FECHA"

print("Original dataframes created...                                ", end="\n")

del dataframe

def getNewCases(dataframe):
	print("Calculating new cases...                                         ", end="\r")
	newCases = pd.DataFrame(index=dataPeriod, columns=dataframe.columns)
	columns = dataframe.columns
	for c in range(len(columns)):
		newCases.loc[newCases.index[0], columns[c]] = dataframe.loc[dataframe.index[0],columns[c]]
		for d in range(dataframe.shape[0] - 1):
			newCases.loc[newCases.index[d+1],columns[c]] = dataframe.loc[dataframe.index[d+1],columns[c]] \
				- dataframe.loc[dataframe.index[d],columns[c]] 
	newCases.index = pd.DatetimeIndex(dataframe.index)
	return newCases

def getNewCases3dAv(dataframe):
	print("Calculating new cases taking 3 day average...                   ", end="\r")
	newCases = pd.DataFrame(index = dataPeriod, columns=dataframe.columns)
	columns = dataframe.columns
	for c in range(len(columns)):
		for d in range(dataframe.shape[0] - 2):
			d0 = dataframe.loc[dataframe.index[d],columns[c]]
			d1 = dataframe.loc[dataframe.index[d+1],columns[c]]
			d2 = dataframe.loc[dataframe.index[d+2],columns[c]]
			newCases.loc[newCases.index[d+1],columns[c]] = (d0 + d1+ d2) / 3
	newCases.index = pd.DatetimeIndex(dataframe.index)
	return newCases

def getNewCases7dAv(dataframe):
	print("Calculating new cases taking 7 day average...                   ", end="\r")
	newCases = pd.DataFrame(index = dataPeriod, columns=dataframe.columns)
	columns = dataframe.columns
	for c in range(len(columns)):
		for d in range(dataframe.shape[0] - 6):
			d0 = dataframe.loc[dataframe.index[d],columns[c]]
			d1 = dataframe.loc[dataframe.index[d+1],columns[c]]
			d2 = dataframe.loc[dataframe.index[d+2],columns[c]]
			d3 = dataframe.loc[dataframe.index[d+3],columns[c]]
			d4 = dataframe.loc[dataframe.index[d+4],columns[c]]
			d5 = dataframe.loc[dataframe.index[d+5],columns[c]]
			d6 = dataframe.loc[dataframe.index[d+6],columns[c]]
			newCases.loc[newCases.index[d+3],columns[c]] = (d0 + d1+ d2 + d3 + d4 + d5 + d6) / 7
	newCases.index = pd.DatetimeIndex(dataframe.index)
	return newCases

def getRatios(dividends, divisors):
	print("Calculating some ratios...                                     ", end="\r")
	rates = pd.DataFrame(index=dataPeriod, columns = dividends.columns)
	columns = dividends.columns
	for c in range(len(columns)):
		for d in range(dividends.shape[0]):
			dividend = dividends.loc[dividends.index[d], columns[c]]
			divisor = divisors.loc[divisors.index[d], columns[c]]
			if divisor > 0:
				rates.loc[rates.index[d],columns[c]] = dividend / divisor
	rates.index = pd.DatetimeIndex(dividends.index)
	return rates

def getLinearDuplicationTimes(cumulative, newCases):
	print("Calculating cases duplication time...                         ", end="\r")
	duplicationtimes = pd.DataFrame(index = dataPeriod, columns = cumulative.columns)
	columns = cumulative.columns
	for c in range(len(columns)):
		duplicationtimes.loc[newCases.index[0], columns[c]] = 1
		for d in range(cumulative.shape[0] - 1):
			count = cumulative.loc[cumulative.index[d],columns[c]]
			variation = newCases.loc[newCases.index[d+1],columns[c]]
			if variation > 0:
				duplicationtimes.loc[duplicationtimes.index[d+1],columns[c]] = count / variation
	duplicationtimes.index = pd.DatetimeIndex(cumulative.index)
	return duplicationtimes

def getLinearDuplicationTimes3dAv(cumulative, newCases3dAv):
	print("Calculating cases duplication time taking 3 day average...    ", end="\r")
	duplicationtimes = pd.DataFrame(index = dataPeriod, columns = cumulative.columns)
	columns = cumulative.columns
	for c in range(len(columns)):
		for d in range(cumulative.shape[0] - 2):
			count = cumulative.loc[cumulative.index[d],columns[c]]
			variation = newCases3dAv.loc[newCases3dAv.index[d+1],columns[c]]
			if variation > 0:
				duplicationtimes.loc[duplicationtimes.index[d+1],columns[c]] = count / variation
	duplicationtimes.index = pd.DatetimeIndex(cumulative.index)
	return duplicationtimes

def getLinearDuplicationTimes7dAv(cumulative, newCases7dAv):
	print("Calculating cases duplication time taking 7 day average...    ", end="\r")
	duplicationtimes = pd.DataFrame(index = dataPeriod, columns = cumulative.columns)
	columns = cumulative.columns
	for c in range(len(columns)):
		for d in range(cumulative.shape[0] - 6):
			count = cumulative.loc[cumulative.index[d],columns[c]]
			variation = newCases7dAv.loc[newCases7dAv.index[d+3],columns[c]]
			if variation > 0:
				duplicationtimes.loc[duplicationtimes.index[d+3],columns[c]] = count / variation
	duplicationtimes.index = pd.DatetimeIndex(cumulative.index)
	return duplicationtimes

print("Ready to build dataframes for analysis...                         ", end="\n")
databases.append(getRatios(databases[2], databases[1])) # 6: Deathrate
databases.append(getNewCases(databases[0])) # 7: New daily confirmed cases
databases.append(getNewCases3dAv(databases[7])) #8: New confirmed cases trend (3 day average)
databases.append(getNewCases(databases[1])) # 9: Active cases daily variation
databases.append(getNewCases3dAv(databases[9])) # 10: Active cases variation trend (3 day average)
databases.append(getNewCases(databases[2])) # 11: New daily deaths
databases.append(getNewCases3dAv(databases[11])) # 12: New deaths cases trend (3 day average)
databases.append(getNewCases(databases[3])) # 13: New daily recovered cases
databases.append(getNewCases3dAv(databases[13])) # 14: Recovered cases trend (3 day average)
databases.append(getNewCases(databases[4])) # 15: Daily tests
databases.append(getNewCases3dAv(databases[15])) # 16: Test trend (3 day average)
databases.append(getRatios(databases[7], databases[15])) # 17: Positive tests ratio (positive/total)
databases.append(getRatios(databases[8], databases[16])) # 18: Positive tests ratio trend (3 day average)
databases.append(getRatios(databases[0], databases[4])) # 19: Cumulative positive tests ratio trend
databases.append(getLinearDuplicationTimes(databases[0], databases[7])) # 20: Linear duplication time
databases.append(getLinearDuplicationTimes3dAv(databases[0], databases[8])) # 21: Linear duplication time trend
databases.append(getLinearDuplicationTimes(databases[2], databases[11])) # 22: Linear deaths duplication time
databases.append(getLinearDuplicationTimes3dAv(databases[2], databases[12])) # 23: Linear deaths duplication trend
databases.append(getNewCases(databases[5])) # 24: New daily dropped cases
databases.append(getNewCases3dAv(databases[24])) # 25: New daily dropped cases trend
databases.append(getNewCases7dAv(databases[7])) # 26: New daily cases trend (7 days average)
databases.append(getNewCases7dAv(databases[9])) # 27: Active cases variation trend (7 days average)
databases.append(getNewCases7dAv(databases[11])) # 28: New deaths trend (7 days average)
databases.append(getNewCases7dAv(databases[13])) # 29: New recovered cases trend (7 days average)
databases.append(getNewCases7dAv(databases[15])) # 30: New tests trend (7 days average)
databases.append(getNewCases7dAv(databases[24])) # 31: New dropped cases trend (7 days average)
databases.append(getLinearDuplicationTimes7dAv(databases[0], databases[26])) # 32: Linear duplication time (7d)
databases.append(getLinearDuplicationTimes7dAv(databases[2], databases[28])) # 33: Linear deaths duplication time (7d)
databases.append(getRatios(databases[26], databases[30])) # 34: Positive tests ratio trend (7 day average)

print("Dataframes for data analysis were build...                       ", end="\n")

print("Saving data to csv files...", end="\r")
for d in range(len(databases)):
	datanumber = "{:02d}".format(d)
	databases[d].to_csv(datapath + "Argentina_COVID19_" + datanumber + "_" + dataTitles[d] + ".csv")
print("That's all. CSV files were saved.                          ", end="\n")