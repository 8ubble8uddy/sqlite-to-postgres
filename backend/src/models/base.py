import time
from datetime import datetime
from typing import Any, ClassVar
from uuid import UUID

from pydantic import validator
from pydantic.dataclasses import dataclass
from pydantic.fields import ModelField

MILLISECOND_DELAY = 0.001


@dataclass
class BaseDataclass(object):
    """Базовый класс данных."""

    id: UUID
    __dataclass_fields__: ClassVar[dict]

    def __post_init__(self):
        """После инициализации класса делается задержка в миллисекунду для сортировки данных по времени загрузки."""
        time.sleep(MILLISECOND_DELAY)
        class_name = type(self).__name__
        if class_name in {'Person', 'Genre', 'Filmwork'}:
            self.modified = datetime.utcnow()
        self.created = datetime.utcnow()

    @validator('*', pre=True)
    def change_none_to_default(cls, value: Any, field: ModelField) -> Any:
        """
        Валидатор для получения значения по умолчанию в случае передачи None в поле.

        Args:
            value: Значение переданное в поле
            field: Поле класса данных

        Returns:
            Any: Значение по умолчанию, если передано None, либо переданное значение
        """
        return field.default if value is None else value
