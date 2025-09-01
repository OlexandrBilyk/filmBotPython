from pydantic import BaseModel
from typing import Union
from aiogram.fsm.state import State, StatesGroup

class Film(BaseModel):
    name: str
    description: str
    rate: float
    genre: str
    actors: list[Union[str, int]]
    poster: str
    year: int
    director: str

class FilmForm(StatesGroup):
    name = State()
    description = State()
    rate = State()
    genre = State()
    actors = State()
    poster = State()
    year = State()
    director = State()

class MovieState(StatesGroup):
    search_query = State()
    filter_params = State()