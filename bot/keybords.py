from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData



class FilmCallback(CallbackData, prefix='film', sep=';'):
   id: int
   name: str

def render_buttons(films: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for i, film in enumerate(films):
         callback_data = FilmCallback(id=i, name=film['name'])
         builder.button(text=f"{film['name']}", callback_data=callback_data)

    builder.adjust(1, True)
    return builder.as_markup()    