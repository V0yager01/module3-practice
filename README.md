# VideoApp
## Описание
Backend проект, предоставляющий api для работы с видеофайлами.

## Запуcк
### Клонируйте репозиторий
```
git clone git@github.com:V0yager01/module3-practice.git
```
### Подготовка виртуального окружения
Создаем окружения для проекта. Указываем данные для входа в postgres
```
sudo nano .env
```
```
SECRET_KEY=secretkey
NAME=example
USER=example
PASSWORD=example
HOST=db
PORT=5432
```

### Запуск Docker compose 
В директории проекта запускаем docker-compose.yml
```
sudo docker compose up -f docker-compose.yml up -d
```

# Функционал 
Доступно добавление/редактирование видео и видеофайлов через админку.

Доступны пути
```
"/v1/videos/{video.id}/"
"/v1/videos/"
"/v1/videos/{video.id}/likes/"
"/v1/videos/ids/"
"/v1/videos/statistics-subquery/"
"/v1/videos/statistics-group-by/"
```
