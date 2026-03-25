from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

router = Router()
keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/movie_search'), 
                                          KeyboardButton(text='/movie_by_rating')], 
                                          [KeyboardButton(text='/low_budget_movie'),
                                          KeyboardButton(text='/high_budget_movie')],
                                          [KeyboardButton(text='/history'), 
                                          KeyboardButton(text='/help')]], resize_keyboard=True)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет {message.from_user.username}!\nЯ бот по поиску интересующих тебя фильмов, введи команду /help, чтобы увидеть список моих возможностей.', 
        reply_markup=keyboard
                         )