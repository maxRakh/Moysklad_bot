# Телеграм бот для работы с API сервиса "МойСклад"
Программа для работы с API сервиса "МойСклад". Реалазация через telegram бота на aiogram. 
- выгрузка остатков на складе по категориям 
- выгрузка всех остатков на складе
- выгрузка продаж за периоды

Далее будут добавляться новые функции.

### Установка и запуск:

1. Клонируйте репозиторий

`git clone https://github.com/maxRakh/Moysklad_bot.git`

2. Создайте виртуальное окружение и активируйте его

`virtualenv venv`

`source venv/bin/activate`

2. Установите зависимости

`pip install -r requirements.txt`

3. Создайте в папке main файл config.p
В нем необходимо прописать следующие переменные

`token_ms = "ваш_токен_от_МойСклад"`
`Получается в личном кабинете Мойсклад или по post запросу через API. Подробнее в документации МойСклад`

`token_tg = "tepegram_token"`
`Получается у BotFather`

`users = []`
`внуттри telegram id юзеров, которым планируете предоставить доступ к боту`