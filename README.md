## SQLite to PostgreSQL

[![python](https://img.shields.io/static/v1?label=python&message=3.8%20|%203.9%20|%203.10&color=informational)](https://github.com/8ubble8uddy/sqlite-to-postgres/actions/workflows/main.yml)
[![dockerfile](https://img.shields.io/static/v1?label=dockerfile&message=published&color=2CB3E8)](https://hub.docker.com/r/8ubble8uddy/sqlite_to_postgres)
[![last updated](https://img.shields.io/static/v1?label=last%20updated&message=july%202022&color=yellow)](https://img.shields.io/static/v1?label=last%20updated&message=july%202022&color=yellow)
[![lint](https://img.shields.io/static/v1?label=lint&message=flake8%20|%20mypy&color=brightgreen)](https://github.com/8ubble8uddy/sqlite-to-postgres/actions/workflows/main.yml)
[![code style](https://img.shields.io/static/v1?label=code%20style&message=WPS&color=orange)](https://wemake-python-styleguide.readthedocs.io/en/latest/)
[![tests](https://img.shields.io/static/v1?label=tests&message=%E2%9C%94%2010%20|%20%E2%9C%98%200&color=critical)](https://github.com/8ubble8uddy/sqlite-to-postgres/actions/workflows/main.yml)

### **Описание**

_Целью данного проекта является реализация скрипта на [Python](https://www.python.org) для миграции данных из [SQLite](https://sqlite.org) в [PostgreSQL](https://www.postgresql.org). Данные содержат информацию о фильмах, персонах и жанрах. В коде используются dataclass, менеджеры контекста для установки и закрытия соединений и есть обработка ошибок записи и чтения. Для проверки целостности данных между таблицами двух БД используется [pytest](https://pytest.org)._

### **Технологии**

```Python``` ```SQLite``` ```PostgreSQL``` ```PyTest``` ```Pydantic``` ```Docker```

### **Как запустить проект:**

Клонировать репозиторий и перейти внутри него в директорию ```/infra```:
```
git clone https://github.com/8ubble8uddy/sqlite-to-postgres.git
```
```
cd sqlite-to-postgres/infra/
```

Создать файл .env и добавить настройки для проекта:
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

Развернуть и запустить проект в контейнерах:
```
docker-compose up
```

Вместе с PostgreSQL запускается связанная с ней админ-панель [pgAdmin](https://www.pgadmin.org):
```
http://127.0.0.1:5050
```

### Автор: Герман Сизов