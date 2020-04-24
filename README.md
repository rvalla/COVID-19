# Analysis and plotting of COVID-19 data

This is a very little piece of code in [Python](https://www.python.org) to analyse trough plots
the data in the [2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns
Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19) by regions. Or the data from [National
Reports](https://www.argentina.gob.ar/coronavirus/informe-diario) published in Argentina.

Data of the outbreak evolution in Argentina is taken from National Reports and then loaded on 
a spreadsheet (exported afterwards to a .csv). The structure of the data is similar to that
in [argcovidapi repository](https://github.com/mariano22/argcovidapi), updating content every
day and adding data about official testing and dropped cases. Note the above-mentioned reports have *confirmed*
and *deaths* cases separated by province but that is not the case with *recovered* cases and
*laboratory tests*. So, the *UNKNOWN* category was added.

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

### With *COVID-19_Ar_Analysis.py*...
You can visualize the data from National Reports published in Argentina. Is possible to:
- Plot cases' data (confirmed cases, deaths, recovered patients).
- Plot death rate evolution.
- See outbreak evolution in Argentina in a synthetic chart.
- Plot duplication time evolution (how many days would be need for total cases being duplicated).

### Definitions
In the charts that the code generates you will see a lot of categories. Pay attention to these descriptions
to know exactly what each one represents.
- Case: simply the word to indicate the event related to a potentially infected person
- Confirmed case: a case confirmed by the authorities
- Confirmed cases: number of cases confirmed so far
- Recovered case: a person who is no longer infected
- Revovered cases: number of recovered cases so far
- Active cases: confirmed cases - recovered cases
- Death case: a case which ended with death of the patient
- New cases: number of new cases registered on a day
- New cases trend: new cases for a day but taking 3 days average. Suppose there were 10 cases on Monday, 15 on
Tuesday and 25 on Wednesday... Then you have a new cases trend of 33.33 for Tuesday ((10+15+25)/3)
- Death rate: the ratio between deaths and confirmed cases (note that confirmed cases are less than actual cases
but we don't know them)
- Duplication speed: days needed to duplicate a cumulative cases until the day before if new cases per day remain constant
- Duplication speed tren: duplication speed taking 3 days average
 

Contact [rodrigovalla[at]yahoo.com.ar](mailto:rodrigovalla@yahoo.com.ar)