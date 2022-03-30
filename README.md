## Бот для отправки уведомлений о проверенных работах [devman.org](devman.org) в Telegram

Бот создан в учебных целях для отправки уведомлений о проверенных домашних работах в telegram

### Как установать?

Вам понадобится установленный Python 3.6-3.9, аккаунт в telegram и git.

Склонируйте репозиторий или скачайте код в виде архива:
```bash
$ git clone git@github.com:IlyaG96/devman_homework_bot.git
```

Создайте в этой папке виртуальное окружение:
```bash
$ python3 -m venv [полный путь до папки devman_homework_bot] env
```

Активируйте виртуальное окружение и установите все необходимые пакеты:
```bash
$ cd devman_homework_bot
$ source env/bin/activate
$ pip install -r requirements.txt
```
### Использование
Заполните прилагающийся .env.example файл и переименуйте его в .env или иным образом задайте переменные среды:

```bash
DEVMAN_TOKEN=""
TG_TOKEN=""
CHAT_ID=""
```

- `DEVMAN_TOKEN` - есть [здесь](https://dvmn.org/api/docs/)
- `TG_TOKEN` - токен бота teleram - написать *@botfather*
- `CHAT_ID` - ваш telegram id, нужен для отправки сообщения именно вам - написать *@userinfobot*
Простейший способ запустить бота
```bash
$ python request_to_devman.py
```
Если одна из ваших работ будет проверена в тот момент, когда бот запущен, вы получите в телеграм следующего вида:
- Если есть ошибки:
```text
Ваш урок 'Джедайские техники рассылки спама' проверен. К сожалению, есть ошибки
Ссылка для перехода к уроку: https://dvmn.org/modules/mac-linux-command-line/lesson/mail-config/
```
- Если нет ошибок:
```text
Ваш урок 'Джедайские техники рассылки спама' проверен. Ошибок нет! Поздравляем!
Ссылка для перехода к уроку: https://dvmn.org/modules/mac-linux-command-line/lesson/mail-config/
```

### Деплой на [heroku.com](https://heroku.com)
**По материалам уроков [devman.org](devman.org)**

- Для того, чтобы бот работал, его необходимо разместить на сервере. Зарегистрируйтесь 
[Здесь](https://id.heroku.com/login) для того, чтобы получить бесплатный сервер
- Создайте в папке с ботом файл Procfile c содержимым:
- ```bot: python3 название_бота.py```
- Убедитесь, что файл requirements.txt есть в папке и заполнен
- Опубликуйте свой код на [github.com](https://github.com)
- Привяжите аккаунт GitHub к аккаунту Heroku и нажмёте Deploy Branch внизу страницы. Загорятся зелёные галочки справа, как на скриншоте.
- ![](https://dvmn.org/media/photo_2019-04-25_17-01-15.jpg)
- Переменные окружения можно задать во вкладке Settings на сайте Heroku. Заполните Config Vars в соответствии с примером из env.example
- Убедитесь, что бот работает. Установите Heroku CLI [инструкция](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
- Просмотрите логи командой 
- ```heroku logs -a название_приложения``` 
- Кроме логов, вы должны наблюдать надпись **Build succeeded**  

В данной версии каждые 90 секунд бут будет писать в лог крайне информативные сообщения о том, что он жив и пытается достучаться до сайта


### Запуск с использованием Docker

```shell
docker build -t devman-homework .
docker run --rm -v 'pwd' -d devman-homework
```
