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
docker-compose exes back python3 manage.py migrate
docker-compose exes back python3 manage.py laod_data
docker-compose exec back python3 manage.py collectstatic --no-input
```
Проект должен быть доступен по http://localhost
Сервер также развернут по адресу: http://84.252.137.69/