from aiogram import Bot, types
from aiogram.types import Message
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
import logging
from app.dialogs import msg
from config import TOKEN, BOT_SUBJECTS
from app import service as s
import SDAMGIA as sg

# стандартный код создания бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer(msg.start_new_user, reply_markup=s.exams_kb())


@dp.callback_query_handler(text_contains='start_')
async def save_config(callback_query: types.CallbackQuery):
    """Обработка команды start. Вывод текста и меню"""
    global callback_data
    callback_data = str(callback_query.data)[6:]
    logging.info(f"call = {callback_data}")
    await callback_query.message.answer("Выбран предмет: " + str(BOT_SUBJECTS[callback_data]))
    await callback_query.message.answer(msg.too_long)
    global test_id
    test_id = sg.sdg.generate_test(callback_data)
    global exercises
    exercises = sg.sdg.get_test_by_id(callback_data, test_id)
    global num_ex
    global cor_ans
    global total
    num_ex = 0
    cor_ans = 0
    total = 0
    await callback_query.message.answer(msg.before_test, reply_markup=s.MAIN_KB)


@dp.message_handler(lambda message: message.text == msg.btn_var)
async def get_results_var(message: types.Message):
    await message.answer(msg.if_by_var)
    await message.answer(sg.sdg.generate_pdf(callback_data, test_id))
    await message.answer(msg.before_check, reply_markup=s.check_kb())


@dp.callback_query_handler(text_contains='check_')
async def save_config(callback_query: types.CallbackQuery):
    await callback_query.message.answer(sg.sdg.generate_answ_pdf(callback_data, test_id))


@dp.message_handler(lambda message: message.text == msg.btn_one)
async def get_results_one(message: types.Message):
    await message.answer(msg.if_by_one)
    await message.answer(sg.sdg.generate_pdf_by_one(callback_data, exercises[num_ex]))


@dp.message_handler()
async def answer_by_user(message: types.Message):
    global num_ex, cor_ans, total
    if sg.sdg.get_problem_by_id(callback_data, exercises[num_ex])['answer'] == message.text:
        cor_ans += 1
        await message.answer(msg.correct_answer, reply_markup=s.ans_kb())
    else:
        await message.answer(msg.wrong_answer, reply_markup=s.ans_kb())


@dp.callback_query_handler(text_contains='answer_')
async def save_config(callback_query: types.CallbackQuery):
    call = str(callback_query.data)[7:]
    logging.info(f"call = {call}")
    global exercises, total, cor_ans, num_ex
    if num_ex < len(exercises) - 1:
        if call == msg.solution:
            await callback_query.message.answer(sg.sdg.get_problem_by_id(callback_data, exercises[num_ex])['answer'])
        elif call == msg.next_ex:
            total += 1
            num_ex += 1
            await callback_query.message.answer(sg.sdg.generate_pdf_by_one(callback_data, exercises[num_ex]))
    elif num_ex == len(exercises) - 1:
        if call == msg.solution:
            await callback_query.message.answer(sg.sdg.get_problem_by_id(callback_data, exercises[num_ex - 1])['answer'])
        elif call == msg.next_ex:
            num_ex += 1
            total += 1
            await callback_query.message.answer(msg.no_results)
        await callback_query.message.answer(msg.results)
        await callback_query.message.answer(msg.final_total)
        await callback_query.message.answer(total + 1)
        await callback_query.message.answer(msg.final_correct)
        await callback_query.message.answer(cor_ans)
    else:
        if call == msg.next_ex:
            await callback_query.message.answer(msg.no_results)
        await callback_query.message.answer(msg.final_total)
        await callback_query.message.answer(total + 1)
        await callback_query.message.answer(msg.final_correct)
        await callback_query.message.answer(cor_ans)
