from threading import Lock
from typing import Optional

from loguru import logger

from telebot import types

from bot.config import DATA_PATH, IMG_PATH
from bot.my_telebot import bot
from bot.support.data_manipulation import get_block_of_words, get_words_by_block, load_dictionary, get_all_blocks, \
    get_block_count, get_words_by_block_one_by_one, get_words_by_block_with_answer

PARSE_MODE = "Markdown"

user_data = {}


class BotHandler(object):
    dictionary_data = None
    dictionary_lock = Lock()

    def __init__(self):
        self._load_dictionary()

    def run(self):
        bot.polling()

    @staticmethod
    def _load_dictionary():
        dictionary = load_dictionary(DATA_PATH)
        with BotHandler.dictionary_lock:
            BotHandler.dictionary_data = dictionary["data"]

    @staticmethod
    @bot.message_handler(commands=["help", "start"])
    def start_message(message):
        bot.send_message(
            message.chat.id,
            "Hello, I will learn English with you.\n" +
            "I have the following commands:\n\n" +
            "1. any number to display the block of words with translationn\n" +
            "2. all - to display a list of all blocks\n" +
            "3. /game for checking words\n" +
            "4. /tenses to get the tenses rules\n"
        )

    @staticmethod
    @bot.message_handler(commands=["game"])
    def ask_type_game(message):
        message = bot.reply_to(
            message, """\
                Which the block do you want to check?"""
        )
        bot.register_next_step_handler(message, BotHandler.check_block)

    block_to_check = None

    @staticmethod
    @bot.message_handler(commands=["tenses"])
    def ask_tenses(message):
        markup = types.ReplyKeyboardMarkup()
        present_simple = types.KeyboardButton("Present_simple")
        present_continuous = types.KeyboardButton("Present_continuous")
        present_perfect = types.KeyboardButton("Present_perfect")
        past_simple = types.KeyboardButton("Past_simple")
        past_continuous = types.KeyboardButton("Past_continuous")
        past_perfect = types.KeyboardButton("Past_perfect")
        future_simple = types.KeyboardButton("Future_simple")
        future_continuous = types.KeyboardButton("Future_continuous")
        future_perfect = types.KeyboardButton("Future_perfect")
        exit_btn = types.KeyboardButton("Exit")
        markup.row(present_simple, present_continuous, present_perfect)
        markup.row(past_simple, past_continuous, past_perfect)
        markup.row(future_simple, future_continuous, future_perfect)
        markup.row(exit_btn)

        message = bot.reply_to(
            message, """\
                Which the tense do you want to see?""",
            parse_mode=PARSE_MODE,
            reply_markup=markup
        )
        bot.register_next_step_handler(message, BotHandler.return_tense)

    @staticmethod
    def return_tense(message):
        markup = types.ReplyKeyboardMarkup()
        present_simple = types.KeyboardButton("Present_simple")
        present_continuous = types.KeyboardButton("Present_continuous")
        present_perfect = types.KeyboardButton("Present_perfect")
        past_simple = types.KeyboardButton("Past_simple")
        past_continuous = types.KeyboardButton("Past_continuous")
        past_perfect = types.KeyboardButton("Past_perfect")
        future_simple = types.KeyboardButton("Future_simple")
        future_continuous = types.KeyboardButton("Future_continuous")
        future_perfect = types.KeyboardButton("Future_perfect")
        exit_btn = types.KeyboardButton("Exit")
        markup.row(present_simple, present_continuous, present_perfect)
        markup.row(past_simple, past_continuous, past_perfect)
        markup.row(future_simple, future_continuous, future_perfect)
        markup.row(exit_btn)

        tenses = {
            "Present_simple": "present-simple.png",
            "Present_continuous": "present-continuous.png",
            "Present_perfect": "present-perfect.png",
            "Past_simple": "past-simple.png",
            "Past_continuous": "past-continuous.png",
            "Past_perfect": "past-perfect.png",
            "Future_simple": "future-simple.png",
            "Future_continuous": "future-continuous.png",
            "Future_perfect": "future-perfect.png"
        }

        if message.text not in tenses:
            if message.text == "Exit":
                markup = types.ReplyKeyboardRemove(selective=False)
                bot.send_message(
                    message.chat.id,
                    "*See you later*",
                    parse_mode=PARSE_MODE, reply_markup=markup
                )
                return
            message = bot.send_message(
                message.chat.id,
                "*There is not tense, please choose in button*",
                parse_mode=PARSE_MODE, reply_markup=markup
            )
            bot.register_next_step_handler(message, BotHandler.return_tense)
            return

        bot.send_photo(
            message.chat.id,
            open(f"{IMG_PATH}/{tenses[message.text]}", "rb"),
            parse_mode=PARSE_MODE,
            reply_markup=markup
        )
        bot.register_next_step_handler(message, BotHandler.return_tense)

    @staticmethod
    def check_block(message):
        markup = types.ReplyKeyboardMarkup()
        start_btn = types.KeyboardButton("Start")
        exit_btn = types.KeyboardButton("Exit")
        markup.row(start_btn, exit_btn)
        try:
            int_message = BotHandler._convert_to_int(message)
            if int_message is not None:
                logger.info(f"User {message.from_user.first_name} will start to check {int_message} block")
                user_data["block_to_check"] = int_message
                user_data["current_index_word"] = 0
                user_data["current_word"] = None
                user_data["count_index"] = get_block_count(BotHandler.dictionary_data, message.text)
                print(user_data)
                message = bot.reply_to(
                    message, "*Can we start to check words?*", parse_mode=PARSE_MODE, reply_markup=markup)
                if message.text == "Exit":
                    markup = types.ReplyKeyboardRemove(selective=False)
                    message = bot.send_message(
                        message.chat.id,
                        "*See you later*",
                        parse_mode=PARSE_MODE, reply_markup=markup
                    )
                    return
                bot.register_next_step_handler(message, BotHandler.game)
        except Exception as e:
            logger.exception(f"Error processing query {message}: {e}")

    @staticmethod
    def game(message):
        markup = types.ReplyKeyboardMarkup()
        next_btn = types.KeyboardButton("Next")
        previous_btn = types.KeyboardButton("Previous")
        answer_btn = types.KeyboardButton("Answer")
        exit_btn = types.KeyboardButton("Exit")
        markup.row(next_btn, previous_btn, answer_btn)
        markup.row(exit_btn)

        try:
            if message.text == "Start":
                word = get_words_by_block_one_by_one(
                    BotHandler.dictionary_data,
                    user_data["block_to_check"],
                    user_data["current_index_word"]
                )
                message = bot.send_message(
                    message.chat.id,
                    f"*{word}*",
                    parse_mode=PARSE_MODE, reply_markup=markup
                )
                user_data["current_word"] = word
                bot.register_next_step_handler(message, BotHandler.game)
            if message.text == "Next":
                user_data["current_index_word"] = user_data["current_index_word"] + 1
                word = get_words_by_block_one_by_one(
                    BotHandler.dictionary_data,
                    user_data["block_to_check"],
                    user_data["current_index_word"]
                )
                message = bot.send_message(
                    message.chat.id,
                    f"*{word}*",
                    parse_mode=PARSE_MODE, reply_markup=markup
                )
                user_data["current_word"] = word
                bot.register_next_step_handler(message, BotHandler.game)
            if message.text == "Previous":
                user_data["current_index_word"] = user_data["current_index_word"] - 1
                word = get_words_by_block_one_by_one(
                    BotHandler.dictionary_data,
                    user_data["block_to_check"],
                    user_data["current_index_word"]
                )
                message = bot.send_message(
                    message.chat.id,
                    f"*{word}*",
                    parse_mode=PARSE_MODE, reply_markup=markup
                )
                user_data["current_word"] = word
                bot.register_next_step_handler(message, BotHandler.game)
            if message.text == "Answer":
                answer = get_words_by_block_with_answer(
                    BotHandler.dictionary_data,
                    user_data["block_to_check"],
                    user_data["current_word"]
                )
                message = bot.send_message(
                    message.chat.id,
                    f"*{user_data['current_word']}    -     {answer}*",
                    parse_mode=PARSE_MODE, reply_markup=markup
                )
                bot.register_next_step_handler(message, BotHandler.game)
            if message.text == "Exit":
                markup = types.ReplyKeyboardRemove(selective=False)
                bot.send_message(
                    message.chat.id,
                    "*See you later*",
                    parse_mode=PARSE_MODE, reply_markup=markup
                )
        except IndexError as e:
            logger.exception(f"User want to check word with index out of range: {e}")
            markup = types.ReplyKeyboardMarkup()
            markup.row(previous_btn, exit_btn)
            bot.send_message(
                message.chat.id,
                "*That`s all, you can return to previous word*",
                parse_mode=PARSE_MODE, reply_markup=markup
            )
            bot.register_next_step_handler(message, BotHandler.game)
        except Exception as e:
            logger.exception(f"Error processing query {message}: {e}")

    @staticmethod
    @bot.message_handler(content_types=["text"])
    def send_text(message):
        # TODO: log all requests
        try:
            int_message = BotHandler._convert_to_int(message)
            if int_message is not None:
                BotHandler.process_data_block_request_message(message)
                return

            BotHandler.process_non_int_message(message)
        except Exception as e:
            logger.exception(f"Error processing query {message}: {e}")

    @staticmethod
    def process_data_block_request_message(message):
        with BotHandler.dictionary_lock:
            if message.text not in get_block_of_words(BotHandler.dictionary_data):
                bot.send_message(
                    message.chat.id,
                    "*I can't find this block in vocabulary.*",
                    parse_mode=PARSE_MODE
                )
                return

            all_words = get_words_by_block(BotHandler.dictionary_data, message.text)
            bot.send_message(message.chat.id, text=f"```{all_words}```", parse_mode="Markdown")

    @staticmethod
    def process_non_int_message(message):
        message_text = message.text.lower()

        if message_text == "all":
            bot.send_message(
                message.chat.id,
                text=f"There are all blocks\n```{get_all_blocks(BotHandler.dictionary_data)}```",
                parse_mode=PARSE_MODE
            )
        else:
            bot.send_message(
                message.chat.id,
                text="I can't understand you, run /help for additional information",
                parse_mode=PARSE_MODE
            )

    @staticmethod
    def _convert_to_int(message) -> Optional[int]:
        try:
            return int(message.text)

        except ValueError as e:
            logger.exception(f"Error processing query {message}: {e}")
            return None
