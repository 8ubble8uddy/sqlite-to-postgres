import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Set, Tuple, Union

import psycopg2
import pytest
from psycopg2.extensions import cursor as _cursor

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = os.environ.get('SQLITE_PATH', BASE_DIR / 'infra' /  'data' / 'db.sqlite')

DSL = MappingProxyType(
    {
        'dbname': os.environ.get('POSTGRES_DB', 'movies_database'),
        'user': os.environ.get('POSTGRES_USER', 'postgres'),
        'password': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'host': os.environ.get('POSTGRES_HOST', '127.0.0.1'),
        'port': os.environ.get('POSTGRES_PORT', '5432'),
        'options': '-c search_path=content',
    },
)

EXCLUDED_COLUMNS = ('created', 'modified', 'created_at', 'updated_at')


@dataclass
class CheckConsistency(object):
    """Класс для получения данных таблиц."""

    curs: Union[sqlite3.Cursor, _cursor]

    def count_records(self, table: str) -> int:
        """Вычисление количество записей таблицы.

        Args:
            table: Название таблицы

        Returns:
            int: Количество записей
        """
        query = 'SELECT COUNT(*) FROM {table};'
        self.curs.execute(query.format(table=table))
        data = self.curs.fetchone()
        return data[0] if isinstance(data, tuple) else 0

    def get_columns(self, table: str) -> str:
        """Получение колонок за исключением колонок создания и обновления записи.

        Args:
            table: Название таблицы

        Returns:
            str: Список колонок
        """
        query = 'SELECT * FROM {table} LIMIT 1;'
        self.curs.execute(query.format(table=table))
        columns = self.curs.description
        return ', '.join(
            name[0] for name in columns if name[0] not in EXCLUDED_COLUMNS
        )

    def all_data(self, table: str) -> Set[Tuple]:
        """Получение данных таблицы за исключением пустых значений.

        Args:
            table: Название таблицы

        Returns:
            Set[Tuple]: Записи таблицы
        """
        columns = self.get_columns(table)
        query = 'SELECT {columns} FROM {table};'
        self.curs.execute(query.format(table=table, columns=columns))
        return {tuple(filter(None, row)) for row in self.curs.fetchall()}


@pytest.fixture
def sqlite():
    """Фикстура базы данных SQLite."""
    conn = sqlite3.connect(DB_PATH)
    curs = conn.cursor()
    yield CheckConsistency(curs)
    conn.close()


@pytest.fixture
def postgres():
    """Фикстура базы данных PostgreSQL."""
    conn = psycopg2.connect(**DSL)
    curs = conn.cursor()
    yield CheckConsistency(curs)
    conn.close()


@pytest.mark.parametrize(
    'table', [
        'genre',
        'film_work',
        'person',
        'genre_film_work',
        'person_film_work',
    ]
)
def test_count_records(sqlite: CheckConsistency, postgres: CheckConsistency, table: str):
    """Проверка количества записей между каждой парой таблиц в SQLite и Postgres.

    Args:
        sqlite: БД SQLite
        postgres: БД PostgreSQL
        table: Название таблицы
    """
    assert sqlite.count_records(table) == postgres.count_records(table)


@pytest.mark.parametrize(
    'table', [
        'genre',
        'film_work',
        'person',
        'genre_film_work',
        'person_film_work',
    ]
)
def test_all_data(sqlite: CheckConsistency, postgres: CheckConsistency, table: str):
    """Проверка содержимого записей внутри каждой таблицы между SQLite и Postgres.

    Args:
        sqlite: БД SQLite
        postgres: БД PostgreSQL
        table: Название таблицы
    """
    assert sqlite.all_data(table) == postgres.all_data(table)
