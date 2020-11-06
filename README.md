# Analysis and plotting of COVID-19 data

This is a very little piece of code in [Python](https://www.python.org) to analyse through plots
the data in the [2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns
Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19) by regions. Or the data from [National
Reports](https://www.argentina.gob.ar/coronavirus/informe-diario) published in Argentina.

Data of the outbreak evolution in Argentina is taken from National Reports and then loaded on
a spreadsheet (exported afterwards to a .csv). The structure of the data is similar to that
in [argcovidapi repository](https://github.com/mariano22/argcovidapi), I updated the data
within the week until September 21st adding data about official testing and dropped cases.
Note the above-mentioned reports have *confirmed* and *deaths* cases separated by province
but that is not the case with *recovered* cases and *laboratory tests*. So, the *UNKNOWN*
category was added.

If you want to plot worldwide data you need to download the Johns Hopkins repository...</br>

Then you need **Python 3** and this packages to use it:
- matplotlib
- pandas
- numpy

### With *COVID-19_Analysis.py*...
You can visualize the data from [2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns
Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19). Is possible to:
- Plot cases' data (confirmed cases, deaths, recovered patients) by date or
since _n_ case appearance.
- Use linear or logarithmic scales.
- Group data by country or study states/province data.
- Plot death rate evolution too.

### With *COVID-19_Ar_ProcessingData.py*...
You can load data on *Argentina.csv* and save information to a group of csv files then used by
*COVID-19_Ar_Analysis.py* to visualize it. The files are stored in *Argentina_Data/Processed_data*. That
files are updated every time I push new data to the repository.

### With *COVID-19_Ar_Analysis.py*...
You can visualize the data from National Reports published in Argentina. Is possible to:
- Plot cases' data (confirmed cases, deaths, recovered patients).
- Plot death rate evolution.
- See outbreak evolution in Argentina in a synthetic chart (that shows confirmed and active cases, deaths,
daily trends, laboratory tests and positive tests ratio among others).
- Plot duplication time evolution (how many days would be need for total cases being duplicated).
- Plot the confirmed cases distribution by day of the week.

### With *COVID-19_DataGobAr_TestsAnalysis.py*...
You can visualize the laboratory tests data published in
[datos.gob.ar](https://datos.gob.ar/dataset/salud-covid-19-determinaciones-registradas-republica-argentina).
Is possible to:
- Plot daily and cumulative tests by province.
- Plot daily and cumulative positive tests by province.
- Plot daily and cumulative positive test ratio (positive/total).

### Definitions
In the charts that the code generates you will see a lot of categories. Pay attention to these descriptions
to know exactly what each one represents.
- Case: simply the word to indicate the event related to a potentially infected person
- Confirmed case: a case confirmed by the authorities
- Confirmed cases: number of cases confirmed so far
- Recovered case: a person who is no longer infected
- Recovered cases: number of recovered cases so far
- Active cases: confirmed cases - recovered cases
- Death case: a case which ended with death of the patient
- New cases: number of new cases registered on a day
- New cases trend: new cases for a day but taking 3 days average. Suppose there were 10 cases on Monday, 15 on
Tuesday and 25 on Wednesday... Then you have a new cases trend of 33.33 for Tuesday ((10+15+25)/3)
- Death rate: the ratio between deaths and confirmed cases (note that confirmed cases are less than actual cases
but we don't know them)
- Duplication speed: days needed to duplicate a cumulative cases until the day before if new cases per day remain constant
- Duplication speed tren: duplication speed taking 3 days average

### Actual charts
If you don't want to run the code but are curious about the outbreak status in Argentina you can download
the charts in *Argentina_Data/actual_charts* folder.


Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
