from uuid import UUID

from pydantic.dataclasses import dataclass

from models.base import BaseDataclass


@dataclass
class Person(BaseDataclass):
    """Класс данных персон."""

    full_name: str


@dataclass
class PersonFilmwork(BaseDataclass):
    """Класс данных между персонами и кинопроизведениями."""

    film_work_id: UUID
    person_id: UUID
    role: str
