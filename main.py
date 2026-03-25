import asyncio
from aiogram.types import InputMediaPhoto
from aiogram import Bot, Dispatcher

import pagination
from handlers import start, help, movie_search, movie_by_rating
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()


def build_movie_text(movie):
    name = movie.get("name")
    year = movie.get("year")

    rating = movie.get("rating", {}).get("kp")
    rating_text = round(rating, 1) if rating else "Не указан"

    description = movie.get("description") or "Нет описания"

    genres = [g["name"] for g in movie.get("genres", [])]
    genres_text = ", ".join(genres) if genres else "Не указаны"

    age = movie.get("ageRating")
    age_text = f"{age}+" if age else "Не указан"

    budget = movie.get("budget", {}).get("value")
    budget_text = f"{budget}+" if budget else "Не указан"

    return f"""
🎬 {name}

📅 Год: {year}
⭐ Рейтинг: {rating_text}
🎭 Жанры: {genres_text}
🔞 Возраст: {age_text}
💰 Бюджет: {budget_text}

📖 {description}
"""


async def send_movie(message, movie, index):
    text = build_movie_text(movie)
    poster = movie.get("poster", {}).get("url")
    keyboard = pagination.movie_keyboard(index)

    if poster:
        await message.answer_photo(photo=poster, caption=text, reply_markup=keyboard)
    else:
        await message.answer(text, reply_markup=keyboard)


async def edit_movie(callback, movie, index):
    text = build_movie_text(movie)
    poster = movie.get("poster", {}).get("url")
    keyboard = pagination.movie_keyboard(index)

    msg = callback.message

    try:
        if msg.photo and not poster:
            await msg.delete()
            await msg.answer(text, reply_markup=keyboard)

        elif poster:
            await msg.edit_media(
                media=InputMediaPhoto(media=poster, caption=text),
                reply_markup=keyboard
            )

        else:
            await msg.edit_text(text, reply_markup=keyboard)

    except Exception:
        await msg.answer(text, reply_markup=keyboard)

    await callback.answer()


async def main():
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(movie_search.router)
    dp.include_router(movie_by_rating.router)
    dp.include_router(pagination.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")