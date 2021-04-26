from bot.bot_handler import BotHandler

from loguru import logger


def main():
    logger.info("Application started")

    my_bot = BotHandler()
    my_bot.run()


if __name__ == "__main__":
    main()
