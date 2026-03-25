from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer('Список моих возможностей:\n'
                         '\n/movie_search - поиск фильма/сериала по названию'
                         '\n/movie_by_rating - поиск фильмов/сериалов по рейтингу'
                         )
