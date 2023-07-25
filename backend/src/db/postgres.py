from contextlib import contextmanager
from typing import Iterator

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from pydantic import BaseSettings, Field


@contextmanager
def get_postgres(**dsn) -> Iterator[_connection]:
    """
    Функция с контекстным менеджером для подключении к базе данных SQLite.

    Args:
        dsn: Параметры для подключения к базе данных (Data Source Name)

    Yields:
        _connection: Соединение с базой данных
    """
    conn = psycopg2.connect(**dsn)
    conn.cursor_factory = DictCursor
    yield conn
    conn.close()


class PostgresSettings(BaseSettings):
    """Класс для валидации настроек подключения к PostgreSQL."""

    dbname: str = Field(env='postgres_db', default='movies_database')
    user: str = Field(env='postgres_user', default='postgres')
    password: str = Field(env='postgres_password', default='postgres')
    host: str = Field(env='postgres_host', default='127.0.0.1')
    port: int = Field(env='postgres_port', default='5432')
    options: str = Field(default='-c search_path=content')
