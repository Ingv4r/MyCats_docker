# Мои кошки
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
## Описание проектов
Мои кошки - это проект, на котором люди могут делиться с другими своими кошками. Можно регистрироваться, загружать картинки, описывать внешность, имя и достижения своих котиков. 

Taski - площадка, где можно вести свои задачи, описывать их и следить за ходом выполнения.
# Настройка SSH для дотупа к удаленному серверму
## Переход в закрытую директорию .ssh и создание директории для ssh ключей
```
cd ~/.ssh
mkdir название-директории

```
## Установление прав доступа к ssh ключам
Устанавливаем права доступа для файла закрытого SSH-ключа: владелец файла может читать и редактировать его, для других пользователей доступ к файлу закрыт.
```
chmod 600 название_файла_закрытого_SSH-ключа
```
Устанавливаем права доступа для файла открытого SSH-ключа: владелец файла может читать и редактировать его, остальные пользователи — только читать.
```
chmod 644 название_файла_открытого_SSH-ключа.pub
```
# Подключение к удаленному серверу
Ключ -i позволяет указать путь до SSH-ключа, отличный от пути по умолчанию.
```
ssh -i путь_до_файла_с_SSH_ключом/название_файла_закрытого_SSH-ключа login@ip(серевера)
```
Далее нужно ввести пароль от закрытого SSH-ключа (passphrase)
# Запуск backend
```
git clone git@github.com:Ingv4r/infra_sprint1.git
```
```
cd infra_sprint
```
- Cоздать и активировать виртуальное окружение
```
python -m venv venv # Для Windows
python3 -m venv venv # Для Linux и macOS
```
```
source venv/Scripts/activate # Для Windows
source venv/bin/activate # Для Linux и macOS
```
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Перейти в папку со скриптом управления и выполнить миграции
```
cd api_yamdb
```
```
python manage.py migrate
```

- Запустить проект
```
python manage.py runserver
```
## Создание суперпользователя
- В директории с файлом manage.py выполнить команду
```
python manage.py createsuperuser
```
- Заполнить поля в терминале
```
Username: <ваше_имя>
Email address: <ваш_email>
Password: <ваш_пароль>
Password (again): <ваш_пароль>
```
# Запуск frontend
## Установка на сревре пакетного менеджера npm
```
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - &&\
sudo apt-get install -y nodejs
```
## Установка зависимостей для frontend
```
cd taski/frontend
npm i
```
## Запуск фронта
```
npm run start
```
# Установка и запуск WSGI-сервера Gunicorn
Из виртуального окружения backend проекта выполнить устновка gunicorn
```
pip install gunicorn==20.1.0
```
## Создание юнита gunicorn
Создать и открыть через nano файл .service
```
sudo nano /etc/systemd/system/gunicorn.service 
```
Описать конфигурацию gunicorn
```
[Unit]
Description=gunicorn daemon 

# Условие: при старте операционной системы запускать процесс только после того, 
# как операционная система загрузится и настроит подключение к сети.
# Ссылка на документацию с возможными вариантами значений 
# https://systemd.io/NETWORK_ONLINE/
After=network.target 

[Service]
# От чьего имени будет происходить запуск:
# укажите имя, под которым вы подключались к серверу.
User=yc-user 

# Путь к директории проекта:
# /home/<имя-пользователя-в-системе>/
# <директория-с-проектом>/<директория-с-файлом-manage.py>/.
# Например:
WorkingDirectory=/home/yc-user/taski/backend/

# Команду, которую вы запускали руками, теперь будет запускать systemd:
# /home/<имя-пользователя-в-системе>/
# <директория-с-проектом>/<путь-до-gunicorn-в-виртуальном-окружении> --bind 0.0.0.0:8000 backend.wsgi
ExecStart=/home/yc-user/taski/backend/venv/bin/gunicorn --bind 0.0.0.0:8000 backend.wsgi

[Install]
# В этом параметре указывается вариант запуска процесса.
# Значение <multi-user.target> указывают, чтобы systemd запустил процесс,
# доступный всем пользователям и без графического интерфейса.
WantedBy=multi-user.target
```
Запуск и добавление в автозагрузку gunicorn
```
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```
# Установка и настройка веб-сервера Nginx
Установка Nginx на удаленный сервер
```
sudo apt install nginx -y
```
Открытие портов 80 и 442 для Nginx и 22 порт для SSH
```
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
```
Активация ufv файрвола
```
sudo ufw enable
```
## Настройка Nginx
Перейти в директорию taski/frontend и выполните команду:
```
npm run build
```
Скопировать папку /frontend/build/ в системную директорию Nginx /var/www/
```
# Команда cp — копировать, ключ -r — рекурсивно, включая вложенные папки и файлы.
sudo cp -r /home/yc-user/taski/frontend/build/. /var/www/taski/ 
# Точка после build важна — будет скопировано содержимое директории.
```
Открыть через nano файл конфигурации Nginx
```
sudo nano /etc/nginx/sites-enabled/default
```
Вставить код из листинга:
```
server {
    server_name ing-taski.ddns.net;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
    }

    location / {
        root   /var/www/taski;
        index  index.html index.htm;
        try_files $uri /index.html;
    }


    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/ing-taski.ddns.net/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/ing-taski.ddns.net/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}
server {
    if ($host = ing-taski.ddns.net) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    server_name 158.160.23.165 ing-taski.ddns.net;
    return 404; # managed by Certbot

}

server {
    server_name ing-kittygram.ddns.net;

    location /api/ {
        proxy_pass http://127.0.0.1:8080;
        client_max_body_size 20M;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8080;
        client_max_body_size 20M;
    }

    location /media/ {
        alias /var/www/kittygram/media/;
    }

    location / {
        root   /var/www/kittygram;
        index  index.html index.htm;
        try_files $uri /index.html;
    }



    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/ing-kittygram.ddns.net/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/ing-kittygram.ddns.net/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {
    if ($host = ing-kittygram.ddns.net) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    server_name ing-kittygram.ddns.net;
    listen 80;
    return 404; # managed by Certbot

}
```
Проверка файла на ошибки
```
sudo nginx -t
```
Перезагрузить конфигурацию Nginx
```
sudo systemctl reload nginx
```
