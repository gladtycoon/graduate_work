# 📚 Library API

REST API для управления библиотекой.  
Проект выполнен в рамках дипломной работы.

---

## 🚀 Технологии

- Python 3.14
- Django 6.0.7
- Django REST Framework
- PostgreSQL
- JWT-авторизация (Simple JWT)
- Swagger (drf-yasg)
- Docker & Docker Compose
- Pytest (тесты)

---

## 📦 Установка и запуск

### Локально

1. **Клонировать репозиторий:**
   ```bash
   git clone https://github.com/gladtycoon/graduate_work.git
   cd graduate_work

2. **Установить Poetry (если ещё нет):**
    ```bash
   pip install poetry
   
3. **Установить зависимости:**
    ```bash
   poetry install
   
4. **Активировать виртуальное окружение:**
    ```bash
   source .venv/bin/activate  # Linux/Mac
    .venv\Scripts\activate     # Windows
   
5. **Настроить переменные окружения:

    ```bash
    SECRET_KEY=
    DEBUG=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_HOST=
    DB_PORT=
   
6. **Настроить переменные окружения:**
    ```bash
    python manage.py migrate

7. **Загрузить тестовые данные:**
    ```bash
    python manage.py loaddata fixtures/initial_data.json
   
8. **Запустить сервер:**
    ```bash
    python manage.py runserver

## 📌 API Эндпоинты
```bash
    Метод	URL	        Описание
    
    POST	/api/register/	Регистрация пользователя
    POST	/api/login/	Получение JWT токена
    GET	        /api/books/	Список книг
    POST	/api/books/	Создать книгу
    GET	        /api/authors/	Список авторов
    GET	        /api/borrow/	Список выдач
    POST	/api/borrow/	Выдать книгу
```

## 🐳 Запуск через Docker
**Сборка и запуск:**
```bash
  docker-compose up --build
```
**Остановка:**
```bash
  docker-compose down
```

## 📖 Документация API
```bash 
    Swagger UI: http://127.0.0.1:8000/swagger/
    Redoc: http://127.0.0.1:8000/redoc/
```
## 🧪 Тесты
```bash
    python manage.py test
```

## 📄 Лицензия
```bash 
   MIT
```


