# Звіти по цінах на нерухомість
### Парсер цін на квартири

Парсер витягує інформацію про ціну на квартири для вторинного ринку з сайту [SV Development](http://www.svdevelopment.com/ua/web/flat_costs/).

### Загальна інформація
Парсер витягує дані починаючи від 2003 року до поточного місяця теперішнього року. Ціни доступні для міста в цілому а також окремо по районах міста і відсортовані по часу. Також генеруються звіти в папці `reports/` у вигляді CSV файлів та інтерактивних діаграм у вигляді HTML файлів.

> [!NOTE]
> Інформація про ціни на нерухомість доступна починаючи з 2003 року.
>
##### Приклад діаграми
<kbd>![Alt text](https://raw.githubusercontent.com/mykolasopushynskyy/realEstateReport/main/resources/example_result/diagram.png "Діаграма цін на квартири")</kbd>
- Прямі графіки позначають ціни в долларах США
- Переривчісті лінії позначають ціни в долларах США з поправкою на інфляцію
- Подвійний клік по діаграмі змінює масштаб на масштаб по замовчуванню
- Клікання по назві району на легенді ховає графік на діаграмі
- [Приклад результатів роботи програми](https://github.com/mykolasopushynskyy/realEstateReport/tree/main/resources/example_result)

### Міста для яких генеруються звіти
- Київ
- Дніпропетровськ
- Донецьк
- Львів
- Одеса
- Харків
### Запуск 
Для запуску запустіть скрипт `./application.py`. Можливе очікування кілька секунд для завантаження інформацї про інфляцію. У разі успішного виконання лог буде наступним.

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

### Ресурси використані в проєкті
1. [SV Development](http://www.svdevelopment.com/ua/web/flat_costs/) - джерело з якого береться статистика для звітів
2. [Plotly Python](https://plotly.com/python/) - бібліотека для генерування інтерактивних діаграм
3. [CPI library](https://pypi.org/project/cpi/) - бібліотека для підрахунку інфляції доллара США