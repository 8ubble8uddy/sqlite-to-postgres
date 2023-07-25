import sqlite3
from contextlib import contextmanager
from typing import Iterator

from pydantic import BaseSettings, Field


@contextmanager
def get_sqlite(db_path: str) -> Iterator[sqlite3.Connection]:
    """
    Функция с контекстным менеджером для подключении к базе данных SQLite.

    Args:
        db_path: Путь к файлу с базой данных

    Yields:
        sqlite3.Connection: Соединение с базой данных
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


class SQLiteSettings(BaseSettings):
    """Класс для валидации настроек подключения к SQLite."""

    db_path: str = Field(env='sqlite_path', default='../../infra/data/db.sqlite')
