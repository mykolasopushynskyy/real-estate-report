# Real Estate Price Reports
### Condo Price Parser

The parser extracts information about apartment prices for the secondary market from the [SV Development](http://www.svdevelopment.com/ua/web/flat_costs/) site.

### General Information
The parser extracts data starting from 2003 up to the current month of the current year. Prices are available for the city as a whole and also separately by city districts, sorted by time. Reports are generated in the reports/ folder in the form of CSV files and interactive charts in the form of HTML files.
> [!NOTE]
> Real estate price information is available starting from 2003.
>
##### Example Chart
<kbd>![Alt text](https://raw.githubusercontent.com/mykolasopushynskyy/realEstateReport/main/resources/example_result/diagram.png "Діаграма цін на квартири")</kbd>
- Solid lines represent prices in USD
- Dashed lines represent prices in USD adjusted for inflation
- Double-clicking on the chart resets the zoom to the default scale
- Clicking on a district name in the legend hides its chart on the diagram
- [Example of program output](https://github.com/mykolasopushynskyy/realEstateReport/tree/main/resources/example_result)

### Cities for Which Reports Are Generated
- Київ
- Дніпропетровськ
- Донецьк
- Львів
- Одеса
- Харків
### Running the Parser
To run the parser, execute the ./application.py script. It may take a few seconds to load inflation information. If the execution is successful, the log will look like this:

```logs
Starting price parsing for cities: ['донецьк', 'одеса', 'львів', 'дніпропетровськ', 'харків', 'київ']

0:00:19 ［■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■］ 100% [ 2024 / 2024 ] Донецьк
	- CSV  report for city Донецьк: <project_path>/reports/донецьк-06-2024.csv
	- HTML report for city Донецьк: <project_path>/reports/донецьк-06-2024.html

0:00:18 ［■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■］ 100% [ 2024 / 2024 ] Одеса
	- CSV  report for city Одеса: <project_path>/reports/одеса-06-2024.csv
	- HTML report for city Одеса: <project_path>/reports/одеса-06-2024.html

0:00:18 ［■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■］ 100% [ 2024 / 2024 ] Львів
	- CSV  report for city Львів: <project_path>/reports/львів-06-2024.csv
	- HTML report for city Львів: <project_path>/reports/львів-06-2024.html

0:00:19 ［■■■■■■■■■■■■■■■■■■■■■■■■■■■■］ 100% [ 2024 / 2024 ] Дніпропетровськ
	- CSV  report for city Дніпропетровськ: <project_path>/reports/дніпропетровськ-06-2024.csv
	- HTML report for city Дніпропетровськ: <project_path>/reports/дніпропетровськ-06-2024.html

0:00:20 ［■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■］ 100% [ 2024 / 2024 ] Харків
	- CSV  report for city Харків: <project_path>/reports/харків-06-2024.csv
	- HTML report for city Харків: <project_path>/reports/харків-06-2024.html

0:00:19 ［■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■］ 100% [ 2024 / 2024 ] Київ
	- CSV  report for city Київ: <project_path>/reports/київ-06-2024.csv
	- HTML report for city Київ: <project_path>/reports/київ-06-2024.html

```

### Resources Used in the Project
1. [SV Development](http://www.svdevelopment.com/ua/web/flat_costs/) - the source from which statistics for the reports are taken
2. [Plotly Python](https://plotly.com/python/) - a library for generating interactive charts
3. [CPI library](https://pypi.org/project/cpi/) - a library for calculating USD inflation