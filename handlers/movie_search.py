from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import requests

import main
from config import API_KEY

router = Router()


class Reg_search(StatesGroup):
    name = State()
    genre = State()
    variant = State()


@router.message(Command('movie_search'))
async def start_search(message: Message, state: FSMContext):
    await state.set_state(Reg_search.name)
    await message.answer('Введите имя фильма/сериала')


@router.message(Reg_search.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg_search.genre)
    await message.answer('Введите жанр')


@router.message(Reg_search.genre)
async def get_genre(message: Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await state.set_state(Reg_search.variant)
    await message.answer('Введите кол-во показываемых вариантов')


@router.message(Reg_search.variant)
async def get_variant(message: Message, state: FSMContext):
    await state.update_data(variant=message.text)

    data = await state.get_data()

    name = data["name"]
    genre = data["genre"]
    try:
        count = int(data["variant"])
    except ValueError:
        await message.answer("Введите число")
        return

    if count <= 0:
        await message.answer('Нужно указать число больше 0')
        return

    await state.clear()

    response = requests.get(
        "https://api.poiskkino.dev/v1.4/movie/search",
        headers={"X-API-KEY": API_KEY},
        params={"query" : name, 
                "limit": max(count * 3, 20)}
    )

    movies = response.json()["docs"]

    if not movies:
        await message.answer("Ничего не найдено по такому названию")
        return

    filtered_movies = []

    for movie in movies:
        genres = [g["name"].lower() for g in movie.get("genres", [])]

        if genre.lower() in genres:
            filtered_movies.append(movie)

    if not filtered_movies:
        await message.answer("Фильмы с таким жанром не найдены")
        return

    filtered_movies = filtered_movies[:count]

    await state.update_data(movies=filtered_movies)

    movie = filtered_movies[0]

    await main.send_movie(message, movie, 0)