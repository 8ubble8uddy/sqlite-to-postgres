from psycopg2.extras import execute_batch

from services.extract import SQLiteExtractor
from services.load import PostgresLoader
from core.config import POSTGRES_PARAMS, RECORDS_SIZE, SQLITE_PARAMS
from db.postgres import get_postgres
from db.sqlite import get_sqlite


def sqlite_to_postgres(sqlite: SQLiteExtractor, postgres: PostgresLoader):
    """Основной метод загрузки данных из SQLite в Postgres.

    Args:
        sqlite: Извлекает данные из SQLite и преобразовывает их
        postgres: Загружает данные в PostgreSQL
    """
    for db_table, db_class in postgres.DATABASE:
        query = postgres.prepare_insert(db_table)
        sqlite.select_table(db_table, db_class.__dataclass_fields__)
        for records in sqlite.load_records(db_class, RECORDS_SIZE):
            execute_batch(postgres.curs, query, records)
            postgres.conn.commit()


def main():
    """Функция с основной логикой работы программы."""
    with get_sqlite(**SQLITE_PARAMS) as sqlite_conn:
        with get_postgres(**POSTGRES_PARAMS) as postgres_conn:
            sqlite_to_postgres(
                sqlite=SQLiteExtractor(sqlite_conn),
                postgres=PostgresLoader(postgres_conn),
            )


if __name__ == '__main__':
    main()
