# Построение профиля лопатки

Веб-приложение предназначено для решения прикладных задач по проектированию направляющих и рабочих решёток лопаточных машин. Проект создан на языке [Python 3.9](https://www.python.org/downloads/release/python-390/) с использованием веб-фреймворка [Flask] и библиотеки визуализации [Plotly.js]. Приложение находится в стадии разработки.

## Содержание

- [Установка](#установка)
    - [Виртуальное окружение](#виртуальное-окружение)
    - [Зависимости](#зависимости)
- [Теоретическая сводка](#теоретическая-сводка)
    - [Основы геометрических построений профилей лопаток](#основы-геометрических-построений-профилей-лопаток)
- [Работа с программой](#работа-с-программой)
- [Дорожная карта](#дорожная-карта)
- [Лицензия](#лицензия)

## Установка

Для работы проекта необходим Python. Для клонирование кода необходимо в командной строке выполнить следующие команды:

```
git clone https://github.com/antonkurnukhin/turbineBladePlottingWebApp.git
cd turbineBladePlottingWebApp
```

### Виртуальное окружение

Веб-приложение предназначено для работы на удаленном сервере. По этой причине и для того, чтобы не загрязнять лишними пакетами корневые папки интерпретатора, целесообразно использовать виртуальное окружение. Установка виртуального окружения осуществляется следующей командой:

```
python -m venv venv
```

Активировать созданное виртуальное окружение можно следующей командой:

```
venv\Scripts\activate
```

### Зависимости

Для установки необходимых рабочих зависимостей необходимо выполнить следующую команду:

``` 
pip install -r requirements.txt
````

### Начало работы

После установки зависимостей, запуск веб-приложения осуществляется с помощью

``` 
python app.py
````

## Теоретическая сводка

TODO

### Основы геометрических построений профилей лопаток

TODO

## Работа с программой

TODO

## Дорожная карта

- [x] Функция расчёта геометрии профиля лопатки;
- [x] Flask-сервер;
- [x] Основные HTML-страницы;
- [x] Одновременное построение рабочего каскада (направляющий и рабочий венцы);
- [x] Функция расчёта треугольников скоростей;
- [ ] Добавления в HTML вкладок для отображения рабочего каскада, направляющей лопатки с основными обозначениями, рабочей лопатки с основными обозначениями, треугольников скоростей;
- [ ] Покрытие тестами и рефакторинг кода;
- [ ] Функция расчёта диффузорности/конфузорности межлопаточного канала;
- [ ] Функция определения рабочих параметров рассчитаного профиля.
- [ ] Документация пользователя и теоретическая сводка;
- [ ] bash-скрипты для развертывания на удаленном сервере.

## Лицензия

Данный проект является открытым для любого использования в соответствии с лицензией MIT.

## Контакты
<a href="https://spb.hh.ru/applicant/resumes/view?resume=88747db9ff0af782180039ed1f66576e306b43">
<img src="./static/logos/hh.png" alt="HH.ru" title="" align="left" width="40%" />
</a>
<a href="https://t.me/KurnukhinAnton">
<img src="./static/logos/tg.png" alt="Telegram" title="" align="right" width="40%" />
</a>