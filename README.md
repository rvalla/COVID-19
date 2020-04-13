# Analysis and plotting of COVID-19 data

This is a very little piece of code in [Python](https://www.python.org) to analyse trough plots
the data in the [2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns
Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19) by regions. Or the data from [National
Reports](https://www.argentina.gob.ar/coronavirus/informe-diario) published in Argentina.

Data of the outbreak evolution in Argentina is taken from National Reports and then loaded on 
a spreadsheet (exported afterwards to a .csv). The structure of the data is similar to that
in [argcovidapi repository](https://github.com/mariano22/argcovidapi), updating content every
day and adding data about official testing. Note the above-mentioned reports have *confirmed*
and *deaths* cases separated by province but that is not the case with *recovered* cases and
*laboratory tests*. So, the *UNKNOWN* category was added.

If you want to plot worldwide data you need to download the Johns Hopkins repository...</br>

Then you need **Python 3** and this packages to use it:
- matplotlib
- pandas
- numpy

###With *COVID-19_Analysis.py*...
You can visualize the data from [2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns
Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19). Is possible to:
- Plot cases' data (confirmed cases, deaths, recovered patients) by date or
since _n_ case appearance.
- Use linear or logarithmic scales.
- Group data by country or study states/province data.
- Plot death rate evolution too.

###With *COVID-19_Ar_Analysis.py*...
You can visualize the data from National Reports published in Argentina. Is possible to:
- Plot cases' data (confirmed cases, deaths, recovered patients).
- Plot death rate evolution.
- See outbreak evolution in Argentina in a synthetic chart.
- Plot duplication time evolution (how many days would be need for total cases being duplicated).

Contact [rodrigovalla[at]yahoo.com.ar](mailto:rodrigovalla@yahoo.com.ar)