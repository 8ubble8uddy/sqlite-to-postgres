import sqlite3
from typing import Dict, Iterator, List

from pydantic.dataclasses import dataclass

from services.base import Config, LoadDataError, LoadTableError
from core.logger import logger


@dataclass(config=Config)
class SQLiteExtractor(object):
    """Класс для выполнения SQLite-запросов."""

    conn: sqlite3.Connection

    def __post_init__(self):
        """При инициализации создаётся объект курсора для работы с базой данных."""
        self.curs = self.conn.cursor()

    def get_columns(self, table: str, cls_fields: Dict) -> str:
        """Получение колонок таблицы, которые есть в полях класса данных.

        Args:
            table: Название таблицы
            cls_fields: Поля класса данных

        Returns:
            str: Названия колонок таблицы
        """
        query = 'PRAGMA table_info({table});'
        self.curs.execute(query.format(table=table))
        columns = [column['name'] for column in self.curs.fetchall()]
        return ', '.join(name for name in columns if name in cls_fields)

    def select_table(self, table: str, cls_fields: Dict):
        """Запрашивает таблицу базы данных.

        Args:
            table: Название таблицы
            cls_fields: Поля класса данных

        Raises:
            LoadTableError: Ошибка при загрузке таблицы
        """
        query = 'SELECT {columns} FROM {table};'
        try:
            self.curs.execute(
                query.format(
                    table=table,
                    columns=self.get_columns(table, cls_fields),
                ),
            )
        except sqlite3.OperationalError as error:
            message = str(error)
            if message == 'no such table: {0}'.format(table):
                logger.error('Таблица {0} не найдена!'.format(table))
            elif message == 'near "FROM": syntax error':
                logger.error(
                    'В таблице {0} нет полей {1}!'.format(table, *cls_fields),
                )
            raise LoadTableError(error)

    def get_object(self, row: sqlite3.Row, db_class: type) -> Dict:
        """Приведение строки таблицы в объект класса данных.

        Args:
            row: Строка таблицы
            db_class: Класс данных

        Raises:
            LoadDataError: Ошибка при загрузке данных

        Returns:
            Dict: Объект класса данных в виде словаря
        """
        try:
            obj = db_class(**row)
        except TypeError as error:
            required_field = str(error).split()[-1]
            logger.error(
                'В строке нет обязательного поля {0}!'.format(required_field),
            )
            raise LoadDataError(error)
        return obj.__dict__

    def load_records(self, db_class: type, size: int) -> Iterator[List[Dict]]:
        """Загрузка данных пачками в установленном размере `size`.

        Args:
            db_class: Класс данных
            size: Размер пачки данных

        Yields:
            Iterator[List[Dict]]: Итератор со списком объектов базы данных
        """
        logger.info('Загрузка таблицы {0}'.format(db_class.__name__))
        while data := self.curs.fetchmany(size):
            yield [self.get_object(row, db_class) for row in data]
        logger.info('Данные успешно загружены!')
