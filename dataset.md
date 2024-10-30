## Описание данных

Данные получены путем скрапинга с официального сайти Центрального банка.

### Итоговая таблица

Сводная таблица [cbr-press-releases.csv]([https://storage.yandexcloud.net/cbr-press-release-classifier/cbr-press-releases.csv](https://storage.yandexcloud.net/cbr-press-release-classifier/cbr-press-releases.csv)) составлена на стадии препроцессинга и включает в себя данные из всех таблиц, полученных путем скрапинга. Содержит следующие столбцы:
- `date` - дата опубликования пресс-релиза;
- `link` - ссылка на пресс-релиз;
- `title` - заголовок пресс-релиза;
- `release` - текст пресс-релиза;
- `days_between` - количество дней прошедших до следующего релиза;
- `rate` - ключевая ставка утвержденная во время следующего заседания;
- `inflation` - значение инфляции в месяц следующего заседания (годовая);
- `usd` - курс доллара на день следующего заседания;
- `usd_cur_change_relative` - изменение курса доллара в день следующего заседания относительно дня текущего;
- `target_categorial` - изменение ключевой ставки на следующем заседании (-1 - уменьшена, 0 - без изменений, 1 - увеличена);
- `target_absolute` - абсолютное изменение ключевой ставки на следующем заседании (в процентах);
- `target_relative` - относительное изменение ключевой ставки утвержденной на следующем к ключевой ставке утвержденной на текущем заседании.


### Таблица процентных ставок

Таблица [key-rates-cbr.csv]([https://storage.yandexcloud.net/cbr-press-release-classifier/key-rates-cbr.csv](https://storage.yandexcloud.net/cbr-press-release-classifier/key-rates-cbr.csv)) содержит следующие столбцы:
- `date` - дата опубликования процентной ставки (как правило это следующий рабочий день после заседания);
- `rate` - величина процентной ставки;


### Таблица уровня инфляции

Таблица [inflation-cbr.csv]([https://storage.yandexcloud.net/cbr-press-release-classifier/inflation-cbr.csv](https://storage.yandexcloud.net/cbr-press-release-classifier/inflation-cbr.csv)) содержит следующие столбцы:
- `date_inflation` - отчетный месяц (mm.YYYY), на текущий месяц данные появляются в начале следующего;
- `inflation` - значение инфляции;


### Таблица значений курса доллара

Таблица [cur-usd-cbr.csv]([https://storage.yandexcloud.net/cbr-press-release-classifier/cur-usd-cbr.csv](https://storage.yandexcloud.net/cbr-press-release-classifier/cur-usd-cbr.csv)) содержит следующие столбцы:
- `date` - дата;
- `usd` - курс доллара;


### Таблица пресс-релизов

Таблица [raw-cbr-press-releases.csv]([https://storage.yandexcloud.net/cbr-press-release-classifier/raw-cbr-press-releases.csv](https://storage.yandexcloud.net/cbr-press-release-classifier/raw-cbr-press-releases.csv)) содержит следующие столбцы:
- `date` - дата опубликования пресс-релиза;
- `link` - ссылка на пресс-релиз;
- `title` - заголовок пресс-релиза;
- `release` - текст пресс-релиза;
