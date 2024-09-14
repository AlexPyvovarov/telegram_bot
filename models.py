from pydantic import BaseModel
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class MyPlaylist(BaseModel):
    name: str
    duration: str
    genre: str
    author: list[str]
    cover: str


class SongForm(StatesGroup):
   name = State()
   duration = State()
   genre = State()
   author = State()
   cover = State()