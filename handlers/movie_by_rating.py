from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import requests

import main
from config import API_KEY

router = Router()


class Reg_rating(StatesGroup):
    rating_min = State()
    rating_max = State()
    variant = State()


@router.message(Command('movie_by_rating'))
async def start_search(message: Message, state: FSMContext):
    await state.set_state(Reg_rating.rating_min)
    await message.answer('Введите минимальный показываемый рейтинг')


@router.message(Reg_rating.rating_min)
async def get_rating_min(message: Message, state: FSMContext):
    await state.update_data(rating_min=message.text)
    await state.set_state(Reg_rating.rating_max)
    await message.answer('Введите максимальный показываемый рейтинг')


@router.message(Reg_rating.rating_max)
async def get_rating_max(message: Message, state: FSMContext):
    await state.update_data(rating_max=message.text)
    await state.set_state(Reg_rating.variant)
    await message.answer('Введите кол-во показываемых вариантов')


@router.message(Reg_rating.variant)
async def get_variant(message: Message, state: FSMContext):
    await state.update_data(variant=message.text)

    data = await state.get_data()

    try:
        rating_min = float(data["rating_min"])
        rating_max = float(data["rating_max"])
        count = int(data["variant"])
    except ValueError:
        await message.answer("Введите корректные числа")
        return

    if count <= 0:
        await message.answer('Нужно указать число больше 0')
        return

    if rating_min < 0 or rating_min > 10:
        await message.answer('Рейтинг должен быть от 0 до 10')
        return

    if rating_max < 0 or rating_max > 10:
        await message.answer('Рейтинг должен быть от 0 до 10')
        return

    if rating_min > rating_max:
        await message.answer("Минимальный рейтинг не может быть больше максимального")
        return

    await state.clear()

    response = requests.get(
        "https://api.poiskkino.dev/v1.4/movie",
        headers={"X-API-KEY": API_KEY},
        params={
            "rating.kp": f"{rating_min}-{rating_max}",
            "limit": max(count * 3, 20)
        }
    )

    all_movies = response.json()["docs"]

    movies = [m for m in all_movies if m.get("name")]

    if not movies:
        await message.answer("Нет фильмов с корректными данными")
        return

    movies.sort(
        key=lambda x: x.get("rating", {}).get("kp", 0),
        reverse=True
    )

    movies = movies[:count]

    await state.update_data(movies=movies)

    movie = movies[0]

    await main.send_movie(message, movie, 0)