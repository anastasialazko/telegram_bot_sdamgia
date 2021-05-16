from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
                          InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_SUBJECTS
from app.dialogs import msg

MAIN_KB = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).row(
    KeyboardButton(msg.btn_var),
    KeyboardButton(msg.btn_one)
)


def exams_kb():
    kb = InlineKeyboardMarkup()
    exams_keys = list(BOT_SUBJECTS.keys())
    for ex_id in exams_keys:
            kb.add(InlineKeyboardButton(
                BOT_SUBJECTS[ex_id],
                callback_data=f"start_{ex_id}"
            ))
    return kb


ANSW_KB = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).row(
    KeyboardButton(msg.next_ex),
    KeyboardButton(msg.solution)
)

def ans_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton( msg.solution, callback_data=f"answer_{msg.solution}"))
    kb.add(InlineKeyboardButton(msg.next_ex, callback_data=f"answer_{msg.next_ex}"))
    return kb


def check_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton( msg.check, callback_data=f"check_{msg.solution}"))
    return kb
