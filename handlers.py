from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters.command import Command
from bot import dp
from utils import types, new_quiz
from aiogram import F
from database import get_rating
# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Рейтинг участников"))
    
    await message.answer("Добро пожаловать!", reply_markup=builder.as_markup(resize_keyboard=True))
    
# Хэндлер на команду /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer("Давайте начнем тест!")
    await new_quiz(message)


@dp.message(F.text=="Рейтинг участников")
@dp.message(Command("rating"))
async def cmd_rating(message: types.Message):
    rating = await get_rating()
    sorted_rating = sorted(rating, key=lambda x: x[1], reverse=True)
    sorted_rating_text = "\n".join([f"{user_name}, количество очков: {right_answers}" for user_name, right_answers in sorted_rating])
    await message.answer(f"Рейтинг участников:\n{sorted_rating_text}\n_________________________\nСохраняется только последнее прохождение теста!")