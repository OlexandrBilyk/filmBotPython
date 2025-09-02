from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

START = Command('start')
FILMS = Command('films')
CREATE_FILM = Command('create_film')
SEARCH_FILM = Command('search_film')
FILTER_FILMS  = Command('filter_films')
SEARCH_FILM_BY_ACTOR  = Command('search_film_by_actor_name')

BOT_COMMANDS = [
    BotCommand(command='start', description='start'), 
    BotCommand(command='films', description='Вивести список фільмів'), 
    BotCommand(command='create_film', description='Додати фільм'), 
    BotCommand(command='search_film', description='Знайти фільм'), 
    BotCommand(command='filter_films', description='Відфільтрувати фільми'), 
    BotCommand(command='search_film_by_actor_name', description='Шукати фільм за ім\'ям актору'), 
]