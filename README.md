# Cultural_compass

Cultural_compass - API приложение для сбора отзывов о книгах, фильмах, музыке. Реализованы команды для автоматического импорта данных из файла .csv в базу
данных.

Социальная сеть позволяет:
- создавать учетную запись;
- авторизированным пользователям публиковать посты, осуществлять подписку на авторов, оставлять комментарии к посту;
- авторам удалять или редактировать свои посты или комментарии;
- просмотр информации о посте или комментарии неавторизированным пользователям.
  
Данный интерфейс позволяет осуществлять передачу данных в формате JSON в любое приложение или на фронтенд, что дает возможность организовать работу мобильного приложения или чат-бот.

### Технологии
[![Python](https://img.shields.io/badge/-Python3.9-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-3.2-blue?logo=django)](https://www.djangoproject.com/)
[![Django](https://img.shields.io/badge/django--rest--framework-3.12.4-blue?)](https://www.django-rest-framework.org/)
[![Django](https://img.shields.io/badge/Simple_JWT-5.2.2-blue?)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
[![Django](https://img.shields.io/badge/Djoser-2.2.0-blue?)](https://djoser.readthedocs.io/en/latest/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0.3-blue?)](https://pandas.pydata.org/)

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Tatiana314/Cultural_compass.git && cd Cultural_compass 
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
Linux/macOS: source env/bin/activate
windows: source env/scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
В директории Cultural_compass создать и заполнить файл .env:
```
touch .env

SECRET_KEY='Секретный ключ'
ALLOWED_HOSTS='Имя или IP хоста'
DEBUG=True
```
Выполнить миграции и запустить проект:
```
python api_yamdb/manage.py migrate && python api_yamdb/manage.py runserver
```

Документация для API доступна по адресу http://127.0.0.1:8000/redoc/. 
Документация представлена в формате Redoc.

### Пример:
```
GET запрос http://127.0.0.1:8000/api/v1/posts/
```
<img width="364" alt="код" src="https://github.com/Tatiana314/api_final_yatube/assets/124789269/52ce389b-04dd-4ef6-b4ea-3953e2a540ef">

## Автор
[Мусатова Татьяна](https://github.com/Tatiana314)


Проект предназначен для публикаций произведений, на которые можно оставлять отзывы и добавлять рейтинг, а также комментировать эти отзывы. Пользователи могут регистрироваться на сайте, создавать профиль, добавлять свои произведения и просматривать произведения других пользователей. Кроме того, пользователи могут оставлять отзывы и ставить рейтинги произведениям других пользователей.

# Установка
Для запуска проекта сначала необходимо установить Python 3 и Django. Для установки выполните следующие команды:

```
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install django
```

После установки Django выполните команду: **pip install pandas.**

# Запуск проекта
Для запуска проекта на локальном сервере выполните следующие команды:

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

# Команды управления Django
Реализованы две пользовательские команды управления Django:

python manage.py dataimport <имя модели> <путь к файлу с данными> - импорт данных из файла .csv в базу данных.
python manage.py dataimportall - заполнение базы данных данными из файлов: users.csv, titles.csv, category.csv, genre.csv, genretitle.csv, review.csv, comments.csv. Данные файла расположены в директории static/data.

# Используемые технологии
- Python 3
- Django
- HTML
- CSS
- JavaScript
- Pandas
