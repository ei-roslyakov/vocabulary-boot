from bot.config import SECRET_TOKEN

import telebot

bot = telebot.TeleBot(SECRET_TOKEN)
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
