from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router, F

import main

router = Router()


def movie_keyboard(index):
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="⬅️", callback_data=f"movie_{index-1}"),
            InlineKeyboardButton(text="➡️", callback_data=f"movie_{index+1}")
        ]]
    )


@router.callback_query(F.data.startswith("movie_"))
async def movie_pagination(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    movies = data.get("movies")

    index = int(callback.data.split("_")[1])

    if index < 0 or index >= len(movies):
        await callback.answer("Больше фильмов нет")
        return

    await main.edit_movie(callback, movies[index], index)