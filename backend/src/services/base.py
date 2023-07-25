class Config(object):
    """Класс с настройками для датакласса на основе pydantic."""

    arbitrary_types_allowed = True


class LoadTableError(Exception):
    """Ошибка при загрузке таблицы."""


class LoadDataError(Exception):
    """Ошибка при загрузке данных."""
