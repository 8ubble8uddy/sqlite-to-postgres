from datetime import date
from typing import Optional

from pydantic.dataclasses import dataclass

from models.base import BaseDataclass


@dataclass
class Filmwork(BaseDataclass):
    """Класс данных кинопроизведений."""

    title: str
    type: str
    description: str = ''
    creation_date: Optional[date] = None
    rating: float = 0
