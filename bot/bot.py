from aiogram import Bot, Dispatcher 
# from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, URLInputFile
import asyncio
import logging
import sys
from config_bot import BOT_TOKEN
from commands import START, FILMS, CREATE_FILM, SEARCH_FILM, FILTER_FILMS, SEARCH_FILM_BY_ACTOR, BOT_COMMANDS
from data import get_films, add_film, search_film_by_actor_name
from keybords import render_buttons, FilmCallback
from models import FilmForm, MovieState, ActorState
from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup


dp = Dispatcher()

@dp.message(START)
async def start(message: Message) -> None:
    await message.answer(""" 
    Here is a list of commands
/films
""")
    
@dp.message(SEARCH_FILM_BY_ACTOR)
async def start(message: Message, state: FSMContext) -> None:
    await state.set_state(ActorState.name)
    await message.answer(""" 
    Enter name of actor
""")
    
@dp.message(ActorState.name)
async def start(message: Message, state: FSMContext) -> None:
    data = await state.update_data(name=message.text.strip().capitalize())
    name = data.get('name', '')
    if name:
        films = search_film_by_actor_name(name)
        if films:
            for f in films:
                await message.answer(f"""
            🎬 <b>{f['name']}</b> ({f['year']})
            ⭐️ Rating: {f['rate']}
            🎭 Genre: {f['genre']}
            🎬 Director: {f['director']}
            👥 Actors: {', '.join(f['actors'])}
            📝 Description:\n{f['description']}
            📌 Poster: {f['poster']}"""
            )

    

@dp.message(SEARCH_FILM)
async def search_film(message: Message, state: FSMContext):
    await message.answer('Введіть назву фільму')
    await state.set_state(MovieState.search_query)

@dp.message(MovieState.search_query)
async def search_film(message: Message, state: FSMContext):
    text = message.text.strip()
    films = get_films()
    searched_films = [film for film in films if text in film['name']]

    if searched_films:
        for f in searched_films:
            markup = render_buttons(searched_films)
            await message.answer(text="film:" , reply_markup=markup)

    else: 
        await message.answer('Фільму за вашою назвою не знайдено')

    await  state.clear()


    
@dp.message(FILTER_FILMS)
async def filter_films(message: Message, state: FSMContext):
    await message.answer('Введіть або рік випуску або жанр або рейтинг')
    await state.set_state(MovieState.filter_params)
    
@dp.message(MovieState.filter_params)
async def filter_films(message: Message, state: FSMContext):
    text = message.text
    films = get_films()
    filtered_films = None


    try:
        text = float(text)

        if text.is_integer():
            filtered_films = [film for film in films if film['year'] == text]
        else:
            if text <= 10 and text > 0:
                filtered_films = [film for film in films if film['rate'] == text]
        
    except ValueError:
        text = text.strip()
        filtered_films = [film for film in films if text in film['genre']]

    if filtered_films:
        for f in filtered_films:
            await message.answer(f"""
🎬 <b>{f['name']}</b> ({f['year']})
⭐️ Rating: {f['rate']}
🎭 Genre: {f['genre']}
🎬 Director: {f['director']}
👥 Actors: {', '.join(f['actors'])}
📝 Description:\n{f['description']}
📌 Poster: {f['poster']}"""
)
    
    await state.clear()
    

@dp.message(CREATE_FILM)
async def create_film(message: Message, state: FSMContext):
    await state.set_state(FilmForm.name)
    await message.answer("""
Enter name of film
""")


@dp.message(FilmForm.name)
async def create_film(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FilmForm.description)
    await message.answer("""
Enter description
""")
    
@dp.message(FilmForm.description)
async def create_film(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(FilmForm.rate)
    await message.answer("""
Enter rate
""")

@dp.message(FilmForm.rate)
async def create_film(message: Message, state: FSMContext):
    await state.update_data(rate=float(message.text))
    await state.set_state(FilmForm.genre)
    await message.answer("""
Enter genre
""")
    
@dp.message(FilmForm.genre)
async def create_film(message: Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await state.set_state(FilmForm.actors)
    await message.answer("""
Enter actors like "Example, Example, Example"
""")
    
@dp.message(FilmForm.actors)
async def create_film(message: Message, state: FSMContext):
    await state.update_data(actors=[t.strip().capitalize() for t in message.text.split(',')])
    await state.set_state(FilmForm.poster)
    await message.answer("""
Enter poster url
""")
    
@dp.message(FilmForm.poster)
async def create_film(message: Message, state: FSMContext):
    await state.update_data(poster=message.text)
    await state.set_state(FilmForm.year)
    await message.answer("""
Enter year
""")
    
@dp.message(FilmForm.year)
async def create_film(message: Message, state: FSMContext):
    await state.update_data(year=int(message.text))
    await state.set_state(FilmForm.director)
    await message.answer("""
Enter director
""")
    
@dp.message(FilmForm.director)
async def create_film(message: Message, state: FSMContext):
    data = await state.update_data(director=message.text)
    add_film(data)
    await state.clear()
    await message.answer(f"""
{data['name']} was added correctly
""")



@dp.message(FILMS)
async def start(message: Message) -> None:
    films = get_films()
    markup = render_buttons(films)
    await message.answer(f"all films", reply_markup=markup)

@dp.callback_query(FilmCallback.filter())
async def send_callback_data(callback: CallbackQuery, callback_data: FilmCallback) -> None:
    film_name = callback_data.name
    film = get_films(film_name)
    await callback.message.answer(text=f"""
🎬 <b>{film['name']}</b> ({film['year']})
⭐️ Rating: {film['rate']}
🎭 Genre: {film['genre']}
🎬 Director: {film['director']}
👥 Actors: {', '.join(film['actors'])}
📝 Description:\n{film['description']}
📌 Poster: {film['poster']}"""
)

    
 
async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands(BOT_COMMANDS)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())