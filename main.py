from aiogram import executor
from app import bot


executor.start_polling(bot.dp,
                       skip_updates=True)
