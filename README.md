# Foodgram
![example workflow](https://github.com/AlexanderZug/foodgram-project-react/actions/workflows/main.yml/badge.svg)


![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)
![](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=Postman&logoColor=white)
![](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

Foodgram - проект, выполненный в рамках обучения в Яндекс Практикуме. Проект позволяет:

- Просматривать рецепты
- Добавлять рецепты в избранное
- Публикование рецепты
- Удалять собственные рецепты или редактировать их
- Скачивать список покупок

## Установка и запуск в docker-compose

Создайте и заполните .env файл в дериктории infra своими данными:
```
# указываем, с какой БД работаем
DB_ENGINE=django.db.backends.postgresql
# имя базы данных
DB_NAME=
# логин для подключения к базе данных
POSTGRES_USER=
# пароль для подключения к БД (установите свой)
POSTGRES_PASSWORD=
# название сервиса (контейнера)
DB_HOST=
# порт для подключения к БД
DB_PORT=
# секретный код приложения
SECRET_KEY=
```

Клонировать репозиторий и перейти в директорию infra:

```
git clone https://github.com/AlexanderZug/foodgram-project-react.git
```

```
cd foodgram-project-react/infra
```
Запустить команду сборки контейнера:

```
docker-compose -d --build
```

Выполнить внутри контейнера миграции, заполнить БД данными и собрать статику:
```
docker-compose exeс back python3 manage.py migrate
docker-compose exeс back python3 manage.py load_data
docker-compose exec back python3 manage.py collectstatic --no-input
```

Проект должен быть доступен по http://localhost, документацию к проекту 
можно будет найти по адресу http://localhost/api/docs/ 

Сервер также развернут по адресу: http://84.252.137.69/