from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot import dp
from database import quiz_data, get_quiz_index, get_right_answers, get_user_name, update_quiz_index, get_question
def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=option)
        )  
    builder.adjust(1)
    
    return builder.as_markup()


@dp.callback_query()
async def answer_behavior(callback: types.CallbackQuery):
    
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    answer=callback.data
    current_question_index = await get_quiz_index(callback.from_user.id)
    current_right_answers = await get_right_answers(callback.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    current_user_name = await get_user_name(callback.from_user.id)

    
    if answer == quiz_data[current_question_index]['options'][correct_option]:
        await callback.message.answer(answer)
        await callback.message.answer("Верно!")
        current_right_answers+=1
        
    else:
        await callback.message.answer(answer)
        await callback.message.answer(f"Неверно!\nПравильный ответ:{quiz_data[current_question_index]['options'][correct_option]}")
    
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_user_name, current_question_index, current_right_answers)
    

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Тест завершен!")
        await callback.message.answer(f"Вы набрали {current_right_answers} очков из {len(quiz_data)} возможных!")



async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    current_right_answers = 0
    user_name = message.from_user.username
    await update_quiz_index(user_id, user_name, current_question_index, current_right_answers)
    await get_question(message, user_id)

