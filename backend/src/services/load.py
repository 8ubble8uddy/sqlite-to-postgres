from typing import Dict, List

from psycopg2.extensions import connection as _connection
from psycopg2.extras import register_uuid
from pydantic.dataclasses import dataclass

from services.base import Config
from models.film_work import Filmwork
from models.genre import Genre, GenreFilmwork
from models.person import Person, PersonFilmwork


@dataclass(config=Config)
class PostgresLoader(object):
    """Класс для выполнения PostgreSQL-запросов."""

    conn: _connection

    DATABASE = [
        ('person', Person),
        ('genre', Genre),
        ('film_work', Filmwork),
        ('genre_film_work', GenreFilmwork),
        ('person_film_work', PersonFilmwork),
    ]

    def __post_init__(self):
        """При инициализации создаётся объект курсора для работы с базой данных."""
        self.curs = self.conn.cursor()

    def get_columns(self, table: str) -> List[str]:
        """Получение колонок таблицы базы данных.

        Args:
            table: Название таблицы

        Returns:
            List[str]: Список из названий колонок таблицы
        """
        query = """SELECT column_name from information_schema.columns
                WHERE table_name = '{table}' ORDER BY ordinal_position;"""
        self.curs.execute(query.format(table=table))
        return [row[0] for row in self.curs.fetchall()]

    def get_query_data(self, table: str, cnt_columns: int) -> Dict[str, str]:
        """Получение параметров для подготовки запроса вставки данных в таблицу.

        Args:
            table: Название таблицы
            cnt_columns: Количество колонок таблицы

        Returns:
            Dict[str, str]: Параметры запроса
        """
        params = ['${0}'.format(param) for param in range(1, cnt_columns + 1)]
        return {
            'table': table,
            'statement': '{0}_insert'.format(table),
            'params': ', '.join(params),
        }

    def get_insert_query(self, statement: str, columns: List[str]) -> str:
        """Получение запроса для вставки данных в таблицу.

        Args:
            statement: Название подготовленного оператора
            columns: Названия колонок таблицы

        Returns:
            str: Запрос для вставки данных
        """
        args = ['%({0})s'.format(name) for name in columns]
        query = 'EXECUTE {statement} ({args});'
        return query.format(statement=statement, args=', '.join(args))

    def prepare_insert(self, table: str) -> str:
        """Выполнение подготовки для вставки данных в таблицу.

        Args:
            table: Название таблицы

        Returns:
            str: Запрос для вставки данных
        """
        register_uuid()
        columns = self.get_columns(table)
        data = self.get_query_data(table, len(columns))
        query = """PREPARE {statement} AS
            INSERT INTO {table} VALUES({params})
            ON CONFLICT (id) DO NOTHING;"""
        self.curs.execute(query.format(**data))
        return self.get_insert_query(data['statement'], columns)
