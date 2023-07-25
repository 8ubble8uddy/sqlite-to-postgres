from uuid import UUID

from pydantic.dataclasses import dataclass

from models.base import BaseDataclass


@dataclass
class Genre(BaseDataclass):
    """Класс данных жанров."""

    name: str
    description: str = ''


@dataclass
class GenreFilmwork(BaseDataclass):
    """Класс данных между жанрами и кинопроизведениями."""

    film_work_id: UUID
    genre_id: UUID
