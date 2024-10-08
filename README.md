# Телеграм бот для отправки уведомлений о проверке работ

Телеграм бот, собирающий информацию о состоянии сданных на проверку работ на курсе по программированию от [Devman](https://dvmn.org)
Бот использует имеющийся API и long polling для менее агрессивного парсинга. 

## Запуск

Для запуска бота вам понадобится Python версии 3.10.

Скачайте код с GitHub. Установите зависимости:

```sh
pip install -r requirements.txt
```
Запустить бота:
```sh
python main.py
```

### Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 4 переменные:
 - `DVMN_TOKEN`= Ваш токен на курсе, можно найти в личном кабинете, после регистрации
 - `DVMN_API_TIMEOUT`= Количество секунд до таймаута по long polling, перед отправкой нового сообщения.
 - `TELEGRAM_BOT_TOKEN`= Токен вашего телеграм бота (можно узнать у [@BotFather](https://t.me/botfather))
 - `TG_CHAT_ID`= Ваш ID в телеграм (ID можно узнать у [@userinfobot](https://t.me/userinfobot))

## Для запуска с помощью Docker
 - Необходимо установить Docker
 - Загрузить содержимое репозитория на локальный диск
 - Создать файл с указанными локальными переменными `.env`
 - C помощью терминала перейти в директорию с проектом
 - Создать Docker образ командой:
```sh
docker build -t homework-bot .
```
 - Запустить образ командой:
```sh
docker run homework-bot
```
Если файл с переменными окружения на момент создания образа находился/находится 
не в директории с проектом, то необходимо явно указать путь до файла в команде запуска:
```sh
docker run --env-file=C:\env_files\.env homework-bot
```

## Цели проекта

Код написан в учебных целях — для курса по Python и веб-разработке на сайте [Devman](https://dvmn.org).
