### **Как запустить тесты:**

Клонировать репозиторий и перейти внутри него в директорию ```/tests```:
```
git clone https://github.com/8ubble8uddy/sqlite-to-postgres.git
```
```
cd sqlite-to-postgres/tests/
```

Создать файл .env и добавить настройки для тестов:
```
nano .env
```
```
# PostgreSQL
POSTGRES_DB=movies_database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# SQLite
SQLITE_PATH=/opt/sqilte_to_postgres/db.sqlite
```

Развернуть и запустить тесты в контейнерах:
```
docker-compose up --build
```

### Автор: Герман Сизов